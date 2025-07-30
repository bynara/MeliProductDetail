from pydantic import BaseModel
from typing import Optional
from datetime import date as dt

class ReviewModel(BaseModel):
    id: int
    product_id: int
    seller_id: int
    buyer: str
    review: str
    rating: int
    date: Optional[dt] = None

    class Config:
        orm_mode = True