# test_services.py
import pytest
from app import app, db
from inventory.models import Item
from billing.services import create_invoice

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_item(client):
    # Create a new item via the API
    response = client.post('/api/inventory', json={
        "name": "Test Frame",
        "sku": "TF100",
        "description": "Test Description",
        "price": 100.0,
        "cost": 60.0,
        "stock_quantity": 10,
        "reorder_threshold": 2
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['name'] == "Test Frame"
    assert data['stock_quantity'] == 10

def test_update_stock(client):
    # Add an item first
    client.post('/api/inventory', json={
        "name": "Test Lens",
        "sku": "TL200",
        "price": 50.0,
        "cost": 30.0,
        "stock_quantity": 5,
        "reorder_threshold": 1
    })
    # Retrieve created item id
    response = client.get('/api/inventory')
    item = response.get_json()[0]
    item_id = item['item_id']

    # Update stock: deduct 3 items
    response = client.put(f'/api/inventory/{item_id}/stock', json={"quantity_change": -3})
    updated = response.get_json()
    assert response.status_code == 200
    assert updated['stock_quantity'] == 2

def test_create_invoice_insufficient_stock(client):
    # Add an item with limited stock
    client.post('/api/inventory', json={
        "name": "Test Accessory",
        "sku": "TA300",
        "price": 20.0,
        "cost": 10.0,
        "stock_quantity": 2,
        "reorder_threshold": 1
    })

    # Try to create an invoice that exceeds available stock
    response = client.post('/api/invoices', json={
        "customer_name": "John Doe",
        "items": [
            {"item_id": 1, "quantity": 3}  # Requesting more than available
        ],
        "tax_rate": 0.05,
        "discount": 0.0
    })
    data = response.get_json()
    assert response.status_code == 400
    assert "Insufficient stock" in data['error']
