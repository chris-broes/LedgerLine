---
name: qa-ledger
description: >
  API-level QA tests for the LedgerLine ledger service (Flask, port 5000).
  Tests transaction posting, amount sign integrity, auto-categorization,
  balance calculation, insights rendering, and recommendations integration.
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
  -d "description=QA: Coffee&amount=-6.50&category=Dining" \
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
  -d "description=QA: Payroll&amount=1450.00&category=Income" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L | grep -o "QA: Payroll\|+\$1450"

sqlite3 ledgerline.db "SELECT amount FROM 'transaction' WHERE description='QA: Payroll' ORDER BY id DESC LIMIT 1;"
# Expect: 1450.0
```

### Flow 4: Balance Calculation
```bash
# After posting purchase (-6.50) and income (1450.00):
sqlite3 ledgerline.db "SELECT SUM(amount) FROM 'transaction' WHERE description LIKE 'QA:%';"
# Expect: 1443.5  (income - purchase)
```

### Flow 5: Auto-Categorization
```bash
# "Uber Eats" MUST categorize as Dining (not Transport — this is seeded bug T7)
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Uber Eats order&amount=-23.40&category=Auto" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L

sqlite3 ledgerline.db "SELECT category FROM 'transaction' WHERE description='QA: Uber Eats order' ORDER BY id DESC LIMIT 1;"
# Current expected: Transport (the seeded bug — confirms T7 still unfixed)
# Post-fix expected: Dining

# Netflix should categorize as Subscriptions
curl -sf -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Netflix monthly&amount=-15.99&category=Auto" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt -L

sqlite3 ledgerline.db "SELECT category FROM 'transaction' WHERE description='QA: Netflix monthly' ORDER BY id DESC LIMIT 1;"
# Expect: Subscriptions
```

### Flow 6: Index Page Renders (balance, chart, activity)
```bash
PAGE=$(curl -sf http://127.0.0.1:5000/)
echo "$PAGE" | grep -o "Current Balance\|Balance Over Time\|Recent Activity\|Spending by Category"
# Expect all four headings present
```

### Flow 7: Newest-First Ordering
```bash
# Post two transactions with known descriptions, verify newer appears first in HTML
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
# Requires recommendations service running
PAGE=$(curl -sf http://127.0.0.1:5000/)
echo "$PAGE" | grep -oE "Cashback Card|High-Yield Savings|Subscription Optimizer|temporarily unavailable"
# Expect one or more product names (or "temporarily unavailable" if :8002 is down)
```

### Flow 9: Graceful Degradation (recommendations service down)
```bash
# Stop the recommendations service, confirm dashboard still renders
pkill -f "recommendations/app.py" 2>/dev/null; sleep 1
PAGE=$(curl -sf http://127.0.0.1:5000/)
echo "$PAGE" | grep -o "temporarily unavailable\|Current Balance"
# Expect: both present (page renders, recs show unavailable message)
# Restart recs service afterward
python recommendations/app.py &
```

### Flow 10: Invalid Amount Rejected
```bash
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:5000/add \
  -d "description=QA: Bad&amount=not-a-number&category=Other" \
  -c /tmp/qa-cookies.txt -b /tmp/qa-cookies.txt)
# Expect: 400
echo "Status: $HTTP_STATUS"
```

---

## Cleanup

```bash
sqlite3 ledgerline.db "DELETE FROM 'transaction' WHERE description LIKE 'QA:%';"
```

---

## Known Failure Modes

1. **CSRF token rejection on POST.** The Flask-WTF CSRF token is embedded in the HTML form. curl POSTs without a valid token will fail form validation silently (200 with re-rendered form, not 302 redirect). Workaround: use the `-c`/`-b` cookie jar AND fetch the form first to capture the token:
   ```bash
   TOKEN=$(curl -sf -c /tmp/qa-cookies.txt http://127.0.0.1:5000/add | grep -oP 'value="\K[^"]+(?=".*hidden)' | head -1)
   curl -sf -X POST ... -d "csrf_token=$TOKEN&..." -b /tmp/qa-cookies.txt
   ```
   Alternatively: set `WTF_CSRF_ENABLED=false` only in the QA environment (test env does this via conftest.py).

2. **ledgerline.db missing table.** If the migration stamp is stale, `flask db upgrade` is a no-op and `/health` returns `{"status":"error"}`. Fix: `sqlite3 ledgerline.db "DELETE FROM alembic_version;" && FLASK_APP=app.py flask db upgrade`.

3. **Port 5000 in use by macOS AirPlay.** macOS ControlCenter squats port 5000. Run ledger on `--port 5001` and update URLs accordingly.
