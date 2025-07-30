from pydantic import BaseModel, Field
from typing import Optional, Dict

class GeneralRating(BaseModel):
    
    reviews_count: int
    ratings_count: Dict[int, int]  # Dictionary with rating counts (1-5)
    average_rating: float