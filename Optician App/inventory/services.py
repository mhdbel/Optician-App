# inventory/services.py
from .models import Item
from your_database_setup import db
from sqlalchemy.orm import Session
from typing import List

def get_all_items() -> List[Item]:
    session: Session = db.session  # type: ignore
    return session.query(Item).all()

def update_stock(item_id: int, new_stock: int) -> Item:
    session: Session = db.session  # type: ignore
    item = session.query(Item).get(item_id)
    if not item:
        raise ValueError(f"Item with id {item_id} not found")
    item.stock_quantity = new_stock
    session.commit()
    return item
