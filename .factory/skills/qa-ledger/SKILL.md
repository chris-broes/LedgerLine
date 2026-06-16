---
name: qa-ledger
description: >
  API-level QA tests for the LedgerLine ledger service (Flask, port 5000).
  Tests transaction posting, amount sign integrity, auto-categorization,
  balance calculation, dashboard rendering, and recommendations integration.
  Includes visual QA for the Sankey cash-flow diagram.
---

# QA Sub-Skill: Ledger Service

**Base URL:** `http://127.0.0.1:5000` (local) or `https://ledger.example.com` (GKE)

**Start command:**
```bash
FLASK_APP=app.py flask db upgrade
SECRET_KEY=dev python app.py &
sleep 2
```

**Auth:** None required.

**Category vocabulary (as of Monarch redesign):**
- Spending categories: `Housing`, `Food`, `Transport`, `Subscriptions`, `Shopping`, `Health`, `Other`
- Income/credit: `Income`, `Refund`
- `Food` replaced the former `Dining` and `Groceries` categories.
- Auto-detect maps coffee/restaurant/delivery → `Food`; grocery/market → `Food`.

---

## Available Test Flows

Run only the flows relevant to the current diff. Each flow is self-contained.

### Flow 1: Health Check
```bash
curl -sf http://127.0.0.1:5000/health
# Expect: {"status":"ok","database":"ok"}
```

### Flow 2: Transaction Posting — Purchase (sign integrity)
The core domain invariant: negative amounts must be stored as negative.

```bash
# Post a purchase
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Coffee&amount=-6.50&category=Food" \
  -c /tmp/qa-cookies.txt \
  -b /tmp/qa-cookies.txt \
  -L | grep -o "QA: Coffee\|-\$6\.50"

# Verify via DB
sqlite3 ledgerline.db "SELECT amount FROM 'transaction' WHERE description='QA: Coffee' ORDER BY id DESC LIMIT 1;"
# Expect: -6.5  (NOT 6.5 — sign integrity is the star bug)
```

### Flow 3: Transaction Posting — Income/Credit
```bash
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Payroll&amount=2150.00&category=Income" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L | grep -o "QA: Payroll\|+\$2150"

sqlite3 ledgerline.db "SELECT amount FROM 'transaction' WHERE description='QA: Payroll' ORDER BY id DESC LIMIT 1;"
# Expect: 2150.0
```

### Flow 4: Balance Calculation
```bash
# After posting purchase (-6.50) and income (2150.00):
sqlite3 ledgerline.db "SELECT SUM(amount) FROM 'transaction' WHERE description LIKE 'QA:%';"
# Expect: 2143.5  (income - purchase)
```

### Flow 5: Auto-Categorization
```bash
# "Uber Eats" MUST categorize as Food (not Transport — seeded bug T7)
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Uber Eats order&amount=-23.40&category=Auto" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L

sqlite3 ledgerline.db "SELECT category FROM 'transaction' WHERE description='QA: Uber Eats order' ORDER BY id DESC LIMIT 1;"
# Current expected: Transport (seeded bug T7 — confirms still unfixed)
# Post-fix expected: Food

# Netflix should categorize as Subscriptions (control — must not regress)
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Netflix monthly&amount=-15.99&category=Auto" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L

sqlite3 ledgerline.db "SELECT category FROM 'transaction' WHERE description='QA: Netflix monthly' ORDER BY id DESC LIMIT 1;"
# Expect: Subscriptions

# Uber (non-food) should remain Transport
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Uber ride&amount=-18.50&category=Auto" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L

sqlite3 ledgerline.db "SELECT category FROM 'transaction' WHERE description='QA: Uber ride' ORDER BY id DESC LIMIT 1;"
# Expect: Transport (must not regress when T7 is fixed)
```

### Flow 6: Dashboard Renders (balance, chart, activity)
```bash
PAGE=$(curl -sf http://127.0.0.1:5000/)
echo "$PAGE" | grep -o "Net Balance\|Balance Over Time\|Recent Activity\|Spending by Category"
# Expect all four headings present
```

### Flow 7: Newest-First Ordering
```bash
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: OLDER&amount=-1.00&category=Other" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L > /dev/null
sleep 1
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: NEWER&amount=-2.00&category=Other" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L > /dev/null

PAGE=$(curl -sf http://127.0.0.1:5000/)
OLDER_POS=$(echo "$PAGE" | grep -n "QA: OLDER" | head -1 | cut -d: -f1)
NEWER_POS=$(echo "$PAGE" | grep -n "QA: NEWER" | head -1 | cut -d: -f1)
[ "$NEWER_POS" -lt "$OLDER_POS" ] && echo "PASS: newest first" || echo "FAIL: ordering wrong"
```

### Flow 8: Recommendations Integration (live call to :8002)
```bash
PAGE=$(curl -sf http://127.0.0.1:5000/)
echo "$PAGE" | grep -oE "Cashback Card|High-Yield Savings|Subscription Optimizer|temporarily unavailable"
# Expect one or more product names (or "temporarily unavailable" if :8002 is down)
```

### Flow 9: Graceful Degradation (recommendations service down)
```bash
pkill -f "recommendations/app.py" 2>/dev/null; sleep 1
PAGE=$(curl -sf http://127.0.0.1:5000/)
echo "$PAGE" | grep -o "temporarily unavailable\|Net Balance"
# Expect: both present (page renders; recs show unavailable message)
python recommendations/app.py &
```

### Flow 10: Invalid Amount Rejected
```bash
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Bad&amount=not-a-number&category=Other" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt)
echo "Status: $HTTP_STATUS"
# Expect: 400
```

### Flow 11: Sankey Diagram — Visual Text-Overlap Check
```bash
# Requires the ledger service running. Fetches live HTML, estimates SVG label
# bounding boxes, reports any intersecting pairs.
python tests/check_sankey_overlaps.py http://127.0.0.1:5000
# Expect: PASS  No Sankey text overlaps (N labels checked)
```

---

## Cleanup

```bash
sqlite3 ledgerline.db "DELETE FROM 'transaction' WHERE description LIKE 'QA:%';"
```

---

## Known Failure Modes

1. **CSRF token rejection on POST.** curl POSTs without a CSRF token fail silently (200 with re-rendered form, no redirect). Workaround: fetch the form first to get the token:
   ```bash
   TOKEN=$(curl -sf -c /tmp/qa-cookies.txt http://127.0.0.1:5000/add | grep -oP 'value="\K[^"]+(?=".*hidden)' | head -1)
   curl -sf -X POST ... -d "csrf_token=$TOKEN&..." -b /tmp/qa-cookies.txt
   ```
   Alternatively: set `WTF_CSRF_ENABLED=false` for the QA environment.

2. **ledgerline.db missing table.** If the migration stamp is stale, `/health` returns `{"status":"error"}`. Fix:
   ```bash
   sqlite3 ledgerline.db "DELETE FROM alembic_version;" && FLASK_APP=app.py flask db upgrade
   ```

3. **Port 5000 in use by macOS AirPlay.** Run ledger on `--port 5001` and update URLs accordingly.

4. **Sankey overlap check requires Python 3.x** and no additional packages — it uses `urllib.request` and `re` from the stdlib only.
