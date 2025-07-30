from pydantic import BaseModel


class PaymentMethod(BaseModel):
    id: int
    name: str
    description: str