#!/usr/bin/python3

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app import app
from utils.database import db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        with app.app_context():
            # Clearing the database
            db.users_collection.delete_many({})
            db.transactions_collection.delete_many({})
        yield client
