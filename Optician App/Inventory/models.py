# inventory/models.py
from sqlalchemy import Column, Integer, String, Float
from your_database_setup import Base

class Item(Base):
    __tablename__ = 'items'
    
    item_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    reorder_threshold = Column(Integer, default=5)

    def serialize(self):
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
