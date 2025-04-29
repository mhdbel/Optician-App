# billing/views.py (or reporting/views.py)
@reporting_bp.route('/reports/historical-sales', methods=['GET'])
def historical_sales_report():
    start_date = request.args.get('start_date')  # expected format: YYYY-MM-DD
    end_date = request.args.get('end_date')
    category = request.args.get('category')  # optional filter
    # Perform your query aggregation based on these filters…
    # For illustration, let’s assume we return a dummy response:
    response = {
        "dates": ["2025-04-20", "2025-04-21", "2025-04-22"],
        "total_sales": [1200.0, 1500.0, 1000.0],
        "invoice_counts": [10, 12, 8]
    }
    return jsonify(response), 200
