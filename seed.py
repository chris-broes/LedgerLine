"""Seed the ledger with a realistic month of demo transactions.

Usage: SECRET_KEY=dev python seed.py
Replaces any existing transactions so reseeding is idempotent.
"""

from datetime import datetime, time, timedelta

from app import app, db, Transaction

# (description, days_ago, hour, amount, category, subcategory)
# Negative = purchase; positive = income/credit.
SEED_TRANSACTIONS = [
    ('Monthly rent',                1,  1, -1850.00, 'Housing',       'Rent'),
    ('Uber trip downtown',          1, 18,   -18.50, 'Transport',     'Rideshare'),
    ('Blue Bottle Coffee',          2,  8,    -6.50, 'Dining',        'Coffee'),
    ('Whole Foods Market',          3, 17,   -86.42, 'Groceries',     'Supermarket'),
    ('Amazon order',                4, 12,   -67.84, 'Shopping',      'Online'),
    ('Golden Gate Grill',           5, 19,   -48.75, 'Dining',        'Restaurant'),
    ('Netflix monthly',             6,  9,   -15.99, 'Subscriptions', 'Streaming'),
    ('Cashback reward',             7, 10,    12.30, 'Income',        'Rewards'),
    ('Spotify Premium',             8,  9,   -11.99, 'Subscriptions', 'Music'),
    ('Slice Pizza Co',              9, 20,   -21.40, 'Dining',        'Restaurant'),
    ("Trader Joe's",               10, 16,   -54.17, 'Groceries',     'Supermarket'),
    ('Target',                     11, 14,   -39.99, 'Shopping',      'Retail'),
    ('ACME Corp payroll',          12,  6,  1450.00, 'Income',        'Payroll'),
    ('DoorDash dinner',            12, 19,   -32.18, 'Dining',        'Delivery'),
    ('Refund: returned headphones', 13, 11,   59.99, 'Refund',        'Return'),
    ('BART transit pass',          14,  7,   -64.00, 'Transport',     'Transit'),
    ('iCloud storage',             15,  9,    -2.99, 'Subscriptions', 'Software'),
    ('PG&E electricity',           16,  9,   -72.00, 'Housing',       'Utilities'),
    ('Freelance consulting',       17, 14,   650.00, 'Income',        'Freelance'),
    ('Safeway',                    17, 18,   -33.08, 'Groceries',     'Supermarket'),
    ('Dentist copay',              19, 10,   -25.00, 'Health',        'Dental'),
    ('Shell gas station',          20, 15,   -41.25, 'Transport',     'Gas'),
    ('T-Mobile phone',             21,  9,   -45.00, 'Subscriptions', 'Phone'),
    ('Comcast internet',           22,  9,   -65.00, 'Housing',       'Internet'),
    ('Prime membership',           23,  9,   -14.99, 'Subscriptions', 'Online'),
    ('Interest payment',           25,  6,     4.21, 'Income',        'Interest'),
    ('ACME Corp payroll',          26,  6,  1450.00, 'Income',        'Payroll'),
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
