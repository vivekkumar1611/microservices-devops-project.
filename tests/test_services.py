import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]

def load_app(service):
    path = ROOT / "services" / service / "app" / "main.py"
    spec = importlib.util.spec_from_file_location(f"{service.replace('-', '_')}_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app

def test_user_health_and_create():
    client = TestClient(load_app("user-service"))
    assert client.get("/health").status_code == 200
    response = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"

def test_product_health_and_create():
    client = TestClient(load_app("product-service"))
    assert client.get("/health").status_code == 200
    response = client.post("/products", json={
        "name": "Keyboard", "description": "Mechanical keyboard", "price": 499.00
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Keyboard"

def test_order_create():
    client = TestClient(load_app("order-service"))
    response = client.post("/orders", json={"user_id": 1, "item": "Book", "quantity": 2})
    assert response.status_code == 201
    assert response.json()["status"] == "CREATED"
