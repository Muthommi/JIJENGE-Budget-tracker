#!/usr/bin/python3

import sys
import os
import pytest
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from models.user import User


def test_register_user(client):
    User.delete_by_email('login@example.com')

    response = client.post('/api/auth/register', json={
        'email': 'login@example.com',
        'password': 'securepassword'
    })
    response_data = response.data.decode('utf-8')
    response_json = json.loads(response_data)
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'


def test_register_existing_user(client):
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    response_data = response.data.decode('utf-8')
    response_json = json.loads(response_data)
    assert response.status_code == 400
    assert response.json['message'] == 'User already exists'


def test_login_success(client):
    User.collection.delete_many({})
    register_response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    assert register_response.status_code == 201

    login_response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'securepassword'
    })
    assert login_response.status_code == 200


def test_login_failure(client):
    response = client.post('/api/auth/login', json={
        'email': 'wrongexample.com',
        'password': 'wrongpassword'
    })
    response_data = response.data.decode('utf-8')
    response_json = json.loads(response_data)
    assert response.status_code == 401
    assert response.json['message'] == 'Invalid credentials'
