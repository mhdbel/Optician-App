# inventory/services.py
from .models import Item
from your_database_setup import db

def get_all_items():
    return Item.query.all()

def create_item(data):
    new_item = Item(
        name=data.get('name'),
        sku=data.get('sku'),
        description=data.get('description', ""),
        price=data.get('price'),
        cost=data.get('cost'),
        stock_quantity=data.get('stock_quantity', 0),
        reorder_threshold=data.get('reorder_threshold', 5)
    )
    db.session.add(new_item)
    db.session.commit()
    return new_item

def update_stock(item_id, quantity_change):
    """
    Adjust the stock quantity. A negative quantity_change indicates a deduction.
    """
    item = Item.query.get(item_id)
    if item:
        if item.stock_quantity + quantity_change < 0:
            raise ValueError("Insufficient stock for item: " + item.name)
        item.stock_quantity += quantity_change
        db.session.commit()
        return item
    else:
        raise ValueError("Item not found")
