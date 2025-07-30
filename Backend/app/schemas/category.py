from pydantic import BaseModel
from typing import Optional

class CategorySchema(BaseModel):
    """Schema representing a product category."""
    id: int
    name: str
    description: Optional[str] = None