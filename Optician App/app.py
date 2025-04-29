# app.py
from flask import Flask
from flask_restx import Api, Resource, fields
from your_database_setup import init_db
import config
from inventory.views import inventory_bp  # ensure these blueprints or controllers are adapted

app = Flask(__name__)
app.config.from_object(config.Config)
init_db(app)

# Initialize Flask-RESTX API and attach Swagger UI (default at /)
api = Api(app, version='1.0', title='Optician Store API',
          description='API Documentation for Inventory & Billing',
          )

# Define a namespace and model for one endpoint as an example
ns = api.namespace('reports', description='Reports operations')

historical_sales_model = api.model('HistoricalSales', {
    'dates': fields.List(fields.String(required=True, description='List of dates')),
    'total_sales': fields.List(fields.Float(required=True, description='Sales total by date')),
    'invoice_counts': fields.List(fields.Integer(required=True, description='Number of invoices by date'))
})

@ns.route('/historical-sales')
class HistoricalSales(Resource):
    @api.doc(params={'start_date': 'Start date (YYYY-MM-DD)',
                     'end_date': 'End date (YYYY-MM-DD)',
                     'category': 'Product category (optional)'})
    @api.marshal_with(historical_sales_model)
    def get(self):
        # Dummy implementation – plug in your actual query and aggregation.
        start_date = api.payload.get('start_date', '2025-04-20')
        end_date = api.payload.get('end_date', '2025-04-22')
        return {
            "dates": ["2025-04-20", "2025-04-21", "2025-04-22"],
            "total_sales": [1200.0, 1500.0, 1000.0],
            "invoice_counts": [10, 12, 8]
        }
