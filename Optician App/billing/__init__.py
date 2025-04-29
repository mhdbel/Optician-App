# billing/__init__.py

"""
This file initializes the billing package. The main models (Invoice, InvoiceLine)
and service functions (e.g., create_invoice) are imported here for easy access.
"""

from .models import Invoice, InvoiceLine
from .services import create_invoice

# Additional billing-level initializations or helper functions can be added here.
