# billing/services.py
from .models import Invoice, InvoiceLine
from inventory.models import Item
from your_database_setup import db
from sqlalchemy.orm import Session
from typing import List, Dict, Any

def create_invoice(
    customer_name: str,
    items: List[Dict[str, Any]],
    tax_rate: float = 0.05,
    discount: float = 0.0
) -> Invoice:
    """
    Create an invoice for a set of items.
    
    :param customer_name: Name of the customer.
    :param items: List of dictionaries with keys 'item_id' and 'quantity'.
    :param tax_rate: Tax rate as a decimal.
    :param discount: Any discount to subtract from the total.
    :return: The created Invoice instance.
    """
    invoice = Invoice(customer_name=customer_name)
    total_amount = 0.0

    for item_line in items:
        # Retrieve and validate the 'item_id'
        item_id = item_line.get('item_id')
        if item_id is None:
            raise ValueError("Missing 'item_id' in one of the items")
        try:
            item_id = int(item_id)
        except Exception as e:
            raise ValueError("'item_id' must be an integer") from e

        # Retrieve and validate the 'quantity'
        quantity = item_line.get('quantity')
        if quantity is None:
            raise ValueError("Missing 'quantity' in one of the items")
        try:
            quantity = int(quantity)
        except Exception as e:
            raise ValueError("'quantity' must be an integer") from e

        item = Item.query.get(item_id)
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")
        if item.stock_quantity < quantity:
            raise ValueError(f"Insufficient stock for item: {item.name}")

        # Deduct stock (this update is made here)
        item.stock_quantity -= quantity

        line_total = quantity * item.price
        inv_line = InvoiceLine(
            item_id=item_id,
            quantity=quantity,
            unit_price=item.price,
            line_total=line_total
        )
        invoice.lines.append(inv_line)
        total_amount += line_total

    invoice.tax = total_amount * tax_rate
    invoice.discount = discount
    invoice.total_amount = total_amount + invoice.tax - discount
    invoice.status = 'paid'  # Adjust per your business logic

    # Cast db.session to a SQLAlchemy Session so that type checkers recognize add() and commit()
    session: Session = db.session  # type: ignore
    session.add(invoice)
    session.commit()
    return invoice
