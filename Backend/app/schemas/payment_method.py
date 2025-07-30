from pydantic import BaseModel, ConfigDict

class PaymentMethodSchema(BaseModel):
    """Schema representing a payment method."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    description: str