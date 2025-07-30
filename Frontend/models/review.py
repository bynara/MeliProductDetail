from pydantic import BaseModel
from typing import Optional

class Review(BaseModel):
    id: int
    product_id: int
    seller_id: int
    buyer: str
    review: Optional[str] = None
    rating: int
    date: Optional[str] = None
