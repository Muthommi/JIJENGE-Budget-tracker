#!/usr/bin/python3

from flask_jwt_extended import create_access_token
from datetime import datetime
from app import app
from models.transaction import Transaction
from utils.database import transactions_collection


def test_get_monthly_summary(client):
    transactions_collection.delete_many({})

    user_id = 'test_user'

    with app.app_context():
        token = create_access_token(identity=user_id)

    transactions = [
        {
            'amount': 500,
            'category': 'Salary',
            'description': 'Monthly salary',
            'user_id': user_id,
            'date': datetime.utcnow()
        },
        {
            'amount': 200,
            'category': 'Groceries',
            'description': 'Grocery shopping',
            'user_id': user_id,
            'date': datetime.utcnow(),
        }
    ]

    for transaction in transactions:
        response = client.post('/api/transactions',
                json=transaction,
                headers={'Authorization': f'Bearer {token}'})
        assert response.status_code == 201

    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    response = client.get(
        f'/api/summary?month={current_month}&year={current_year}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['total'] > 0
