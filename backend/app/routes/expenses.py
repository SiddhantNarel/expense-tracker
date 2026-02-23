from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import get_connection
from app.utils.validators import validate_amount, validate_date, validate_payment_method

expenses_bp = Blueprint('expenses', __name__)


def row_to_dict(row):
    return dict(row) if row else None


@expenses_bp.route('/expenses', methods=['GET'])
@jwt_required()
def list_expenses():
    conn = get_connection()
    c = conn.cursor()

    query = """
        SELECT e.*, cat.name as category_name, cat.emoji as category_emoji, cat.color as category_color
        FROM expenses e
        LEFT JOIN categories cat ON e.category_id = cat.id
        WHERE 1=1
    """
    params = []

    date_from = request.args.get('from')
    date_to = request.args.get('to')
    category_id = request.args.get('category_id')
    payment_method = request.args.get('payment_method')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    if date_from:
        query += " AND e.date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND e.date <= ?"
        params.append(date_to)
    if category_id:
        query += " AND e.category_id = ?"
        params.append(category_id)
    if payment_method:
        query += " AND e.payment_method = ?"
        params.append(payment_method)
    if search:
        query += " AND e.description LIKE ?"
        params.append(f'%{search}%')

    sort_col = 'e.date' if sort_by == 'date' else 'e.amount'
    order = 'DESC' if sort_order == 'desc' else 'ASC'
    query += f" ORDER BY {sort_col} {order}"

    count_query = f"SELECT COUNT(*) FROM ({query})"
    total = c.execute(count_query, params).fetchone()[0]

    query += " LIMIT ? OFFSET ?"
    params += [per_page, (page - 1) * per_page]

    rows = c.execute(query, params).fetchall()
    conn.close()

    return jsonify({
        'data': [dict(r) for r in rows],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    })


@expenses_bp.route('/expenses/<int:expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT e.*, cat.name as category_name, cat.emoji as category_emoji "
        "FROM expenses e LEFT JOIN categories cat ON e.category_id=cat.id WHERE e.id=?",
        (expense_id,)
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dict(row))


@expenses_bp.route('/expenses', methods=['POST'])
@jwt_required()
def create_expense():
    data = request.get_json() or {}
    amount, err = validate_amount(data.get('amount'))
    if err:
        return jsonify({'error': err}), 400
    date, err = validate_date(data.get('date'))
    if err:
        return jsonify({'error': err}), 400
    payment_method = data.get('payment_method', 'Cash')
    pm, err = validate_payment_method(payment_method)
    if err:
        return jsonify({'error': err}), 400

    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO expenses (amount, category_id, date, description, payment_method) VALUES (?,?,?,?,?)",
        (amount, data.get('category_id'), date, data.get('description', ''), pm)
    )
    conn.commit()
    row = conn.execute(
        "SELECT e.*, cat.name as category_name, cat.emoji as category_emoji "
        "FROM expenses e LEFT JOIN categories cat ON e.category_id=cat.id WHERE e.id=?",
        (c.lastrowid,)
    ).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@expenses_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM expenses WHERE id=?", (expense_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json() or {}
    amount = existing['amount']
    date = existing['date']
    payment_method = existing['payment_method']

    if 'amount' in data:
        amount, err = validate_amount(data['amount'])
        if err:
            conn.close()
            return jsonify({'error': err}), 400
    if 'date' in data:
        date, err = validate_date(data['date'])
        if err:
            conn.close()
            return jsonify({'error': err}), 400
    if 'payment_method' in data:
        payment_method, err = validate_payment_method(data['payment_method'])
        if err:
            conn.close()
            return jsonify({'error': err}), 400

    conn.execute(
        "UPDATE expenses SET amount=?, category_id=?, date=?, description=?, payment_method=?, updated_at=datetime('now') WHERE id=?",
        (amount, data.get('category_id', existing['category_id']), date,
         data.get('description', existing['description']), payment_method, expense_id)
    )
    conn.commit()
    row = conn.execute(
        "SELECT e.*, cat.name as category_name, cat.emoji as category_emoji "
        "FROM expenses e LEFT JOIN categories cat ON e.category_id=cat.id WHERE e.id=?",
        (expense_id,)
    ).fetchone()
    conn.close()
    return jsonify(dict(row))


@expenses_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM expenses WHERE id=?", (expense_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    conn.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})
