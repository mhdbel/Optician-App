# billing/views.py
from flask import Blueprint, request, jsonify
from .services import create_invoice

billing_bp = Blueprint('billing_bp', __name__)

@billing_bp.route('/invoices', methods=['POST'])
def new_invoice():
    data = request.get_json()
    customer_name = data.get('customer_name')
    items = data.get('items', [])
    tax_rate = data.get('tax_rate', 0.05)
    discount = data.get('discount', 0.0)
    try:
        invoice = create_invoice(customer_name, items, tax_rate, discount)
        return jsonify(invoice.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
