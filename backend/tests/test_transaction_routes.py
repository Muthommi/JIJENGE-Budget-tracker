#!/usr/bin/python3
import unittest
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from routes.transaction_routes import transaction_routes
from app import app
from models.transaction import Transaction


class TestTransactionRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'test-key'
        self.app.config['TESTING'] = True

        self.jwt = JWTManager(self.app)

        self.app.register_blueprint(transaction_routes)

        self.client = self.app.test_client()
        self.headers = {
            'Content-Type': 'application/json'
        }

        with self.app.app_context():
            self.access_token = create_access_token(identity=1)
            self.headers['Authorization'] = f'Bearer {self.access_token}'

    def tearDown(self):
        pass

    def test_add_transaction(self):
        original_create = Transaction.create
        Transaction.create = lambda data: {
                'id': '123',
                'user_id': data['user_id'],
                'amount': data['amount'],
                'category': data['category'],
                'description': data['description']
        }

        data = {
            'amount': 100.50,
            'category': 'Groceries',
            'description': 'Weekly shopping'
        }

        try:
            response = self.client.post(
                    '/transactions',
                    json=data,
                    headers=self.headers
            )
            self.assertEqual(response.status_code, 201)
            self.assertIn('id', response.json)
            self.assertEqual(response.json['amount'], 100.50)
            self.assertEqual(response.json['category'], 'Groceries')
            self.assertEqual(response.json['description'], 'Weekly shopping')
        finally:
            Transaction.create = original_create


    def test_get_transactions(self):
        mock_transactions = [
            {
                'id': 1,
                'user_id': 1,
                'amount': 100.50,
                'category': 'Groceries',
                'description': 'Weekly shopping',
                'timestamp': '2025-01-01T12:00:00'
            }
        ]

        original_get_transactions = Transaction.get_transactions_by_user

        Transaction.get_transactions_by_user = lambda user_id: mock_transactions

        try:
            response = self.client.get(
                    '/transactions',
                    headers=self.headers
            )
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)
            self.assertEqual(len(response.json), 1)
            self.assertEqual(response.json[0]['amount'], 100.50)
            self.assertEqual(response.json[0]['category'], 'Groceries')
            self.assertEqual(response.json[0]['description'], 'Weekly shopping')
        finally:
            Transaction.get_transactions_by_user = original_get_transactions


if __name__ == '__main__':
    unittest.main()
