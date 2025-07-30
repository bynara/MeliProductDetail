from pydantic import BaseModel
from typing import Any, Dict, Optional, List

from .category import CategoryModel



class ProductModel(BaseModel):
    id: int
    title: str
    description: str
    price: float
    images: List[str]
    seller_id: int
    payment_methods_ids: List[int]
    stock: int
    category_ids: List[int]
    categories: Optional[List[CategoryModel]] = None
    features: Optional[Dict[str, Any]] = None