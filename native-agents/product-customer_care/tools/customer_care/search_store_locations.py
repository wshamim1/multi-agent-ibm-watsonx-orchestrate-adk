from typing import List, Optional

from pydantic import BaseModel, Field
from enum import Enum

from ibm_watsonx_orchestrate.agent_builder.tools import tool, ToolPermission

class StoreType(str, Enum):
    FLAGSHIP = 'Flagship Store'
    OUTLET = 'Outlet Store'
    WAREHOUSE = 'Warehouse'
    PICKUP_POINT = 'Pickup Point'

class StoreLocation(BaseModel):
    store_id: str = Field(..., description="The unique identifier of the store")
    name: str = Field(..., description="The store name")
    store_type: StoreType = Field(..., description="Type of store")
    address: str = Field(..., description="The address of the store")
    phone: str = Field(..., description="Store phone number")
    hours: str = Field(..., description="Store operating hours")
    services: List[str] = Field(..., description="Available services at this location")

@tool
def search_store_locations(
        location: str,
        store_type: Optional[StoreType] = None
) -> List[StoreLocation]:
    """
    Find nearby store locations where you can shop, pick up orders, or return items.
    Search by city, state, or zip code.

    Args:
        location: Geographic location to search stores in (city, state, zip code, etc.)
        store_type: (Optional) Type of store to filter by (Flagship Store, Outlet Store, Warehouse, Pickup Point)

    Returns:
      A list of store locations near the specified location
    """
    # Mock store data
    all_stores = [
        {
            "store_id": "STR001",
            "name": "TechMart Boston Flagship",
            "store_type": "Flagship Store",
            "address": "100 Boylston St, Boston, MA 02116",
            "phone": "(617) 555-0100",
            "hours": "Mon-Sat: 9AM-9PM, Sun: 10AM-7PM",
            "services": ["In-store pickup", "Returns", "Tech support", "Product demos"]
        },
        {
            "store_id": "STR002",
            "name": "TechMart Cambridge Outlet",
            "store_type": "Outlet Store",
            "address": "50 Cambridge St, Cambridge, MA 02141",
            "phone": "(617) 555-0200",
            "hours": "Mon-Sat: 10AM-8PM, Sun: 11AM-6PM",
            "services": ["In-store pickup", "Returns", "Clearance items"]
        },
        {
            "store_id": "STR003",
            "name": "TechMart Warehouse - Somerville",
            "store_type": "Warehouse",
            "address": "200 Assembly Row, Somerville, MA 02145",
            "phone": "(617) 555-0300",
            "hours": "Mon-Fri: 8AM-6PM, Sat: 9AM-5PM",
            "services": ["Bulk orders", "Business accounts", "In-store pickup"]
        },
        {
            "store_id": "STR004",
            "name": "TechMart Pickup - Brookline",
            "store_type": "Pickup Point",
            "address": "300 Harvard St, Brookline, MA 02446",
            "phone": "(617) 555-0400",
            "hours": "Mon-Sun: 8AM-10PM",
            "services": ["In-store pickup", "Returns", "24/7 locker access"]
        }
    ]
    
    # Filter by store type if provided
    if store_type:
        stores = [s for s in all_stores if s['store_type'] == store_type]
    else:
        stores = all_stores
    
    # Convert to StoreLocation objects
    store_locations = [StoreLocation(**store) for store in stores]
    
    # In a real implementation, we would filter by location proximity
    # For now, return all matching stores
    return store_locations