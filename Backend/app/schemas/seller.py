from typing import Optional
from pydantic import BaseModel
from schemas.general_rating import GeneralRating

class SellerSchema(BaseModel):
    """Schema representing a seller."""
    id: int
    name: str
    location: str
    email: str
    phone: str
    rating_info: Optional[GeneralRating] = None