#!/usr/bin/python3

from flask import Blueprint, request, jsonify
from bson import ObjectId
from models.user import User
from utils.jwt_helper import generate_token


auth_routes = Blueprint('auth_routes', __name__)


def json_serializable(user):
    if '_id' in user:
        user['_id'] = str(user['_id'])
    return user


@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Received data:", data)
    if User.find_by_email(data['email']):
        return jsonify({"message": "User already exists"}), 400
    try:
        user = User.register(data['email'], data['password'])
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.find_by_email(data['email'])
    if not user or not User.verify_password(
        data['password'],
        user['password']
    ):
        return jsonify({"message": "Invalid credentials"}), 401
    token = generate_token(user['_id'])
    return jsonify({'message': 'Login successful'}), 200
