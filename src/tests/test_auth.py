from fastapi.testclient import TestClient
from databases_test import override_get_db
from databases import get_db
from main import app

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_creates_normal_user():
    data = {
        'username': 'test',
        'email': 'test',
        'password': 'test'
    }

    # creates user with no privileges;
    response = client.post('/auth/signup', json=data)
    assert response.status_code == 201
    assert response.json()['username'] == 'test'

    # try to creates user with the same email and username;
    response = client.post('/auth/signup', json=data)
    assert response.status_code == 400
    assert response.json()['detail'] == 'username or email already being used. '

def test_login_normal_user():
    data = {
        'username': 'test',
        'password': 'test'
    }

    # authenticates user;
    response = client.post('/auth/login', json=data)
    assert response.status_code == 200
    assert list(response.json().keys()) == ['access_token', 'refresh_token']
    
    return response.json()['access_token']

def test_creates_staff_user():
    data = {
        'username': 'admin',
        'email': 'admin',
        'password': 'admin',
        'is_staff': True
    }

    # creates user with privileges;
    response = client.post('auth/signup', json=data)
    assert response.status_code == 201
    assert response.json()['username'] == 'admin'

def test_login_staff_user():
    data = {
        'username': 'admin',
        'password': 'admin'
    }

    # authenticates user;
    response = client.post('/auth/login', json=data)
    assert response.status_code == 200
    assert list(response.json().keys()) == ['access_token', 'refresh_token']
    
    return response.json()['access_token']
