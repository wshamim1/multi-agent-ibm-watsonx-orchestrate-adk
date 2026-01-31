from typing import List, Optional
from pydantic import BaseModel, Field

from ibm_watsonx_orchestrate.agent_builder.tools import tool

class ProductReview(BaseModel):
    """Represents a customer review for a product."""
    review_id: str = Field(..., description="Unique review identifier")
    customer_name: str = Field(..., description="Name of the reviewer")
    rating: float = Field(..., description="Rating out of 5 stars")
    review_date: str = Field(..., description="Date the review was posted")
    review_text: str = Field(..., description="Review content")
    verified_purchase: bool = Field(..., description="Whether this is a verified purchase")
    helpful_count: int = Field(..., description="Number of people who found this helpful")

@tool
def get_product_reviews(product_id: str, min_rating: Optional[int] = None) -> List[ProductReview]:
    """
    Get customer reviews for a specific product. Helps customers make informed purchase decisions
    by reading what other customers think about the product.

    Args:
        product_id: The unique identifier of the product (e.g., ELEC001, CLOTH001)
        min_rating: Optional minimum rating filter (1-5 stars). Only show reviews with this rating or higher.

    Returns:
        A list of customer reviews for the product, including ratings, review text, and helpful counts.
    """
    # Mock review data
    all_reviews = {
        "ELEC001": [
            {
                "review_id": "REV001",
                "customer_name": "Sarah M.",
                "rating": 5.0,
                "review_date": "2025-01-20",
                "review_text": "Amazing sound quality! The noise cancellation is incredible. Battery lasts all day. Highly recommend!",
                "verified_purchase": True,
                "helpful_count": 45
            },
            {
                "review_id": "REV002",
                "customer_name": "John D.",
                "rating": 4.0,
                "review_date": "2025-01-18",
                "review_text": "Great headphones overall. Comfortable for long wear. Only minor issue is the Bluetooth range could be better.",
                "verified_purchase": True,
                "helpful_count": 23
            },
            {
                "review_id": "REV003",
                "customer_name": "Emily R.",
                "rating": 5.0,
                "review_date": "2025-01-15",
                "review_text": "Best purchase I've made this year! Perfect for working from home and blocking out distractions.",
                "verified_purchase": True,
                "helpful_count": 67
            }
        ],
        "ELEC002": [
            {
                "review_id": "REV004",
                "customer_name": "Mike T.",
                "rating": 4.5,
                "review_date": "2025-01-22",
                "review_text": "Excellent fitness tracking features. GPS is accurate. Battery life is impressive - lasts 3 days with heavy use.",
                "verified_purchase": True,
                "helpful_count": 34
            },
            {
                "review_id": "REV005",
                "customer_name": "Lisa K.",
                "rating": 5.0,
                "review_date": "2025-01-19",
                "review_text": "Love this smartwatch! Tracks everything I need. The heart rate monitor is very accurate.",
                "verified_purchase": True,
                "helpful_count": 56
            }
        ],
        "HOME001": [
            {
                "review_id": "REV006",
                "customer_name": "David L.",
                "rating": 5.0,
                "review_date": "2025-01-21",
                "review_text": "Professional quality cookware at a great price. Heats evenly and the non-stick coating works perfectly.",
                "verified_purchase": True,
                "helpful_count": 89
            }
        ]
    }
    
    # Get reviews for the product
    reviews = all_reviews.get(product_id, [])
    
    # Filter by minimum rating if specified
    if min_rating is not None:
        reviews = [r for r in reviews if r['rating'] >= min_rating]
    
    # Convert to ProductReview objects
    return [ProductReview(**review) for review in reviews]

