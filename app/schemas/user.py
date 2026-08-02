from pydantic import BaseModel, EmailStr

from app.schemas.jwt_token import Refresh_token
from app.schemas.payment import PaymentResponse
from typing import List, Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: Optional[bool]
    hashed_password: str
    payment_cards: List[PaymentResponse] = []
    ref_token: List[Refresh_token] = []

    class Config:
        from_attributes = True