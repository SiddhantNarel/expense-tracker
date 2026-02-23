import os
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '')
    password = data.get('password', '')

    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH', '')

    if not admin_password_hash:
        return jsonify({'error': 'Authentication service unavailable'}), 500

    if username != admin_username or not check_password_hash(admin_password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_access_token(identity=username)
    return jsonify({'access_token': token})


@auth_bp.route('/auth/verify', methods=['GET'])
@jwt_required()
def verify():
    return jsonify({'valid': True, 'user': get_jwt_identity()})
