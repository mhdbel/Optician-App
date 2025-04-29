# inventory/__init__.py

"""
This file initializes the inventory package. It re-exports commonly used 
modules and functions, so that they can be imported directly from the 'inventory' package.
"""

from .models import Item
from .services import get_all_items, update_stock

# You can add additional initializations or helper functions here if needed.

