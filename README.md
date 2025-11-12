Mini Order & Inventory Management API
-------------------------------------

This project implements Mini Order & Inventory Management API built with FastAPI, SQL Alchemy ORM and MySQL
It provides endpoints for managing products and orders, stock-level checking, and follows business logic consistency for order confirmation and cancellation, 
includes of caching and authentication.

Functionalities:
---------------
1.Creation and listing of products
2.Creation and listing of orders
3.Cancellation and confirmation of orders
4.Reduce and restore stock levels
5.Caching for endpoints
6.JWT authentication for endpoints

Technical:
----------
Backend - Python, FastAPI
pydantic for validations
MySQL for database
SQLAlchemy
Caching - In-memory
JWt for authentication

How to run and setup instructions:
----------------------------------
1. git clone <https://github.com/MaddalaNarmada/leafcraft.git>
cd leafcraft

2. Install dependencies - pip install -r requirements.txt

3. Update database in database.py - DATABASE_URL = "mysql+pymysql://{username}:{password}@{host}/{database}"
   Added local db credentials

4. Run server - uvicorn app.main:app --reload

Now You can see API through link - http://127.0.0.1:8000/

API Requests/Responses:
-----------------------
1. create New Product
   http://127.0.0.1:8000/products/

   Example schema -
{"name": "product name",
  "stock_quantity": 10,
  "price": 25.99,
  "id": 1
}


2. Get List of products
   http://127.0.0.1:8000/products/

   Example response
[{
    "name": "Test Prod",
    "stock_quantity": 12,
    "price": 199,
    "id": 1
  },
  {
    "name": "Hoodie",
    "stock_quantity": 0,
    "price": 499.9,
    "id": 2

  }]

    3.Create New Order
    http://127.0.0.1:8000/orders/create_order

    Example schema
{
  "id": 4,
  "items": [
    {
      "quantity": 1,
      "product_id": 5
    },
    {
      "quantity": 2,
      "product_id": 4
    }
  ],
  "total_amount": 1407.98,
  "status": "Pending"
}

4.Confirm Order
    http://127.0.0.1:8000/orders/{order_id}/confirm
{
  "message": "Order Confirmed successfully"
}

5.Cancel Order
     http://127.0.0.1:8000/orders/7/cancel

6.Get List of all Orders
    http://127.0.0.1:8000/orders/
[
  {
    "id": 1,
    "items": [
      {
        "quantity": 2,
        "product_id": 2
      }
    ],
    "total_amount": 999.8,
    "status": "Pending"
  },
  {
    "id": 2,
    "items": [
      {
        "quantity": 1,
        "product_id": 1
      }
    ],
    "total_amount": 199,
    "status": "Cancelled"
  }]



Business Logic summary:
-----------------------
  1.On order creation status will be pending, stock will be same
  2.On confirmation:
      a.First check stock availabilty
        If stock available, then order status mark as confirmed and reduce stock
  3.On cancellation:
      a.Restore stock, and update status as cancelled

Running Tests:
--------------
Enter " pytest tests/test_orders.py -v"



Note:
-----
In database.py - need to use localhost credentials
In auth.py - need to add secret key for authentication
