#!/usr/bin/python3

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from models.transaction import Transaction

transaction_routes = Blueprint('transaction_routes', __name__)


def json_serializable(data):
    if isinstance(data, list):
        return [json_serializable(item) for item in data]
    if isinstance(data, dict):
        return {key: json_serializable(value) for key, value in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data


@transaction_routes.route('/transactions', methods=['POST'])
@jwt_required()
def add_transaction():
    data = request.json
    user_id = get_jwt_identity()
    data['user_id'] = user_id
    transaction = Transaction.create(data)
    transaction = json_serializable(transaction)
    return jsonify(transaction), 201


@transaction_routes.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    transactions = Transaction.get_transactions_by_user(user_id)
    return jsonify(transactions), 200
