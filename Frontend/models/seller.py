from pydantic import BaseModel
from typing import Optional

from models.general_rating import GeneralRating

class Seller(BaseModel):
    id: int
    name: str
    location: str
    email: str
    phone: str
    rating_info: Optional[GeneralRating] = None
