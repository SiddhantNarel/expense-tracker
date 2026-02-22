from flask import Blueprint, request, jsonify
from app.database import get_connection
from app.utils.validators import validate_amount

budgets_bp = Blueprint('budgets', __name__)


@budgets_bp.route('/budgets', methods=['GET'])
def list_budgets():
    conn = get_connection()
    month = request.args.get('month')
    year = request.args.get('year')
    query = "SELECT b.*, cat.name as category_name, cat.emoji as category_emoji FROM budgets b LEFT JOIN categories cat ON b.category_id=cat.id WHERE 1=1"
    params = []
    if month:
        query += " AND b.month=?"
        params.append(int(month))
    if year:
        query += " AND b.year=?"
        params.append(int(year))
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@budgets_bp.route('/budgets', methods=['POST'])
def set_budget():
    data = request.get_json() or {}
    amount, err = validate_amount(data.get('amount'))
    if err:
        return jsonify({'error': err}), 400

    month = data.get('month')
    year = data.get('year')
    if not month or not year:
        return jsonify({'error': 'month and year are required'}), 400

    category_id = data.get('category_id')

    conn = get_connection()
    # Upsert: update if exists, else insert
    existing = conn.execute(
        "SELECT id FROM budgets WHERE category_id IS ? AND month=? AND year=?",
        (category_id, int(month), int(year))
    ).fetchone()

    if existing:
        conn.execute("UPDATE budgets SET amount=? WHERE id=?", (amount, existing['id']))
        conn.commit()
        row = conn.execute(
            "SELECT b.*, cat.name as category_name, cat.emoji as category_emoji FROM budgets b LEFT JOIN categories cat ON b.category_id=cat.id WHERE b.id=?",
            (existing['id'],)
        ).fetchone()
    else:
        c = conn.cursor()
        c.execute(
            "INSERT INTO budgets (category_id, amount, month, year) VALUES (?,?,?,?)",
            (category_id, amount, int(month), int(year))
        )
        conn.commit()
        row = conn.execute(
            "SELECT b.*, cat.name as category_name, cat.emoji as category_emoji FROM budgets b LEFT JOIN categories cat ON b.category_id=cat.id WHERE b.id=?",
            (c.lastrowid,)
        ).fetchone()

    conn.close()
    return jsonify(dict(row)), 201


@budgets_bp.route('/budgets/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM budgets WHERE id=?", (budget_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    conn.execute("DELETE FROM budgets WHERE id=?", (budget_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})
