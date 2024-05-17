import pytest
from fastapi.testclient import TestClient

from ..main import app 

@pytest.fixture
def client():
    return TestClient(app)

# Test for getting users
def test_get_users(client):
    response = client.get("/accounts/")
    assert response.status_code == 200
    assert len(response.json()) > 0  # assuming there are users in the database

# Test for creating a user
def test_create_account(client):
    user_data = {"username": "Test User", "email": "test@example.com", "password": "password123"}
    response = client.post("/accounts/", json=user_data)
    assert response.status_code == 201
    assert response.json().get("email") == "test@example.com"

# Test for getting a user by ID
def test_get_user(client):
    response = client.get("/accounts/1")  # assuming there is a user with ID 1 in the database
    assert response.status_code == 200
    assert response.json().get("username") != None  # assuming the user's name is "Test User"

# Test for updating a user
def test_update_user(client):
    user_data = {"name": "Updated Name", "email": "updated@example.com"}
    response = client.put("/accounts/1", json=user_data)  # assuming there is a user with ID 1 in the database
    assert response.status_code == 202
    assert response.json().get("name") == "Updated Name"

# Test for deleting a user
def test_delete_user(client):
    response = client.delete("/accounts/1")  # assuming there is a user with ID 1 in the database
    assert response.status_code == 202
    assert response.json().get("data") == "success!"

# Test for getting user notifications
def test_get_notifications(client):
    response = client.get("/accounts/notifications/mynotifications")
    assert response.status_code == 200
    assert len(response.json()) > 0  # assuming there are notifications in the database