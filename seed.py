"""Seed the ledger with a realistic month of demo transactions.

Usage: SECRET_KEY=dev python seed.py
Replaces any existing transactions so reseeding is idempotent.
"""

from datetime import datetime, time, timedelta

from app import app, db, Transaction

# (description, days_ago, hour, amount, category, subcategory)
# Negative = purchase; positive = income/credit.
SEED_TRANSACTIONS = [
    # ── Income ───────────────────────────────────────────────────────────
    ('ACME Corp payroll',          1,   6,  2150.00, 'Income',        'Payroll'),
    ('Cashback reward',            7,  10,    22.00, 'Income',        'Rewards'),
    ('Freelance consulting',      10,  14,   550.00, 'Income',        'Freelance'),
    ('Refund: returned jacket',   13,  11,    78.00, 'Refund',        'Return'),
    ('Interest payment',          25,   6,    12.00, 'Income',        'Interest'),
    ('ACME Corp payroll',         26,   6,  2150.00, 'Income',        'Payroll'),

    # ── Housing ──────────────────────────────────────────────────────────
    ('Mortgage payment',           1,   7, -1900.00, 'Housing',       'Mortgage'),
    ('Home insurance',             5,   9,  -145.00, 'Housing',       'Insurance'),
    ('PG&E electricity',          10,   9,   -95.00, 'Housing',       'Utilities'),
    ('Water & sewage',            15,  10,   -50.00, 'Housing',       'Utilities'),
    ('Comcast internet',          20,   9,   -80.00, 'Housing',       'Utilities'),

    # ── Food / Groceries ─────────────────────────────────────────────────
    ('Whole Foods Market',         3,  17,  -115.00, 'Food',          'Groceries'),
    ("Trader Joe's",              11,  16,   -70.00, 'Food',          'Groceries'),
    ('Safeway',                   18,  18,   -42.00, 'Food',          'Groceries'),

    # ── Food / Dining ─────────────────────────────────────────────────────
    ('Golden Gate Grill',          2,  19,   -65.00, 'Food',          'Dining'),
    ('Slice Pizza Co',             8,  20,   -28.00, 'Food',          'Dining'),
    ('DoorDash dinner',           14,  19,   -42.00, 'Food',          'Dining'),

    # ── Food / Drinks ─────────────────────────────────────────────────────
    ('Blue Bottle Coffee',         4,   8,    -8.50, 'Food',          'Drinks'),
    ('Sightglass Coffee',          9,   8,    -7.50, 'Food',          'Drinks'),
    ('Bar Agricole',              16,  21,   -58.00, 'Food',          'Drinks'),

    # ── Transport ─────────────────────────────────────────────────────────
    ('Uber Eats — Thai Kitchen',   3,  19,   -34.50, 'Transport',      None),
    ('Auto loan payment',          1,   8,  -350.00, 'Transport',     'Auto Loan'),
    ('Auto insurance',             5,   9,  -125.00, 'Transport',     'Insurance'),
    ('Firestone — brake repair',  12,  10,  -185.00, 'Transport',     'Repairs'),
    ('Shell gas station',         20,  15,   -52.00, 'Transport',     'Gas'),

    # ── Shopping ─────────────────────────────────────────────────────────
    ('Amazon order',               4,  12,   -88.00, 'Shopping',      'Online'),
    ('Target',                    11,  14,   -52.00, 'Shopping',      'Retail'),
    ('H&M clothing',              17,  13,   -62.00, 'Shopping',      'Clothing'),

    # ── Subscriptions ─────────────────────────────────────────────────────
    ('Netflix monthly',            6,   9,   -22.00, 'Subscriptions', 'Streaming'),
    ('Spotify Premium',            8,   9,   -12.00, 'Subscriptions', 'Music'),
    ('Adobe Creative Cloud',      15,   9,   -55.00, 'Subscriptions', 'Software'),
    ('iCloud storage',            15,   9,    -4.00, 'Subscriptions', 'Software'),
    ('T-Mobile phone',            21,   9,   -55.00, 'Subscriptions', 'Phone'),
    ('Amazon Prime',              22,   9,   -17.00, 'Subscriptions', 'Online'),

    # ── Health ────────────────────────────────────────────────────────────
    ('Dentist copay',             19,  10,   -35.00, 'Health',        'Dental'),
    ('Planet Fitness',            15,  17,   -25.00, 'Health',        'Fitness'),
]


def seed(only_if_empty: bool = False) -> None:
    today = datetime.now().date()
    with app.app_context():
        if only_if_empty and Transaction.query.count() > 0:
            print("DB already has data, skipping seed.")
            return
        Transaction.query.delete()
        for description, days_ago, hour, amount, category, subcategory in SEED_TRANSACTIONS:
            db.session.add(Transaction(
                date=today - timedelta(days=days_ago),
                time=time(hour=hour, minute=(days_ago * 7) % 60),
                description=description,
                amount=amount,
                category=category,
                subcategory=subcategory,
            ))
        db.session.commit()
        count = Transaction.query.count()
        balance = sum(txn.amount for txn in Transaction.query.all())
        print(f"Seeded {count} transactions, balance ${balance:.2f}")


if __name__ == '__main__':
    import sys
    only_if_empty = '--if-empty' in sys.argv
    seed(only_if_empty=only_if_empty)
