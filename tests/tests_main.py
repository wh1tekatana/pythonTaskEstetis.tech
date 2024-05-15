# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_courier():
    response = client.post(
        "/courier/",
        json={"name": "John Doe", "districts": ["District 1", "District 2"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["districts"] == ["District 1", "District 2"]


def test_get_courier():
    response = client.get("/courier/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "districts" in data

def test_update_courier():
    response = client.put(
        "/courier/1",
        json={"name": "Updated Name", "districts": ["Updated District"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Updated Name"
    assert data["districts"] == ["Updated District"]

def test_create_order():
    response = client.post(
        "/order/",
        json={"name": "Test Order", "district": "District 1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert "courier_id" in data
