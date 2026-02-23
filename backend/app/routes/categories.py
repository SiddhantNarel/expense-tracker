from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import get_connection

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/categories', methods=['GET'])
@jwt_required()
def list_categories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM categories ORDER BY is_custom, name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@categories_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO categories (name, emoji, color, is_custom) VALUES (?,?,?,1)",
        (name, data.get('emoji', ''), data.get('color', '#6366f1'))
    )
    conn.commit()
    row = conn.execute("SELECT * FROM categories WHERE id=?", (c.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


@categories_bp.route('/categories/<int:cat_id>', methods=['PUT'])
@jwt_required()
def update_category(cat_id):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM categories WHERE id=?", (cat_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json() or {}
    conn.execute(
        "UPDATE categories SET name=?, emoji=?, color=? WHERE id=?",
        (data.get('name', existing['name']), data.get('emoji', existing['emoji']),
         data.get('color', existing['color']), cat_id)
    )
    conn.commit()
    row = conn.execute("SELECT * FROM categories WHERE id=?", (cat_id,)).fetchone()
    conn.close()
    return jsonify(dict(row))


@categories_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
@jwt_required()
def delete_category(cat_id):
    conn = get_connection()
    existing = conn.execute("SELECT * FROM categories WHERE id=?", (cat_id,)).fetchone()
    if not existing:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    if not existing['is_custom']:
        conn.close()
        return jsonify({'error': 'Cannot delete built-in categories'}), 400
    conn.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})
