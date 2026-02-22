import csv
import io
from flask import Blueprint, request, Response
from app.database import get_connection

export_bp = Blueprint('export', __name__)


def _csv_response(filename, headers, rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


@export_bp.route('/export/expenses', methods=['GET'])
def export_expenses():
    date_from = request.args.get('from', '2000-01-01')
    date_to = request.args.get('to', '2999-12-31')
    conn = get_connection()
    rows = conn.execute(
        "SELECT e.id, e.date, e.amount, cat.name as category, e.description, e.payment_method "
        "FROM expenses e LEFT JOIN categories cat ON e.category_id=cat.id "
        "WHERE e.date>=? AND e.date<=? ORDER BY e.date DESC",
        (date_from, date_to)
    ).fetchall()
    conn.close()
    return _csv_response(
        'expenses.csv',
        ['ID', 'Date', 'Amount (INR)', 'Category', 'Description', 'Payment Method'],
        [(r['id'], r['date'], r['amount'], r['category'], r['description'], r['payment_method']) for r in rows]
    )


@export_bp.route('/export/income', methods=['GET'])
def export_income():
    date_from = request.args.get('from', '2000-01-01')
    date_to = request.args.get('to', '2999-12-31')
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, date, amount, source, description FROM income WHERE date>=? AND date<=? ORDER BY date DESC",
        (date_from, date_to)
    ).fetchall()
    conn.close()
    return _csv_response(
        'income.csv',
        ['ID', 'Date', 'Amount (INR)', 'Source', 'Description'],
        [(r['id'], r['date'], r['amount'], r['source'], r['description']) for r in rows]
    )


@export_bp.route('/export/loans', methods=['GET'])
def export_loans():
    conn = get_connection()
    rows = conn.execute(
        "SELECT f.name as friend, lt.type, lt.amount, lt.date, lt.description "
        "FROM loan_transactions lt JOIN friends f ON lt.friend_id=f.id ORDER BY lt.date DESC"
    ).fetchall()
    conn.close()
    return _csv_response(
        'loans.csv',
        ['Friend', 'Type', 'Amount (INR)', 'Date', 'Description'],
        [(r['friend'], r['type'], r['amount'], r['date'], r['description']) for r in rows]
    )


@export_bp.route('/export/report', methods=['GET'])
def export_report():
    date_from = request.args.get('from', '2000-01-01')
    date_to = request.args.get('to', '2999-12-31')
    conn = get_connection()

    total_expense = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM expenses WHERE date>=? AND date<=?", (date_from, date_to)
    ).fetchone()[0]
    total_income = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM income WHERE date>=? AND date<=?", (date_from, date_to)
    ).fetchone()[0]
    cat_rows = conn.execute(
        "SELECT cat.name, COALESCE(SUM(e.amount),0) as total FROM categories cat "
        "LEFT JOIN expenses e ON e.category_id=cat.id AND e.date>=? AND e.date<=? "
        "GROUP BY cat.id ORDER BY total DESC",
        (date_from, date_to)
    ).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Report Period', f'{date_from} to {date_to}'])
    writer.writerow(['Total Income (INR)', total_income])
    writer.writerow(['Total Expenses (INR)', total_expense])
    writer.writerow(['Net Savings (INR)', total_income - total_expense])
    writer.writerow([])
    writer.writerow(['Category Breakdown'])
    writer.writerow(['Category', 'Amount (INR)'])
    for r in cat_rows:
        writer.writerow([r['name'], r['total']])

    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=report.csv'}
    )
