#!/usr/bin/python3

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.transaction import Transaction
from bson import ObjectId
from datetime import datetime

summary_routes = Blueprint('summary_routes', __name__)


def json_serializable(data):
    if isinstance(data, list):
        return [json_serializable(item) for item in data]
    if isinstance(data, dict):
        return {key: json_serializable(value) for key, value in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    if isinstance(data, datetime):
        return data.isoformat()
    return data


@summary_routes.route('/summary', methods=['GET'])
@jwt_required()
def get_monthly_summary():
    user_id = get_jwt_identity()
    month = int(request.args.get('month'))
    year = int(request.args.get('year'))
    print(f"User ID: {user_id}, Month: {month}, Year: {year}")
    summary = Transaction.get_monthly_summary(user_id, month, year)
    print(f"Summary: {summary}")
    summary = json_serializable(summary)
    return jsonify(summary), 200
