from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime, date
import os
import re
import logging
import requests
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from categorize import categorize
from config import config_by_name

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config_by_name[os.environ.get('FLASK_ENV', 'development')])

if not app.config.get('SECRET_KEY'):
    raise RuntimeError(
        "SECRET_KEY is not set. Define the SECRET_KEY environment variable "
        "before starting the app in this environment."
    )

db = SQLAlchemy(app)
migrate = Migrate(app, db)

RECOMMENDATIONS_URL = os.environ.get('RECOMMENDATIONS_URL', 'http://127.0.0.1:8002')

CATEGORY_COLORS: dict[str, str] = {
    'Housing':       '#0ea5e9',
    'Dining':        '#ef4444',
    'Groceries':     '#f97316',
    'Transport':     '#3b82f6',
    'Subscriptions': '#8b5cf6',
    'Shopping':      '#ec4899',
    'Health':        '#f43f5e',
    'Refund':        '#10b981',
    'Income':        '#22c55e',
    'Other':         '#6b7280',
}

CATEGORIES = [
    ('Auto', 'Auto-detect from description'),
    ('Housing', 'Housing'),
    ('Dining', 'Dining'),
    ('Groceries', 'Groceries'),
    ('Transport', 'Transport'),
    ('Subscriptions', 'Subscriptions'),
    ('Shopping', 'Shopping'),
    ('Health', 'Health'),
    ('Refund', 'Refund'),
    ('Income', 'Income'),
    ('Other', 'Other'),
]


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(40), nullable=False)
    subcategory = db.Column(db.String(40), nullable=True)


class TransactionForm(FlaskForm):
    description = StringField(
        'Description',
        validators=[DataRequired(), Length(max=200)],
    )
    amount = StringField(
        'Amount (USD — purchases negative, income/credits positive, e.g. -24.99 or 1450.00)',
        validators=[DataRequired(), Length(max=20)],
    )
    category = SelectField('Category', choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField('Post Transaction')


def _parse_amount(value: str) -> Optional[float]:
    match = re.search(r"\d+(?:\.\d+)?", value)
    if not match:
        return None
    return float(match.group(0))


@app.route('/health')
def health():
    try:
        db.session.execute(text('SELECT 1'))
    except SQLAlchemyError as exc:
        logger.error("Health check database probe failed: %s", exc)
        return jsonify(status='error', database='unavailable'), 503
    return jsonify(status='ok', database='ok')


@app.route('/')
def index():
    transactions = Transaction.query.order_by(
        Transaction.date.desc(), Transaction.time.desc()
    ).all()
    profile = _spending_profile(transactions)
    spend_total = sum(profile['category_totals'].values())
    categories = sorted(
        profile['category_totals'].items(), key=lambda item: item[1], reverse=True,
    )
    cashflow = _monthly_cashflow(transactions)
    return render_template(
        'index.html',
        transactions=transactions,
        balance=profile['balance'],
        categories=categories,
        spend_total=spend_total,
        recommendations=_fetch_recommendations(profile),
        chart=_balance_chart(transactions),
        sankey=_sankey_chart(transactions, categories, spend_total),
        monthly_income=cashflow['income'],
        monthly_expenses=cashflow['expenses'],
        category_colors=CATEGORY_COLORS,
    )


def _spending_profile(transactions: list['Transaction']) -> dict:
    category_totals: dict[str, float] = {}
    for txn in transactions:
        if txn.amount < 0:
            category_totals[txn.category] = category_totals.get(txn.category, 0.0) - txn.amount
    return {
        'balance': sum(txn.amount for txn in transactions),
        'category_totals': category_totals,
        'subscription_count': sum(1 for txn in transactions if txn.category == 'Subscriptions'),
    }


def _bb(lx: float, ly1: float, ly2: float, rx: float, ry1: float, ry2: float) -> str:
    """Smooth bezier band SVG path from left edge (ly1..ly2) to right edge (ry1..ry2)."""
    cx1 = lx + (rx - lx) * 0.42
    cx2 = rx - (rx - lx) * 0.42
    return (
        f"M {lx:.1f} {ly1:.1f} "
        f"C {cx1:.1f} {ly1:.1f} {cx2:.1f} {ry1:.1f} {rx:.1f} {ry1:.1f} "
        f"L {rx:.1f} {ry2:.1f} "
        f"C {cx2:.1f} {ry2:.1f} {cx1:.1f} {ly2:.1f} {lx:.1f} {ly2:.1f} Z"
    )


def _sankey_chart(
    transactions: list['Transaction'],
    categories: list[tuple],
    spend_total: float,
) -> Optional[dict]:
    """3-column Monarch-style cash-flow Sankey.

    Col 0  Income sources (Payroll / Freelance / Other)
    Col 1  Income aggregate node
    Col 2  Savings + spending categories
    """
    income_total = sum(t.amount for t in transactions if t.amount > 0)
    if income_total <= 0 or spend_total <= 0:
        return None

    # ── layout constants ──────────────────────────────────────────────────
    H = 380.0          # pixel height = total income
    PAD = 20.0         # top/bottom padding
    NW = 18            # node width (px)
    GAP = 10           # gap between col-2 nodes (px)
    GAP_SAVE = 16      # larger gap after Savings node
    ppu = H / income_total  # pixels-per-dollar

    col0_x = 145       # income source nodes (left edge)
    col1_x = 335       # income aggregate node (left edge)
    col2_x = 560       # savings + categories (left edge)
    vw = 870           # total SVG viewBox width (room for right labels)

    # ── income sources (col 0) ────────────────────────────────────────────
    src: dict[str, float] = {}
    for t in transactions:
        if t.amount <= 0:
            continue
        key = t.subcategory if t.subcategory and t.category == 'Income' else t.category
        if key in ('Refund', 'Income'):
            key = t.subcategory or 'Other Income'
        src[key] = src.get(key, 0.0) + t.amount

    ORDER = ['Payroll', 'Freelance']
    sources = [(k, src[k]) for k in ORDER if k in src]
    others = sum(v for k, v in src.items() if k not in ORDER)
    if others > 0:
        sources.append(('Other Income', others))

    src_colors = {'Payroll': '#22c55e', 'Freelance': '#10b981', 'Other Income': '#6ee7b7'}

    col0: list[dict] = []
    y = PAD
    for name, amt in sources:
        h = amt * ppu
        col0.append({'name': name, 'y': y, 'h': h, 'mid': y + h / 2,
                     'color': src_colors.get(name, '#22c55e'), 'amount': amt})
        y += h

    # ── income node (col 1) ───────────────────────────────────────────────
    col1 = {'y': PAD, 'h': H, 'mid': PAD + H / 2}

    # ── savings + categories (col 2) ─────────────────────────────────────
    savings = income_total - spend_total
    col2_items: list[tuple] = []
    if savings > 0:
        col2_items.append(('Savings', savings, '#22c55e', True))
    for name, amt in categories:
        col2_items.append((name, amt, CATEGORY_COLORS.get(name, '#6b7280'), False))

    col2: list[dict] = []
    y_rect = PAD
    y_flow = PAD          # tracks proportional position on col1 right edge
    for name, amt, color, is_savings in col2_items:
        h = amt * ppu
        pct = round(amt / income_total * 100, 1)
        col2.append({
            'name': name, 'amount': amt, 'color': color,
            'y_rect': y_rect, 'h': h, 'mid': y_rect + h / 2,
            'y_flow': y_flow, 'pct': pct,
        })
        y_rect += h + (GAP_SAVE if is_savings else GAP)
        y_flow += h

    # ── flows col0 → col1 ─────────────────────────────────────────────────
    flows_01: list[dict] = []
    y_col1_in = PAD
    for s in col0:
        path = _bb(col0_x + NW, s['y'], s['y'] + s['h'],
                   col1_x, y_col1_in, y_col1_in + s['h'])
        flows_01.append({'path': path, 'color': s['color'], 'name': s['name']})
        y_col1_in += s['h']

    # ── flows col1 → col2 ─────────────────────────────────────────────────
    flows_12: list[dict] = []
    for c2 in col2:
        path = _bb(col1_x + NW, c2['y_flow'], c2['y_flow'] + c2['h'],
                   col2_x, c2['y_rect'], c2['y_rect'] + c2['h'])
        flows_12.append({'path': path, 'color': c2['color']})

    # ── total SVG height ──────────────────────────────────────────────────
    max_y = max(
        col0[-1]['y'] + col0[-1]['h'],
        col1['y'] + col1['h'],
        col2[-1]['y_rect'] + col2[-1]['h'],
    ) + PAD if col0 and col2 else H + 2 * PAD

    return {
        'col0': col0, 'col1': col1, 'col2': col2,
        'flows_01': flows_01, 'flows_12': flows_12,
        'col0_x': col0_x, 'col1_x': col1_x, 'col2_x': col2_x,
        'nw': NW, 'vw': vw, 'vh': round(max_y),
        'income_total': income_total,
    }


def _monthly_cashflow(transactions: list['Transaction']) -> dict:
    today = date.today()
    monthly = [t for t in transactions if t.date.year == today.year and t.date.month == today.month]
    income = sum(t.amount for t in monthly if t.amount > 0)
    expenses = abs(sum(t.amount for t in monthly if t.amount < 0))
    return {'income': income, 'expenses': expenses}


def _balance_chart(transactions: list['Transaction']) -> Optional[dict]:
    ordered = sorted(transactions, key=lambda txn: (txn.date, txn.time))
    if len(ordered) < 2:
        return None

    series: list[tuple] = []
    running = 0.0
    for txn in ordered:
        running += txn.amount
        series.append((txn.date, running))

    width, height, pad = 640, 65, 6
    values = [value for _, value in series]
    low = min(min(values), 0.0)
    high = max(max(values), 0.0)
    span = (high - low) or 1.0
    last_index = len(series) - 1

    points = []
    for i, (_, value) in enumerate(series):
        x = pad + i * (width - 2 * pad) / last_index
        y = height - pad - (value - low) * (height - 2 * pad) / span
        points.append(f"{x:.1f},{y:.1f}")

    zero_y = height - pad - (0.0 - low) * (height - 2 * pad) / span
    return {
        'points': ' '.join(points),
        'zero_y': round(zero_y, 1),
        'low': low,
        'high': high,
        'start': series[0][0],
        'end': series[-1][0],
    }


def _fetch_recommendations(profile: dict) -> Optional[list[dict]]:
    try:
        response = requests.post(
            f"{RECOMMENDATIONS_URL}/recommendations", json=profile, timeout=3,
        )
        response.raise_for_status()
        return response.json().get('recommendations', [])
    except (requests.RequestException, ValueError) as exc:
        logger.warning("Recommendations service unavailable: %s", exc)
        return None


@app.route('/coming-soon')
def coming_soon():
    page = request.args.get('page', 'This feature')
    return render_template('coming_soon.html', page=page)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = TransactionForm()
    if form.validate_on_submit():
        amount = _parse_amount(form.amount.data)
        if amount is None:
            return "Invalid amount", 400

        category = form.category.data
        if category == 'Auto':
            category = categorize(form.description.data)

        now = datetime.now()
        txn = Transaction(
            date=now.date(),
            time=now.time(),
            description=form.description.data,
            amount=amount,
            category=category,
        )
        try:
            db.session.add(txn)
            db.session.commit()
        except SQLAlchemyError as exc:
            db.session.rollback()
            logger.error("Failed to save transaction: %s", exc)
            return "Failed to save transaction", 500
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False))
