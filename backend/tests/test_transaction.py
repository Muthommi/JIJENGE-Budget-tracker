#!/usr/bin/python3

import pytest
from datetime import datetime
from models.transaction import Transaction
from utils.database import transactions_collection


@pytest.fixture
def transaction_data():
    return {
        "user_id": "12345",
        "amount": 1000,
        "category": "Food",
        "description": "Grocery shopping"
    }


@pytest.fixture(autouse=True)
def clear_transactions_collection():
    transactions_collection.delete_many({})


def test_add_transaction(transaction_data):
    transaction = Transaction.add_transaction(**transaction_data)
    assert transaction["user_id"] == transaction_data["user_id"]
    assert transaction["amount"] == transaction_data["amount"]
    assert transaction["category"] == transaction_data["category"]
    assert transaction["description"] == transaction_data["description"]
    assert isinstance(transaction["date"], datetime)


def test_get_transactions_by_user(transaction_data):
    Transaction.add_transaction(**transaction_data)
    transactions = Transaction.get_transactions_by_user(transaction_data["user_id"])
    assert len(transactions) == 1
    assert transactions[0]["user_id"] == transaction_data["user_id"]


def test_get_monthly_summary(transaction_data):
    Transaction.add_transaction(**transaction_data)
    summary = Transaction.get_monthly_summary(transaction_data["user_id"], datetime.utcnow().month, datetime.utcnow().year)
    assert len(summary) == 1
    assert summary[0]["_id"] == transaction_data["category"]
    assert summary[0]["total"] == transaction_data["amount"]
