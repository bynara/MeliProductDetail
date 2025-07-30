from pydantic import BaseModel

class PaymentMethodSchema(BaseModel):
    """Schema representing a payment method."""
    id: int
    name: str
    description: str

    model_config = {"from_attributes": True}