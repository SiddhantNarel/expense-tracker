from flask import Blueprint, request, jsonify
from app.database import get_connection
from app.utils.validators import validate_amount, validate_date
import datetime

loans_bp = Blueprint('loans', __name__)


def _calc_balance(friend_id, conn):
    rows = conn.execute(
        "SELECT type, amount FROM loan_transactions WHERE friend_id=?", (friend_id,)
    ).fetchall()
    balance = 0.0
    for r in rows:
        if r['type'] == 'gave':
            balance += r['amount']
        elif r['type'] in ('received', 'settlement'):
            balance -= r['amount']
    return balance


@loans_bp.route('/friends', methods=['GET'])
def list_friends():
    conn = get_connection()
    friends = conn.execute("SELECT * FROM friends ORDER BY name").fetchall()
    result = []
    for f in friends:
        balance = _calc_balance(f['id'], conn)
        last_tx = conn.execute(
            "SELECT date FROM loan_transactions WHERE friend_id=? ORDER BY date DESC LIMIT 1",
            (f['id'],)
        ).fetchone()
        d = dict(f)
        d['balance'] = balance
        d['last_transaction_date'] = last_tx['date'] if last_tx else None
        result.append(d)
    conn.close()
    return jsonify(result)


@loans_bp.route('/friends', methods=['POST'])
def create_friend():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO friends (name, phone, notes) VALUES (?,?,?)",
        (name, data.get('phone', ''), data.get('notes', ''))
    )
    conn.commit()
    row = conn.execute("SELECT * FROM friends WHERE id=?", (c.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@loans_bp.route('/friends/<int:friend_id>', methods=['PUT'])
def update_friend(friend_id):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM friends WHERE id=?", (friend_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json() or {}
    conn.execute(
        "UPDATE friends SET name=?, phone=?, notes=? WHERE id=?",
        (data.get('name', existing['name']), data.get('phone', existing['phone']),
         data.get('notes', existing['notes']), friend_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM friends WHERE id=?", (friend_id,)).fetchone()
    conn.close()
    return jsonify(dict(row))


@loans_bp.route('/friends/<int:friend_id>', methods=['DELETE'])
def delete_friend(friend_id):
    conn = get_connection()
    existing = conn.execute("SELECT id FROM friends WHERE id=?", (friend_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    conn.execute("DELETE FROM friends WHERE id=?", (friend_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})


@loans_bp.route('/friends/<int:friend_id>/transactions', methods=['GET'])
def list_transactions(friend_id):
    conn = get_connection()
    friend = conn.execute("SELECT * FROM friends WHERE id=?", (friend_id,)).fetchone()
    if not friend:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    rows = conn.execute(
        "SELECT * FROM loan_transactions WHERE friend_id=? ORDER BY date DESC, created_at DESC",
        (friend_id,)
    ).fetchall()
    balance = _calc_balance(friend_id, conn)
    conn.close()
    return jsonify({
        'friend': dict(friend),
        'transactions': [dict(r) for r in rows],
        'balance': balance
    })


@loans_bp.route('/friends/<int:friend_id>/transactions', methods=['POST'])
def add_transaction(friend_id):
    conn = get_connection()
    friend = conn.execute("SELECT id FROM friends WHERE id=?", (friend_id,)).fetchone()
    if not friend:
        conn.close()
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json() or {}
    tx_type = data.get('type')
    if tx_type not in ('gave', 'received'):
        conn.close()
        return jsonify({'error': "Type must be 'gave' or 'received'"}), 400

    amount, err = validate_amount(data.get('amount'))
    if err:
        conn.close()
        return jsonify({'error': err}), 400
    date, err = validate_date(data.get('date'))
    if err:
        conn.close()
        return jsonify({'error': err}), 400

    c = conn.cursor()
    c.execute(
        "INSERT INTO loan_transactions (friend_id, type, amount, date, description) VALUES (?,?,?,?,?)",
        (friend_id, tx_type, amount, date, data.get('description', ''))
    )
    conn.commit()
    row = conn.execute("SELECT * FROM loan_transactions WHERE id=?", (c.lastrowid,)).fetchone()
    balance = _calc_balance(friend_id, conn)
    conn.close()
    return jsonify({'transaction': dict(row), 'balance': balance}), 201


@loans_bp.route('/friends/<int:friend_id>/settle', methods=['POST'])
def settle(friend_id):
    conn = get_connection()
    friend = conn.execute("SELECT id FROM friends WHERE id=?", (friend_id,)).fetchone()
    if not friend:
        conn.close()
        return jsonify({'error': 'Not found'}), 404

    data = request.get_json() or {}
    balance = _calc_balance(friend_id, conn)

    if balance == 0:
        conn.close()
        return jsonify({'error': 'Already settled'}), 400

    # If amount provided use it, else full settlement
    amount_raw = data.get('amount')
    if amount_raw:
        amount, err = validate_amount(amount_raw)
        if err:
            conn.close()
            return jsonify({'error': err}), 400
    else:
        amount = abs(balance)

    date, err = validate_date(data.get('date', datetime.date.today().isoformat()))
    if err:
        conn.close()
        return jsonify({'error': err}), 400

    # settlement type always reduces what is owed
    c = conn.cursor()
    c.execute(
        "INSERT INTO loan_transactions (friend_id, type, amount, date, description) VALUES (?,?,?,?,?)",
        (friend_id, 'settlement', amount, date, data.get('description', 'Settlement'))
    )
    conn.commit()
    new_balance = _calc_balance(friend_id, conn)
    conn.close()
    return jsonify({'message': 'Settled', 'balance': new_balance}), 201
