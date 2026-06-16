---
name: qa
description: >
  Run API-level QA tests for LedgerLine. Analyzes git diff to determine which
  services are affected, starts those services locally, exercises them via curl,
  and generates a structured report. Use when testing PRs or smoke-testing the
  running environment.
---

# QA Orchestrator — LedgerLine

**SCOPE: Functional/API QA only — verifying that the services behave correctly
by making real HTTP requests. Do NOT run pytest, flake8, or any CI checks. Those
are handled by the python-app.yml workflow.**

## Step 1: Load Configuration

Read `.factory/skills/qa/config.yaml` for environment URLs, service start
commands, and app path patterns.

## Step 2: Determine Target Environment

Default is `local`. If the user specifies `gke`, substitute the GKE URLs from
config. Respect environment restrictions.

## Step 3: Analyze Git Diff

```bash
git diff origin/main...HEAD --name-only
```

Map changed files to services using `path_patterns` in config.yaml:

- `app.py`, `categorize.py`, `config.py`, `templates/**`, `static/**` → **ledger**
- `reminders/**` → **reminders**
- `recommendations/**` → **recommendations**

Files outside all path patterns (`.github/**`, `k8s/**`, `demo/**`, `.factory/**`,
`tests/**`) are NOT associated with any service. Report INCONCLUSIVE if only
non-service files changed.

## Step 4: Start Affected Services (local mode)

For each affected service, start it in the background if not already running:

```bash
# ledger
SECRET_KEY=dev python app.py &
sleep 2 && curl -sf http://127.0.0.1:5000/health || echo "ledger not ready"

# reminders
python reminders/app.py &
sleep 2 && curl -sf http://127.0.0.1:8001/health || echo "reminders not ready"

# recommendations
python recommendations/app.py &
sleep 2 && curl -sf http://127.0.0.1:8002/health || echo "recommendations not ready"
```

If a service fails to start, mark all its tests as BLOCKED and continue with
other affected services.

**For the ledger service, run the migration first:**
```bash
FLASK_APP=app.py flask db upgrade
```

## Step 5: Execute Relevant Flows

For each affected service, load its sub-skill and run only the flows relevant
to the diff. Generate additional targeted tests for the specific changes.

- Ledger changes → `.factory/skills/qa-ledger/SKILL.md`
- Reminders changes → `.factory/skills/qa-reminders/SKILL.md`
- Recommendations changes → `.factory/skills/qa-recommendations/SKILL.md`

## Step 6: Evidence Capture

Capture curl responses as text evidence. Include:
- HTTP status codes
- Relevant response body fields
- Before/after state for mutation tests

Embed evidence as fenced code blocks in the report.

## Step 7: Cleanup

After tests complete:
```bash
# stop background services
pkill -f "python app.py" 2>/dev/null
pkill -f "reminders/app.py" 2>/dev/null
pkill -f "recommendations/app.py" 2>/dev/null

# clean test transactions from ledger DB
sqlite3 ledgerline.db "DELETE FROM 'transaction' WHERE description LIKE 'QA:%';"
```

## Step 8: Generate Report

Write the report to `./qa-results/report.md` using the template at
`.factory/skills/qa/REPORT-TEMPLATE.md`.

## Step 9: Suggest Skill Updates

After generating the report, check for new failure patterns per the
`failure_learning: open_pr` strategy. Write `qa-results/skill-updates.json`
if any new environment insights were found.

## Step 10: Never Skip Silently

If a flow cannot complete, report it as BLOCKED with what was tried and how
to fix it. Continue with remaining flows.
