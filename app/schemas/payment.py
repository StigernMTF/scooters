from pydantic import BaseModel

class PaymentBase(BaseModel):
    card_number: str
    card_expiration_date: str
    card_CVC: str

class PaymentResponse(PaymentBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True