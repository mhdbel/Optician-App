# billing/models.py
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from your_database_setup import Base
import datetime

class Invoice(Base):
    __tablename__ = 'invoices'
    invoice_id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    customer_name = Column(String, nullable=False)
    total_amount = Column(Float, default=0)
    tax = Column(Float, default=0)
    discount = Column(Float, default=0)
    status = Column(String, default='pending')  # e.g., 'pending', 'paid'
    lines = relationship("InvoiceLine", backref="invoice")

    def serialize(self):
        return {
            "invoice_id": self.invoice_id,
            "date": self.date.isoformat(),
            "customer_name": self.customer_name,
            "total_amount": self.total_amount,
            "tax": self.tax,
            "discount": self.discount,
            "status": self.status,
            "lines": [line.serialize() for line in self.lines]
        }

class InvoiceLine(Base):
    __tablename__ = 'invoice_lines'
    line_id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.invoice_id'))
    item_id = Column(Integer, ForeignKey('items.item_id'))  # linking to inventory
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)

    def serialize(self):
        return {
            "line_id": self.line_id,
            "item_id": self.item_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "line_total": self.line_total
        }
