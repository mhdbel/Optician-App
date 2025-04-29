# inventory/__init__.py
# This file can be empty, or you could import key elements:
from .models import Item
from .services import get_all_items, create_item

# Now other modules can import directly from the inventory package:
from inventory import Item, create_item
