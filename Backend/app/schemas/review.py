from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date as dt

class ReviewSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    """Schema representing a product review."""
    id: int
    product_id: int
    seller_id: int
    buyer: str
    review: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    date: Optional[dt] = None