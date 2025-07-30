

from typing import Dict
from pydantic import BaseModel


class GeneralRating(BaseModel):
    reviews_count: int
    ratings_count: Dict[int, int]
    average_rating: float