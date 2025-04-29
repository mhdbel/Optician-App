from flask import Blueprint, request, jsonify
from sqlalchemy import func
from billing.models import Invoice
from inventory.models import Item
from your_database_setup import db
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import cast
import datetime

reporting_bp = Blueprint('reporting_bp', __name__, url_prefix='/api/reports')

@reporting_bp.route('/daily-sales', methods=['GET'])
def daily_sales_report():
    """
    Returns daily sales information given a 'date' query parameter (YYYY-MM-DD).
    Defaults to today's date if no date is provided.
    """
    # Use today's date as default if no date is given.
    date_str = request.args.get("date", datetime.date.today().strftime("%Y-%m-%d"))
    try:
        report_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Expected YYYY-MM-DD."}), 400

    start_datetime = datetime.datetime.combine(report_date, datetime.time.min)
    end_datetime = datetime.datetime.combine(report_date, datetime.time.max)

    # Use db.session.query() rather than Invoice.query to appease the type checker.
    invoices = db.session.query(Invoice).filter(
        Invoice.date >= start_datetime,
        Invoice.date <= end_datetime
    ).all()

    total_sales = sum(invoice.total_amount for invoice in invoices)
    invoice_count = len(invoices)

    return jsonify({
        "date": date_str,
        "total_sales": total_sales,
        "invoice_count": invoice_count
    }), 200

@reporting_bp.route('/historical-sales', methods=['GET'])
def historical_sales_report():
    """
    Returns historical sales data grouped by day between start_date and end_date.
    Both dates must be in YYYY-MM-DD format.
    """
    start_str = request.args.get("start_date")
    end_str = request.args.get("end_date")
    if not start_str or not end_str:
        return jsonify({"error": "start_date and end_date are required in YYYY-MM-DD format."}), 400

    try:
        start_date = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Expected YYYY-MM-DD."}), 400

    start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
    end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

    # Query historical sales using db.session.query()
    results = db.session.query(
        func.date(Invoice.date).label("report_date"),
        func.sum(Invoice.total_amount).label("total_sales"),
        func.count(Invoice.invoice_id).label("invoice_count")
    ).filter(
        Invoice.date >= start_datetime,
        Invoice.date <= end_datetime
    ).group_by(
        func.date(Invoice.date)
    ).order_by(
        func.date(Invoice.date)
    ).all()

    # Unpack each returned tuple directly.
    report = [
        {
            "date": str(report_date),
            "total_sales": total_sales,
            "invoice_count": invoice_count
        }
        for report_date, total_sales, invoice_count in results
    ]
    return jsonify(report), 200

@reporting_bp.route('/low-stock', methods=['GET'])
def low_stock_report():
    """
    Returns a list of items with low stock.
    Optionally filters by category if the 'category' query parameter is provided.
    """
    # Use db.session.query(Item) instead of Item.query.
    query = db.session.query(Item).filter(
        cast(BinaryExpression, Item.stock_quantity <= Item.reorder_threshold)
    )

    category_param = request.args.get("category")
    if category_param and hasattr(Item, "category"):
        # Cast the attribute to InstrumentedAttribute to help with type checking.
        category_col = cast(InstrumentedAttribute, getattr(Item, "category"))
        query = query.filter(category_col == category_param)

    items = query.all()
    return jsonify([item.serialize() for item in items]), 200
