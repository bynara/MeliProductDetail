from pydantic import BaseModel

class SellerModel(BaseModel):
    id: int
    name: str
    location: str
    email: str
    phone: str