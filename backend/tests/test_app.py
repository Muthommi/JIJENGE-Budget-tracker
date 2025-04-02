import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Hello, Flask!"

def test_auth_routes_registered(client):
    response = client.get('/api/auth')
    assert response.status_code in [404]

def test_transaction_routes_registered(client):
    response = client.get('/api/transactions')
    assert response.status_code in [401]

def test_summary_routes_registered(client):
    response = client.get('/api/summary?month=1&year=2025', headers={'Authorization': 'Bearer YOUR_JWT_TOKEN'})
    assert response.status_code in [200]
