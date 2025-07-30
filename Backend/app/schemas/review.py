from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as dt

class ReviewSchema(BaseModel):
    """Schema representing a product review."""
    id: int
    product_id: int
    seller_id: int
    buyer: str
    review: Optional[str] = None
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    date: Optional[dt] = None

    class Config:
        orm_mode = True