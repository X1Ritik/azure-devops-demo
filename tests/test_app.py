import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../app'))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_get_todos_empty(client):
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.get_json() == []

def test_add_todo(client):
    response = client.post("/api/todos",
        json={"text": "buy milk"},
        content_type="application/json")
    assert response.status_code == 201
    assert response.get_json()["text"] == "buy milk"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200