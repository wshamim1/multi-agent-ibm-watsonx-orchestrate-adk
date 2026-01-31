from enum import Enum
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class ProductCategory(str, Enum):
    ELECTRONICS = 'Electronics'
    CLOTHING = 'Clothing'
    HOME_GARDEN = 'Home & Garden'
    SPORTS = 'Sports & Outdoors'
    BOOKS = 'Books'

@tool
def get_product_catalog(category: Optional[ProductCategory] = None, search_term: Optional[str] = None):
    """
    Retrieve a comprehensive list of products from our e-commerce catalog.
    Browse products by category or search for specific items.

    Args:
        category: Product category to filter by (Electronics, Clothing, Home & Garden, Sports & Outdoors, Books). If not provided, all categories will be returned.
        search_term: Optional search term to find specific products by name or description.

    Returns:
      A list of dictionaries, where each dictionary contains:
          - 'product_id': Unique identifier for the product
          - 'name': Product name
          - 'category': Product category
          - 'price': Current price in USD
          - 'stock': Number of items in stock
          - 'rating': Average customer rating (1-5 stars)
          - 'description': Brief product description
    """
    # Mock product catalog data
    products = [
        {
            "product_id": "ELEC001",
            "name": "Wireless Bluetooth Headphones",
            "category": "Electronics",
            "price": 79.99,
            "stock": 45,
            "rating": 4.5,
            "description": "Premium noise-cancelling wireless headphones with 30-hour battery life"
        },
        {
            "product_id": "ELEC002",
            "name": "Smart Watch Pro",
            "category": "Electronics",
            "price": 299.99,
            "stock": 23,
            "rating": 4.7,
            "description": "Advanced fitness tracking with heart rate monitor and GPS"
        },
        {
            "product_id": "CLOTH001",
            "name": "Cotton T-Shirt Pack (3-pack)",
            "category": "Clothing",
            "price": 29.99,
            "stock": 150,
            "rating": 4.3,
            "description": "Comfortable 100% cotton t-shirts in assorted colors"
        },
        {
            "product_id": "HOME001",
            "name": "Stainless Steel Cookware Set",
            "category": "Home & Garden",
            "price": 149.99,
            "stock": 12,
            "rating": 4.8,
            "description": "Professional 10-piece cookware set with non-stick coating"
        },
        {
            "product_id": "SPORT001",
            "name": "Yoga Mat with Carrying Strap",
            "category": "Sports & Outdoors",
            "price": 34.99,
            "stock": 67,
            "rating": 4.6,
            "description": "Extra-thick exercise mat with non-slip surface"
        },
        {
            "product_id": "BOOK001",
            "name": "The Art of Programming",
            "category": "Books",
            "price": 49.99,
            "stock": 89,
            "rating": 4.9,
            "description": "Comprehensive guide to modern software development practices"
        }
    ]
    
    # Filter by category if provided
    if category:
        products = [p for p in products if p['category'] == category]
    
    # Filter by search term if provided
    if search_term:
        search_lower = search_term.lower()
        products = [p for p in products if search_lower in p['name'].lower() or search_lower in p['description'].lower()]
    
    return products