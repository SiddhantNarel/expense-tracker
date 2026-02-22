from flask import Blueprint, request, jsonify
from app.database import get_connection

analytics_bp = Blueprint('analytics', __name__)


def _get_date_range(request):
    date_from = request.args.get('from')
    date_to = request.args.get('to')
    if not date_from or not date_to:
        from datetime import date
        today = date.today()
        date_from = today.replace(day=1).isoformat()
        date_to = today.isoformat()
    return date_from, date_to


@analytics_bp.route('/analytics/summary', methods=['GET'])
def summary():
    date_from, date_to = _get_date_range(request)
    conn = get_connection()

    total_expense = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE date>=? AND date<=?",
        (date_from, date_to)
    ).fetchone()[0]

    total_income = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM income WHERE date>=? AND date<=?",
        (date_from, date_to)
    ).fetchone()[0]

    # Overall budget for this period
    month = int(date_from[5:7])
    year = int(date_from[:4])
    overall_budget = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM budgets WHERE category_id IS NULL AND month=? AND year=?",
        (month, year)
    ).fetchone()[0]

    conn.close()
    return jsonify({
        'total_expense': total_expense,
        'total_income': total_income,
        'net_savings': total_income - total_expense,
        'overall_budget': overall_budget,
        'budget_remaining': overall_budget - total_expense,
        'date_from': date_from,
        'date_to': date_to
    })


@analytics_bp.route('/analytics/category-breakdown', methods=['GET'])
def category_breakdown():
    date_from, date_to = _get_date_range(request)
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT cat.id, cat.name, cat.emoji, cat.color, COALESCE(SUM(e.amount),0) as total
        FROM categories cat
        LEFT JOIN expenses e ON e.category_id=cat.id AND e.date>=? AND e.date<=?
        GROUP BY cat.id
        ORDER BY total DESC
        """,
        (date_from, date_to)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@analytics_bp.route('/analytics/trends', methods=['GET'])
def trends():
    date_from, date_to = _get_date_range(request)
    group_by = request.args.get('group_by', 'day')
    conn = get_connection()

    if group_by == 'month':
        fmt = "%Y-%m"
        label = "strftime('%Y-%m', date)"
    elif group_by == 'week':
        fmt = "%Y-W%W"
        label = "strftime('%Y-W%W', date)"
    else:
        label = "date"

    rows = conn.execute(
        f"SELECT {label} as period, COALESCE(SUM(amount),0) as total FROM expenses WHERE date>=? AND date<=? GROUP BY period ORDER BY period",
        (date_from, date_to)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@analytics_bp.route('/analytics/income-vs-expense', methods=['GET'])
def income_vs_expense():
    date_from, date_to = _get_date_range(request)
    conn = get_connection()

    expense_rows = conn.execute(
        "SELECT strftime('%Y-%m', date) as month, COALESCE(SUM(amount),0) as total FROM expenses WHERE date>=? AND date<=? GROUP BY month ORDER BY month",
        (date_from, date_to)
    ).fetchall()

    income_rows = conn.execute(
        "SELECT strftime('%Y-%m', date) as month, COALESCE(SUM(amount),0) as total FROM income WHERE date>=? AND date<=? GROUP BY month ORDER BY month",
        (date_from, date_to)
    ).fetchall()

    conn.close()
    return jsonify({
        'expenses': [dict(r) for r in expense_rows],
        'income': [dict(r) for r in income_rows]
    })
