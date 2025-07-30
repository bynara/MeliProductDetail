from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from .general_rating import GeneralRating
from .payment_method import PaymentMethodSchema
from .category import CategorySchema

class ProductSchema(BaseModel):
    """Schema representing a product."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str
    price: float
    images: List[str]
    seller_id: int
    payment_methods_ids: List[int]
    stock: int
    category_ids: List[int]
    categories: Optional[List[CategorySchema]] = None
    payment_methods: Optional[List[PaymentMethodSchema]] = None
    features: Optional[Dict[str, Any]] = None
    rating_info: Optional[GeneralRating] = None
