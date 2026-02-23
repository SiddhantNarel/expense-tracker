from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import get_connection
from app.utils.validators import validate_amount, validate_date

income_bp = Blueprint('income', __name__)

INCOME_SOURCES = ['Family', 'Pocket Money', 'Freelance', 'Part-time Job', 'Stipend', 'Other']


@income_bp.route('/income', methods=['GET'])
@jwt_required()
def list_income():
    conn = get_connection()
    query = "SELECT * FROM income WHERE 1=1"
    params = []

    date_from = request.args.get('from')
    date_to = request.args.get('to')
    source = request.args.get('source')
    search = request.args.get('search')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    if date_from:
        query += " AND date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)
    if source:
        query += " AND source = ?"
        params.append(source)
    if search:
        query += " AND description LIKE ?"
        params.append(f'%{search}%')

    query += " ORDER BY date DESC"

    count_query = f"SELECT COUNT(*) FROM ({query})"
    total = conn.execute(count_query, params).fetchone()[0]

    query += " LIMIT ? OFFSET ?"
    params += [per_page, (page - 1) * per_page]

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify({
        'data': [dict(r) for r in rows],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    })


@income_bp.route('/income', methods=['POST'])
@jwt_required()
def create_income():
    data = request.get_json() or {}
    amount, err = validate_amount(data.get('amount'))
    if err:
        return jsonify({'error': err}), 400
    date, err = validate_date(data.get('date'))
    if err:
        return jsonify({'error': err}), 400
    source = data.get('source', 'Other')

    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO income (amount, source, date, description) VALUES (?,?,?,?)",
        (amount, source, date, data.get('description', ''))
    )
    conn.commit()
    row = conn.execute("SELECT * FROM income WHERE id=?", (c.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@income_bp.route('/income/<int:income_id>', methods=['PUT'])
@jwt_required()
def update_income(income_id):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM income WHERE id=?", (income_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json() or {}
    amount = existing['amount']
    date = existing['date']

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

    conn.execute(
        "UPDATE income SET amount=?, source=?, date=?, description=?, updated_at=datetime('now') WHERE id=?",
        (amount, data.get('source', existing['source']), date,
         data.get('description', existing['description']), income_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM income WHERE id=?", (income_id,)).fetchone()
    conn.close()
    return jsonify(dict(row))


@income_bp.route('/income/<int:income_id>', methods=['DELETE'])
@jwt_required()
def delete_income(income_id):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM income WHERE id=?", (income_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    conn.execute("DELETE FROM income WHERE id=?", (income_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})


@income_bp.route('/income/sources', methods=['GET'])
@jwt_required()
def get_sources():
    return jsonify(INCOME_SOURCES)
