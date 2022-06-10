from fastapi.testclient import TestClient
from main import app
from databases import get_db
from databases_test import override_get_db
from test_auth import test_login_normal_user, test_login_staff_user


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

user_jwt_token = test_login_normal_user()
staff_jwt_token = test_login_staff_user()

def test_create_order():
    data = {
        "quantity": 1,
        "flavour": "BACON",
        "size": "SMALL"
    }

    unvalid_data = {
        "quantity": 1,
        "flavour": "unvalid_value",
        "size": "unvalid_value"
    }

    # tests an order creation with a unvalid request body;
    response = client.post('orders/order/', json=unvalid_data, headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 422
    assert response.json()['detail'] == "invalid request data body. "

    # tests an order creation with a valid jwt token;
    response = client.post('orders/order/', json=data, headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 201
    assert response.json()['quantity'] == 1

    # tests an order creation with a fake jwt token;
    response = client.post('orders/order/', json=data, headers={'Authorization': f'Bearer fake_token'})
    assert response.status_code == 401


def test_staff_updates_order_status():
    data = {
        'order_status': "DELIVERED"
    }

    # tests an update order status with a valid staff jwt token;
    response = client.put('orders/order/update/status/1', json=data, headers={'Authorization': f'Bearer {staff_jwt_token}'})
    assert response.status_code == 202

    # tests an update order status with a valid user jwt token;
    response = client.put('orders/order/update/status/1', json=data, headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 403

    # tests an update order status without a jwt token;
    response = client.put('orders/order/update/status/1', json=data)
    assert response.status_code == 401

    # tests an update order status with a unvalid request body;
    data['order_status'] = "unvalid_status_value"
    response = client.put('orders/order/update/status/1', json=data, headers={'Authorization': f'Bearer {staff_jwt_token}'})
    assert response.status_code == 422
    assert response.json()['detail'] == "invalid request body. "

def test_staff_get_all_orders():
    # tests a GET HTTP with a valid staff jwt token;
    response = client.get('/orders/orders/', headers={'Authorization': f'Bearer {staff_jwt_token}'})
    assert response.status_code == 200

    # tests a GET HTTP with a valid user jwt token;
    response = client.get('/orders/orders/', headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 403

    # tests a GET HTTP being unauthenticated;
    response = client.get('/orders/orders/', headers={'Authorization': f'Bearer fake_token'})
    assert response.status_code == 401

def test_staff_get_specific_order():
    # tests a GET HTTP with a valid staff jwt token;
    response = client.get('/orders/orders/1', headers={'Authorization': f'Bearer {staff_jwt_token}'})
    assert response.status_code == 200

    # tests a GET HTTP with a valid user jwt token;
    response = client.get('/orders/orders/1', headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 403

    # tests a GET HTTP being unauthenticated;
    response = client.get('/orders/orders/1', headers={'Authorization': f'Bearer fake_token'})
    assert response.status_code == 401


def test_get_logged_user_all_orders():
    # tests a GET HTTP with a valid jwt token;
    response = client.get('orders/user/orders', headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 200
    assert len(response.json()) == 1

    # tests a GET HTTP with a fake jwt token;
    response = client.get('orders/user/orders', headers={'Authorization': f'Bearer fake_token'})
    assert response.status_code == 401

def test_get_logged_user_specific_order():
    # tests a GET HTTP with a valid jwt token;
    response = client.get('orders/user/orders/1', headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 200
    assert len(list(response.json())) == 6

    # tests a GET HTTP with a fake jwt token;
    response = client.get('orders/user/orders/1', headers={'Authorization': 'Bearer fake_token'})
    assert response.status_code == 401


def test_update_order():
    data = {
        "quantity": 2,
        "flavour": "PEPPERONI",
        "size": "LARGE"
    }

    unvalid_data = {
        "quantity": 2,
        "flavour": "unvalid_value",
        "size": "unvalid_value"
    }

    # tests an order update with a valid jwt token;
    response = client.put('orders/order/update/1', json=data, headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 202
    assert response.json()['quantity'] == 2

    # tests an order update with a fake jwt token;
    response = client.put('orders/order/update/1', json=data, headers={'Authorization': f'Bearer fake_token'})
    assert response.status_code == 401
    
    # tests an order update with an unexisting order;
    response = client.put('orders/order/update/2', json=data, headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 404

    # tests an order update with an unvalid request body;
    response = client.put('orders/order/update/1', json=unvalid_data, headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 422

def test_delete_order():
    # tests an order delete on a unexisting order;
    response = client.delete('orders/order/delete/2', headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 404

    # tests an order delete without being authenticated;
    response = client.delete('orders/order/delete/1', headers={'Authorization': f'Bearer fake_token'})
    assert response.status_code == 401

    # tests an order delete with a valid jwt token;
    response = client.delete('orders/order/delete/1', headers={'Authorization': f'Bearer {user_jwt_token}'})
    assert response.status_code == 204