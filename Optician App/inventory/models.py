# inventory/models.py
from your_database_setup import db

class Item(db.Model):
    __tablename__ = 'items'
    
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sku = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, default="")
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, default=0)
    reorder_threshold = db.Column(db.Integer, default=5)
    
    def __init__(
        self,
        name: str,
        sku: str,
        description: str,
        price: float,
        cost: float,
        stock_quantity: int = 0,
        reorder_threshold: int = 5
    ) -> None:
        self.name = name
        self.sku = sku
        self.description = description
        self.price = price
        self.cost = cost
        self.stock_quantity = stock_quantity
        self.reorder_threshold = reorder_threshold

    def serialize(self) -> dict:
        return {
            "item_id": self.item_id,
            "name": self.name,
            "sku": self.sku,
            "description": self.description,
            "price": self.price,
            "cost": self.cost,
            "stock_quantity": self.stock_quantity,
            "reorder_threshold": self.reorder_threshold,
        }
