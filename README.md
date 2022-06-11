# Pizza Delivery API
API made with FastAPI that manages a pizza delivery sistem.

# Endpoints

| METHOD	          |  ROUTE              | FUNCTIONALITY       | ACCESS              |
| ------------------- | ------------------- | ------------------- | ------------------- |
|  POST               |  /auth/signup/      | Register new user   | All users           |
|  POST               |  /auth/login/       | 	Login user        | All users           |
|  POST               |  /orders/order/     | 	Place an order    | All users           |
|  PUT                |   /orders/order/update/{order_id}/     | 	Update an order    | All users           |
|  PUT                |   /orders/order/status/{order_id}/     | 	Update order status    | Superuser         |
|  DELETE             |   /orders/order/delete/{order_id}/     | 	Delete/Remove an order    | All users         |
|  GET                |   /orders/user/orders/     | 	Get user's orders    | 	All users        |
|  GET                |   /orders/orders/     | 	List all orders made    | 	Superuser        |
|  GET                |   /orders/orders/{order_id}/     | 	Retrieve an order    | 	Superuser        |
|  GET                |   /orders/user/order/{order_id}/     | 	Get user's specific order    | 	Superuser        |


# To run you need to..
* 1. Install Docker on your system.
* 2. Once you have Docker installed, clone this repo.
```python
git clone https://github.com/cerozi/pizzadeliveryAPI.git
```
* 3. On the project root directory, opens the terminal and build the containers.
```docker-compose up --build
```
* 4. Now, you can access the API endpoints at http://0.0.0.0:8000/docs