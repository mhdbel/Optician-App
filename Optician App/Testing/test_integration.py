# test_integration.py
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_full_flow(client):
    # 1. Create an inventory item
    create_response = client.post('/api/inventory', json={
        "name": "Optician Frame",
        "sku": "OF001",
        "price": 150.0,
        "cost": 90.0,
        "stock_quantity": 10,
        "reorder_threshold": 3
    })
    assert create_response.status_code == 201
    item_id = create_response.get_json()['item_id']

    # 2. Create an invoice deducting some items
    invoice_response = client.post('/api/invoices', json={
        "customer_name": "Alice Smith",
        "items": [
            {"item_id": item_id, "quantity": 2}
        ],
        "tax_rate": 0.05,
        "discount": 5.0
    })
    assert invoice_response.status_code == 201

    # 3. Verify that inventory has been updated
    list_response = client.get('/api/inventory')
    updated_item = list_response.get_json()[0]
    assert updated_item["stock_quantity"] == 8
