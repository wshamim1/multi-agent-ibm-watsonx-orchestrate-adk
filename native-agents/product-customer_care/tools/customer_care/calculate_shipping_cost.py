from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

from ibm_watsonx_orchestrate.agent_builder.tools import tool

class ShippingMethod(str, Enum):
    STANDARD = "Standard Shipping"
    EXPRESS = "Express Shipping"
    OVERNIGHT = "Overnight Shipping"
    SAME_DAY = "Same Day Delivery"

class ShippingOption(BaseModel):
    """Represents a shipping option with cost and delivery time."""
    method: ShippingMethod = Field(..., description="Shipping method name")
    cost: float = Field(..., description="Shipping cost in USD")
    delivery_days: str = Field(..., description="Estimated delivery time")
    description: str = Field(..., description="Description of the shipping method")

@tool
def calculate_shipping_cost(
    zip_code: str,
    order_total: float,
    weight_lbs: Optional[float] = 5.0
) -> list[ShippingOption]:
    """
    Calculate shipping costs for different delivery methods based on destination zip code,
    order total, and package weight. Helps customers choose the best shipping option.

    Args:
        zip_code: Destination zip code (e.g., "02101" for Boston)
        order_total: Total order amount in USD (free shipping may apply for orders over $50)
        weight_lbs: Package weight in pounds (default: 5.0 lbs)

    Returns:
        List of available shipping options with costs and estimated delivery times.
    """
    # Determine if free shipping applies
    free_shipping_threshold = 50.0
    qualifies_for_free_shipping = order_total >= free_shipping_threshold
    
    # Base shipping rates (would normally call a shipping API)
    base_rates = {
        "Standard Shipping": 5.99,
        "Express Shipping": 12.99,
        "Overnight Shipping": 24.99,
        "Same Day Delivery": 15.99
    }
    
    # Adjust rates based on weight (add $1 per lb over 5 lbs)
    actual_weight = weight_lbs if weight_lbs is not None else 5.0
    weight_surcharge = max(0, (actual_weight - 5.0) * 1.0)
    
    # Check if zip code is in local delivery area (Boston area)
    local_zip_prefixes = ["021", "024"]  # Boston and surrounding areas
    is_local = any(zip_code.startswith(prefix) for prefix in local_zip_prefixes)
    
    shipping_options = []
    
    # Standard Shipping
    standard_cost = 0.0 if qualifies_for_free_shipping else base_rates["Standard Shipping"] + weight_surcharge
    shipping_options.append(ShippingOption(
        method=ShippingMethod.STANDARD,
        cost=round(standard_cost, 2),
        delivery_days="5-7 business days",
        description="Free for orders over $50" if qualifies_for_free_shipping else "Economical shipping option"
    ))
    
    # Express Shipping
    express_cost = base_rates["Express Shipping"] + weight_surcharge
    shipping_options.append(ShippingOption(
        method=ShippingMethod.EXPRESS,
        cost=round(express_cost, 2),
        delivery_days="2-3 business days",
        description="Faster delivery with tracking"
    ))
    
    # Overnight Shipping
    overnight_cost = base_rates["Overnight Shipping"] + weight_surcharge
    shipping_options.append(ShippingOption(
        method=ShippingMethod.OVERNIGHT,
        cost=round(overnight_cost, 2),
        delivery_days="Next business day",
        description="Guaranteed next-day delivery"
    ))
    
    # Same Day Delivery (only for local areas)
    if is_local:
        same_day_cost = base_rates["Same Day Delivery"] + weight_surcharge
        shipping_options.append(ShippingOption(
            method=ShippingMethod.SAME_DAY,
            cost=round(same_day_cost, 2),
            delivery_days="Same day (order by 2 PM)",
            description="Available for Boston metro area only"
        ))
    
    return shipping_options

