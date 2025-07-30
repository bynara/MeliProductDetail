from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from models.category import Category
from models.general_rating import GeneralRating
from models.payment_method import PaymentMethod
from models.review import Review


class Product(BaseModel):
    id: int
    title: str
    description: str
    price: float
    images: List[str]
    seller_id: int
    payment_methods_ids: List[int]
    stock: int
    category_ids: List[int]
    categories: Optional[List[Category]] = None
    payment_methods: Optional[List[PaymentMethod]] = None
    features: Optional[Dict[str, Any]] = None
    rating_info: Optional[GeneralRating] = None
    reviews: Optional[List[Review]] = None
