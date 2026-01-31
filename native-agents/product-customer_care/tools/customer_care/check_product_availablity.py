from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

from ibm_watsonx_orchestrate.agent_builder.tools import tool

class StockStatus(str, Enum):
    IN_STOCK = "In Stock"
    LOW_STOCK = "Low Stock"
    OUT_OF_STOCK = "Out of Stock"
    BACKORDERED = "Backordered"

class StoreInventory(BaseModel):
    """Represents inventory at a specific store location."""
    store_id: str = Field(..., description="Store identifier")
    store_name: str = Field(..., description="Store name")
    quantity: int = Field(..., description="Number of items available")
    status: StockStatus = Field(..., description="Stock status")
    next_restock_date: Optional[str] = Field(None, description="Expected restock date if out of stock")

class ProductAvailability(BaseModel):
    """Represents product availability information."""
    product_id: str = Field(..., description="Product identifier")
    product_name: str = Field(..., description="Product name")
    online_stock: int = Field(..., description="Online warehouse stock quantity")
    online_status: StockStatus = Field(..., description="Online availability status")
    store_availability: List[StoreInventory] = Field(..., description="Availability at physical stores")
    can_ship_today: bool = Field(..., description="Whether the product can ship today")

@tool
def check_product_availability(product_id: str, check_stores: bool = True) -> ProductAvailability:
    """
    Check real-time product availability across online warehouse and physical store locations.
    Helps customers know if a product is in stock and where they can get it.

    Args:
        product_id: The unique identifier of the product (e.g., ELEC001, CLOTH001)
        check_stores: Whether to check physical store inventory (default: True)

    Returns:
        Complete availability information including online stock and store-by-store inventory.
    """
    # Mock availability data
    availability_data = {
        "ELEC001": {
            "product_id": "ELEC001",
            "product_name": "Wireless Bluetooth Headphones",
            "online_stock": 45,
            "online_status": "In Stock",
            "can_ship_today": True,
            "store_availability": [
                {
                    "store_id": "STR001",
                    "store_name": "TechMart Boston Flagship",
                    "quantity": 12,
                    "status": "In Stock",
                    "next_restock_date": None
                },
                {
                    "store_id": "STR002",
                    "store_name": "TechMart Cambridge Outlet",
                    "quantity": 3,
                    "status": "Low Stock",
                    "next_restock_date": "2025-02-05"
                },
                {
                    "store_id": "STR003",
                    "store_name": "TechMart Warehouse - Somerville",
                    "quantity": 89,
                    "status": "In Stock",
                    "next_restock_date": None
                }
            ]
        },
        "ELEC002": {
            "product_id": "ELEC002",
            "product_name": "Smart Watch Pro",
            "online_stock": 23,
            "online_status": "In Stock",
            "can_ship_today": True,
            "store_availability": [
                {
                    "store_id": "STR001",
                    "store_name": "TechMart Boston Flagship",
                    "quantity": 8,
                    "status": "In Stock",
                    "next_restock_date": None
                },
                {
                    "store_id": "STR002",
                    "store_name": "TechMart Cambridge Outlet",
                    "quantity": 0,
                    "status": "Out of Stock",
                    "next_restock_date": "2025-02-10"
                }
            ]
        },
        "HOME001": {
            "product_id": "HOME001",
            "product_name": "Stainless Steel Cookware Set",
            "online_stock": 2,
            "online_status": "Low Stock",
            "can_ship_today": True,
            "store_availability": [
                {
                    "store_id": "STR001",
                    "store_name": "TechMart Boston Flagship",
                    "quantity": 5,
                    "status": "Low Stock",
                    "next_restock_date": "2025-02-03"
                },
                {
                    "store_id": "STR003",
                    "store_name": "TechMart Warehouse - Somerville",
                    "quantity": 15,
                    "status": "In Stock",
                    "next_restock_date": None
                }
            ]
        },
        "SPORT001": {
            "product_id": "SPORT001",
            "product_name": "Yoga Mat with Carrying Strap",
            "online_stock": 67,
            "online_status": "In Stock",
            "can_ship_today": True,
            "store_availability": [
                {
                    "store_id": "STR001",
                    "store_name": "TechMart Boston Flagship",
                    "quantity": 25,
                    "status": "In Stock",
                    "next_restock_date": None
                },
                {
                    "store_id": "STR002",
                    "store_name": "TechMart Cambridge Outlet",
                    "quantity": 18,
                    "status": "In Stock",
                    "next_restock_date": None
                }
            ]
        }
    }
    
    # Get availability or return not found
    if product_id in availability_data:
        data = availability_data[product_id]
        
        # If not checking stores, return empty store list
        if not check_stores:
            data["store_availability"] = []
        
        return ProductAvailability(**data)
    else:
        # Return not found response
        return ProductAvailability(
            product_id=product_id,
            product_name="Unknown Product",
            online_stock=0,
            online_status=StockStatus.OUT_OF_STOCK,
            can_ship_today=False,
            store_availability=[]
        )

