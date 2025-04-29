# inventory/views.py
from flask import Blueprint, request, jsonify
from inventory.services import get_all_items, update_stock

inventory_bp = Blueprint("inventory_bp", __name__, url_prefix="/api/inventory")

@inventory_bp.route("/items", methods=["GET"])
def list_items():
    items = get_all_items()
    return jsonify([item.serialize() for item in items]), 200

@inventory_bp.route("/items/<int:item_id>/stock", methods=["POST"])
def change_stock(item_id):
    data = request.get_json() or {}
    new_stock = data.get("stock_quantity")
    if new_stock is None:
        return jsonify({"error": "Missing 'stock_quantity' parameter"}), 400
    try:
        new_stock = int(new_stock)
    except (ValueError, TypeError):
        return jsonify({"error": "'stock_quantity' must be an integer"}), 400
    try:
        updated_item = update_stock(item_id, new_stock)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(updated_item.serialize()), 200
