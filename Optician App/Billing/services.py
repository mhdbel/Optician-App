# billing/services.py
from .models import Invoice, InvoiceLine
from inventory.models import Item
from your_database_setup import db

def create_invoice(customer_name, items, tax_rate=0.05, discount=0.0):
    """
    Create an invoice for a set of items.
    :param customer_name: Name of the customer.
    :param items: List of dicts with 'item_id' and 'quantity'.
    :param tax_rate: Tax rate as a decimal.
    :param discount: Any discount to subtract from the total.
    """
    invoice = Invoice(customer_name=customer_name)
    total_amount = 0.0

    for item_line in items:
        item_id = item_line.get('item_id')
        quantity = item_line.get('quantity')
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
    invoice.status = 'paid'  # This can be adjusted per your business logic

    db.session.add(invoice)
    db.session.commit()
    return invoice
