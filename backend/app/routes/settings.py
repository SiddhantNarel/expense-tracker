from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.database import get_connection

settings_bp = Blueprint('settings', __name__)


@settings_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    conn = get_connection()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return jsonify({r['key']: r['value'] for r in rows})


@settings_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    data = request.get_json() or {}
    conn = get_connection()
    for key, value in data.items():
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, str(value))
        )
    conn.commit()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return jsonify({r['key']: r['value'] for r in rows})
