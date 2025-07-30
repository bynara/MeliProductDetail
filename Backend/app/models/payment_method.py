from pydantic import BaseModel


class PaymentMethodModel(BaseModel):
    id: int
    name: str
    description: str