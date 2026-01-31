from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import random

from ibm_watsonx_orchestrate.agent_builder.tools import tool

class ShipmentEvent(BaseModel):
    """Represents a tracking event in the shipment journey."""
    timestamp: str = Field(..., description="Date and time of the event")
    location: str = Field(..., description="Location where the event occurred")
    status: str = Field(..., description="Status description")
    details: Optional[str] = Field(None, description="Additional details about the event")

class ShipmentTracking(BaseModel):
    """Represents complete shipment tracking information."""
    tracking_number: str = Field(..., description="Shipment tracking number")
    carrier: str = Field(..., description="Shipping carrier (FedEx, UPS, USPS)")
    current_status: str = Field(..., description="Current shipment status")
    estimated_delivery: str = Field(..., description="Estimated delivery date")
    origin: str = Field(..., description="Origin location")
    destination: str = Field(..., description="Destination address")
    events: List[ShipmentEvent] = Field(..., description="List of tracking events")

@tool
def track_shipment(tracking_number: str) -> ShipmentTracking:
    """
    Track a shipment using the tracking number. Get real-time updates on package location,
    delivery status, and estimated delivery date. Works with major carriers like FedEx, UPS, and USPS.

    Args:
        tracking_number: The tracking number provided when the order was shipped (e.g., TRK9876543210)

    Returns:
        Complete tracking information including current status, location, and delivery estimate.
    """
    # Mock tracking data based on tracking number
    mock_tracking = {
        "TRK9876543210": {
            "tracking_number": "TRK9876543210",
            "carrier": "FedEx",
            "current_status": "Delivered",
            "estimated_delivery": "2025-01-20",
            "origin": "TechMart Warehouse, Somerville, MA",
            "destination": "123 Main St, Boston, MA 02101",
            "events": [
                {
                    "timestamp": "2025-01-20T14:30:00",
                    "location": "Boston, MA",
                    "status": "Delivered",
                    "details": "Package delivered to front door. Signed by: Resident"
                },
                {
                    "timestamp": "2025-01-20T09:15:00",
                    "location": "Boston, MA",
                    "status": "Out for Delivery",
                    "details": "Package is on the delivery vehicle"
                },
                {
                    "timestamp": "2025-01-20T06:00:00",
                    "location": "Boston Distribution Center, MA",
                    "status": "Arrived at Facility",
                    "details": "Package arrived at local facility"
                },
                {
                    "timestamp": "2025-01-19T18:45:00",
                    "location": "Somerville, MA",
                    "status": "In Transit",
                    "details": "Package departed from origin facility"
                },
                {
                    "timestamp": "2025-01-19T15:00:00",
                    "location": "TechMart Warehouse, Somerville, MA",
                    "status": "Picked Up",
                    "details": "Package picked up by carrier"
                }
            ]
        },
        "TRK1234567890": {
            "tracking_number": "TRK1234567890",
            "carrier": "UPS",
            "current_status": "In Transit",
            "estimated_delivery": "2025-02-02",
            "origin": "TechMart Warehouse, Somerville, MA",
            "destination": "123 Main St, Boston, MA 02101",
            "events": [
                {
                    "timestamp": "2025-01-30T08:30:00",
                    "location": "Hartford, CT",
                    "status": "In Transit",
                    "details": "Package is in transit to next facility"
                },
                {
                    "timestamp": "2025-01-29T22:15:00",
                    "location": "New York, NY",
                    "status": "Departed Facility",
                    "details": "Package departed from sorting facility"
                },
                {
                    "timestamp": "2025-01-29T14:00:00",
                    "location": "New York, NY",
                    "status": "Arrived at Facility",
                    "details": "Package arrived at UPS facility"
                },
                {
                    "timestamp": "2025-01-28T16:30:00",
                    "location": "Somerville, MA",
                    "status": "Picked Up",
                    "details": "Package picked up by UPS"
                }
            ]
        }
    }
    
    # Get tracking info or return not found message
    if tracking_number in mock_tracking:
        tracking_data = mock_tracking[tracking_number]
        return ShipmentTracking(**tracking_data)
    else:
        # Return a generic "not found" response
        return ShipmentTracking(
            tracking_number=tracking_number,
            carrier="Unknown",
            current_status="Not Found",
            estimated_delivery="N/A",
            origin="N/A",
            destination="N/A",
            events=[
                ShipmentEvent(
                    timestamp=datetime.now().isoformat(),
                    location="System",
                    status="Not Found",
                    details=f"Tracking number {tracking_number} not found in system. Please verify the tracking number."
                )
            ]
        )

