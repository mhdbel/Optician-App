# inventory/views.py
from flask import Blueprint, request, jsonify
from .services import get_all_items, create_item, update_stock

inventory_bp = Blueprint('inventory_bp', __name__)

@inventory_bp.route('/inventory', methods=['GET'])
def list_items():
    items = get_all_items()
    return jsonify([item.serialize() for item in items]), 200

@inventory_bp.route('/inventory', methods=['POST'])
def add_item():
    data = request.get_json()
    try:
        new_item = create_item(data)
        return jsonify(new_item.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inventory_bp.route('/inventory/<int:item_id>/stock', methods=['PUT'])
def update_item_stock(item_id):
    data = request.get_json()
    change = data.get('quantity_change', 0)
    try:
        updated_item = update_stock(item_id, change)
        return jsonify(updated_item.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
