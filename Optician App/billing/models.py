from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from your_database_setup import db  # Make sure db is correctly imported from your setup file
import datetime
from typing import List

class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    customer_name = db.Column(db.String, nullable=False)
    total_amount = db.Column(db.Float, default=0.0)
    tax = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending')
    
    # 🔥 FIX: Use "InvoiceLine" in quotes for forward reference
    lines: List['InvoiceLine'] = db.relationship("InvoiceLine", backref="invoice", lazy=True) # type: ignore

    def __init__(self, customer_name: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.customer_name = customer_name

    def serialize(self) -> dict:
        return {
            "invoice_id": self.invoice_id,
            "date": self.date.isoformat() if self.date else None,
            "customer_name": self.customer_name,
            "total_amount": self.total_amount,
            "tax": self.tax,
            "discount": self.discount,
            "status": self.status,
            "lines": [line.serialize() for line in self.lines],
        }

class InvoiceLine(db.Model):
    __tablename__ = 'invoice_lines'
    line_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.invoice_id'))
    item_id = db.Column(db.Integer)  # Optionally, you might use a ForeignKey if you have an inventory table.
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)

    def __init__(self, item_id: int, quantity: int, unit_price: float, line_total: float, **kwargs) -> None:
        super().__init__(**kwargs)
        self.item_id = item_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.line_total = line_total

    def serialize(self) -> dict:
        return {
            "line_id": self.line_id,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "line_total": self.line_total,
        }
