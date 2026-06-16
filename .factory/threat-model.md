# LedgerLine — Threat Model

This file is read by Factory Droid's security review skill to anchor STRIDE/OWASP
analysis against LedgerLine's specific attack surface.

## System Overview

LedgerLine is a personal-finance web application with three services:

| Service | Technology | Port | Exposure |
|---|---|---|---|
| ledger | Flask + SQLAlchemy | 8000 | Public (Ingress) |
| reminders | aiohttp + static SPA | 8001 | Public (Ingress) |
| recommendations | aiohttp REST API | 8002 | Internal only (ClusterIP) |

**Persistence:** SQLite (dev/demo) or Cloud SQL PostgreSQL (production).
**Auth:** None — single-user, demo-scoped. No login, no sessions beyond CSRF.
**Deployment target:** GKE (see `k8s/`).

---

## Trust Boundaries

1. **Internet → Ingress → ledger/reminders**: unauthenticated public traffic.
2. **ledger → recommendations**: intra-cluster only; ledger makes outbound HTTP POST.
3. **ledger → SQLite/Cloud SQL**: local file or TCP to Cloud SQL proxy.
4. **GitHub Actions (toaster1)**: self-hosted runner with `GH_PAT` + `FACTORY_API_KEY`.

---

## High-Value Assets

| Asset | Sensitivity | Notes |
|---|---|---|
| Transaction data (amounts, categories) | High | Sign integrity is a product invariant |
| Balance calculation | High | Corrupted balance = direct user harm |
| `SECRET_KEY` | High | Governs CSRF token validity |
| `DATABASE_URL` | High | Full ledger data access |
| `GH_PAT` | High | Repo write access, used for PR creation |
| `FACTORY_API_KEY` | High | LLM agent execution |
| Product recommendations | Medium | Integrity matters (wrong recs = bad UX) |

---

## STRIDE Analysis

### Spoofing
- **No auth** on the ledger or reminders UI — any user on the network can post
  transactions or reminders. Acceptable for demo scope; must be addressed before
  multi-user production deployment.
- `SECRET_KEY` must be set via environment; if unset the app refuses to start
  (enforced in `app.py`).

### Tampering
- **Amount sign stripping** (`_parse_amount` regex `\d+` drops minus sign) —
  the seeded demo bug. A malicious or erroneous client can cause credits to be
  stored as charges. Fix: regex must be `-?\d+(?:\.\d+)?`.
- No input length limits on `description` beyond WTF `Length(max=200)`.
- Reminders titles have no length limit at the API boundary.
- SQLite file is writable on the host; PVC in k8s — access control is
  infrastructure-level only.

### Repudiation
- No audit log for transaction mutations. For a production fintech app,
  every create/update/delete should be logged with timestamp and source IP.

### Information Disclosure
- `DEBUG=False` enforced in `ProductionConfig` and guarded in `app.py`.
- Tracebacks not exposed to users (Flask default in production mode).
- `SECRET_KEY` never logged or committed (env-var only).
- `DATABASE_URL` with credentials never logged.
- The recommendations service returns full product details including reasons
  derived from user spend — no PII, but spending patterns are sensitive.

### Denial of Service
- No rate limiting on `/add` — an attacker can flood the transaction table.
- No request size limit beyond Flask defaults (16MB). Consider limiting
  `MAX_CONTENT_LENGTH`.
- Recommendations service holds state in memory; restart resets it — low
  DoS surface but zero persistence.

### Elevation of Privilege
- Single-user app — no role system to escalate within.
- `GH_PAT` has repo write scope; if leaked, attacker can push to `main`.
  Scope should be restricted to the minimum needed (fine-grained PAT, target
  repo only, no admin).
- self-hosted runner (`toaster1`) executes arbitrary workflow code. Owner-gating
  (issue author must be `OWNER`) limits who can trigger Droid agent runs.
  Any repo contributor can trigger `pull_request`-based workflows.

---

## OWASP Top 10 Notes

| # | Risk | Status |
|---|---|---|
| A01 Broken Access Control | **Open** — no auth; anyone can post/delete. Acceptable for demo. |
| A02 Cryptographic Failures | `SECRET_KEY` from env; no passwords stored; SQLite not encrypted at rest. |
| A03 Injection | SQLAlchemy ORM used throughout — no raw SQL. CSRF on all forms. |
| A04 Insecure Design | Amount sign bug is an insecure design issue — no server-side sign enforcement. |
| A05 Security Misconfiguration | `DEBUG=False` enforced; no default credentials. |
| A06 Vulnerable Components | Dependencies pinned in `requirements.txt`. CodeQL + bandit in CI. |
| A07 Authentication Failures | N/A (no auth). |
| A08 Software Integrity | All agent PRs go through CI + review + security review before merge. |
| A09 Logging Failures | No audit log for mutations. Flask `logger` in place for errors only. |
| A10 SSRF | Ledger calls `RECOMMENDATIONS_URL` (env-configured). Internal cluster DNS only in production; validate URL scheme and host before making outbound calls. |

---

## Key Invariants for Security Review

When reviewing any PR, Droid should verify:

1. **Sign integrity**: `_parse_amount` must preserve the minus sign. Any change
   to amount parsing must be tested with negative inputs.
2. **No secrets in code**: `SECRET_KEY`, `DATABASE_URL`, `GH_PAT`,
   `FACTORY_API_KEY` must never appear in source files.
3. **No `debug=True`**: Flask must not be started with debug mode in committed code.
4. **CSRF on all state-changing routes**: every POST must include the WTF CSRF token.
5. **RECOMMENDATIONS_URL validated**: outbound HTTP from ledger must only target
   the configured internal URL; never accept a user-supplied URL.
6. **Regression tests required**: any bug fix must include a test that would have
   caught the original defect.
