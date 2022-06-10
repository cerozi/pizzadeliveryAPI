from fastapi.testclient import TestClient
from src.databases_test import override_get_db
from databases import get_db
from main import app

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_creates_user():
    data = {
        'username': 'test',
        'email': 'test',
        'password': 'test'
    }

    response = client.post('/auth/signup', json=data)
    assert response.status_code == 201
    assert response.json()['username'] == 'test'

def test_login():
    data = {
        'username': 'test',
        'password': 'test'
    }
    response = client.post('/auth/login', json=data)
    assert response.status_code == 200
    assert list(response.json().keys()) == ['access_token', 'refresh_token']

