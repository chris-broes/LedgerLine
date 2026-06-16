---
name: qa-recommendations
description: >
  API-level QA tests for the LedgerLine recommendations microservice (aiohttp, port 8002).
  Tests the product catalog, rules engine logic, input validation, and spending-profile-driven
  recommendation accuracy.
---

# QA Sub-Skill: Recommendations Service

**Base URL:** `http://127.0.0.1:8002`

**Start command:**
```bash
python recommendations/app.py &
sleep 2
```

**Auth:** None required.

---

## Available Test Flows

### Flow 1: Health Check
```bash
curl -sf http://127.0.0.1:8002/health
# Expect: {"status":"ok"}
```

### Flow 2: Product Catalog
```bash
curl -sf http://127.0.0.1:8002/products | python3 -c \
  "import sys,json; d=json.load(sys.stdin); print(len(d['products']), 'products')"
# Expect: 6 products
```

### Flow 3: Cashback Card — Heavy Dining Spend
```bash
curl -sf -X POST http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d '{"balance":200,"category_totals":{"Dining":150.0},"subscription_count":0}' \
| python3 -c "import sys,json; recs=json.load(sys.stdin)['recommendations']; \
  names=[r['name'] for r in recs]; \
  print('PASS' if any('Cashback' in n for n in names) else 'FAIL', names)"
```

### Flow 4: High-Yield Savings — Large Positive Balance
```bash
curl -sf -X POST http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d '{"balance":1500,"category_totals":{},"subscription_count":0}' \
| python3 -c "import sys,json; recs=json.load(sys.stdin)['recommendations']; \
  names=[r['name'] for r in recs]; \
  print('PASS' if any('High-Yield' in n for n in names) else 'FAIL', names)"
```

### Flow 5: Credit Builder — Negative Balance
```bash
curl -sf -X POST http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d '{"balance":-200,"category_totals":{},"subscription_count":0}' \
| python3 -c "import sys,json; recs=json.load(sys.stdin)['recommendations']; \
  names=[r['name'] for r in recs]; \
  print('PASS' if any('Credit Builder' in n for n in names) else 'FAIL', names)"
```

### Flow 6: Subscription Optimizer — Many Subscriptions
```bash
curl -sf -X POST http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d '{"balance":0,"category_totals":{"Subscriptions":60.0},"subscription_count":4}' \
| python3 -c "import sys,json; recs=json.load(sys.stdin)['recommendations']; \
  names=[r['name'] for r in recs]; \
  print('PASS' if any('Optimizer' in n for n in names) else 'FAIL', names)"
```

### Flow 7: Capped at 3 Recommendations
```bash
COUNT=$(curl -sf -X POST http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d '{"balance":1000,"category_totals":{"Dining":200,"Transport":80,"Subscriptions":50},"subscription_count":4}' \
| python3 -c "import sys,json; print(len(json.load(sys.stdin)['recommendations']))")
[ "$COUNT" -le 3 ] && echo "PASS: $COUNT recs (≤3)" || echo "FAIL: $COUNT recs (>3)"
```

### Flow 8: Empty Profile Falls Back to Default
```bash
curl -sf -X POST http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d '{}' \
| python3 -c "import sys,json; recs=json.load(sys.stdin)['recommendations']; \
  print('PASS' if len(recs)==1 and 'Round-Up' in recs[0]['name'] else 'FAIL', [r['name'] for r in recs])"
```

### Flow 9: Each Recommendation Has a Reason
```bash
curl -sf -X POST http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d '{"balance":800,"category_totals":{"Dining":120.0},"subscription_count":0}' \
| python3 -c "import sys,json; \
  recs=json.load(sys.stdin)['recommendations']; \
  missing=[r['name'] for r in recs if not r.get('reason','').strip()]; \
  print('PASS' if not missing else 'FAIL: missing reason', missing)"
```

### Flow 10: Invalid Body Rejected
```bash
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  http://127.0.0.1:8002/recommendations \
  -H "Content-Type: application/json" \
  -d 'not valid json')
[ "$STATUS" = "400" ] && echo "PASS: 400 on bad JSON" || echo "FAIL: got $STATUS"
```

---

## Known Failure Modes

1. **State is in-memory.** Restarting the service resets the in-memory product catalog and counters. Tests are stateless by design — each POST is independent.

2. **Non-dict body returns 400.** Sending a JSON array or scalar instead of an object will return 400. This is intended behavior.
