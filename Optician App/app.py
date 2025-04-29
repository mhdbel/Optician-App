# app.py
from flask import Flask
from inventory.views import inventory_bp
from billing.views import billing_bp
from reporting.views import reporting_bp
from your_database_setup import init_db
import config # type: ignore

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize database and create tables
init_db(app)

# Register blueprints with a common prefix, e.g. /api
app.register_blueprint(inventory_bp, url_prefix='/api')
app.register_blueprint(billing_bp, url_prefix='/api')
app.register_blueprint(reporting_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
