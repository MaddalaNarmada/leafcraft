import pytest
from fastapi.testclient import TestClient
from main import app
from utils.auth import create_token

client = TestClient(app)


def test_list_orders_with_valid_token():
    # Create valid JWT token and setting authorization header
    token = create_token("admin@gmail.com")
    headers = {"Authorization": f"Bearer {token}"}

    #makes API call
    response = client.get("/orders/", headers=headers)

    #check the response
    assert response.status_code == 200
    assert isinstance(response.json(), list)
