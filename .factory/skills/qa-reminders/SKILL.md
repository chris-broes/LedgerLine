---
name: qa-reminders
description: >
  API-level QA tests for the LedgerLine reminders microservice (aiohttp, port 8001).
  Tests reminder CRUD, blank-title validation, completion toggling, and static UI serving.
---

# QA Sub-Skill: Reminders Service

**Base URL:** `http://127.0.0.1:8001`

**Start command:**
```bash
python reminders/app.py &
sleep 2
```

**Auth:** None required.

---

## Available Test Flows

### Flow 1: Health Check
```bash
curl -sf http://127.0.0.1:8001/health
# Expect: {"status":"ok"}
```

### Flow 2: List Reminders
```bash
curl -sf http://127.0.0.1:8001/reminders
# Expect: JSON array, includes the seeded default reminder
```

### Flow 3: Create Reminder
```bash
curl -sf -X POST http://127.0.0.1:8001/reminders \
  -H "Content-Type: application/json" \
  -d '{"title":"QA: Transfer to savings"}'
# Expect: 201, JSON with id, title, completed=false
```

### Flow 4: Blank Title Rejected (seeded bug T2)
```bash
STATUS=$(curl -s -o /tmp/qa-blank.json -w "%{http_code}" -X POST \
  http://127.0.0.1:8001/reminders \
  -H "Content-Type: application/json" \
  -d '{"title":""}')
echo "Status: $STATUS"
cat /tmp/qa-blank.json
# Current expected: 201 with blank title (BUG — confirms T2 still unfixed)
# Post-fix expected: 400 {"error":"Title is required"}

# Whitespace-only title
STATUS2=$(curl -s -o /tmp/qa-ws.json -w "%{http_code}" -X POST \
  http://127.0.0.1:8001/reminders \
  -H "Content-Type: application/json" \
  -d '{"title":"   "}')
echo "Status whitespace: $STATUS2"
# Post-fix expected: 400
```

### Flow 5: Get Single Reminder
```bash
ID=$(curl -sf -X POST http://127.0.0.1:8001/reminders \
  -H "Content-Type: application/json" -d '{"title":"QA: Get test"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
curl -sf http://127.0.0.1:8001/reminders/$ID
# Expect: 200, correct reminder object
```

### Flow 6: Toggle Completion
```bash
ID=$(curl -sf -X POST http://127.0.0.1:8001/reminders \
  -H "Content-Type: application/json" -d '{"title":"QA: Toggle"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
RESULT=$(curl -sf -X PUT http://127.0.0.1:8001/reminders/$ID \
  -H "Content-Type: application/json" -d '{"completed":true}')
echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print('PASS' if d['completed'] else 'FAIL')"
```

### Flow 7: Delete Reminder
```bash
ID=$(curl -sf -X POST http://127.0.0.1:8001/reminders \
  -H "Content-Type: application/json" -d '{"title":"QA: Delete me"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
curl -sf -X DELETE http://127.0.0.1:8001/reminders/$ID
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001/reminders/$ID)
[ "$STATUS" = "404" ] && echo "PASS: deleted" || echo "FAIL: still exists ($STATUS)"
```

### Flow 8: Static UI Served
```bash
curl -sf http://127.0.0.1:8001/static/index.html | grep -o "Payment Reminders\|LedgerLine"
# Expect: both strings present
```

### Flow 9: Not Found Returns 404
```bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8001/reminders/99999)
[ "$STATUS" = "404" ] && echo "PASS" || echo "FAIL: got $STATUS"
```

---

## Known Failure Modes

1. **State is in-memory.** Restarting the service resets all reminders to only the seeded default. Tests that depend on previously created reminders must create them in the same test run.

2. **No CSRF / no auth.** All endpoints are open — no token needed.
