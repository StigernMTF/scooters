from typing import reveal_type

import bcrypt
from fastapi import HTTPException
from pydantic.v1 import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from bcrypt import hashpw

#from app.models import tokens
from app.models.payment import Payment
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.payment import PaymentBase
from app.schemas.jwt_token import Tokens


async def create_user(user_data: UserCreate, session: AsyncSession) -> User:
    password_bytes = user_data.password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password.decode('utf-8'),
        is_active=True
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user, attribute_names=['payment_cards'])
    return new_user

async def user_login(user_data: UserCreate, session: AsyncSession):
    user = await get_user_by_email(email=user_data.email, session=session)

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    provided_pw = user_data.password.encode('utf-8')
    db_hash = user.hashed_password.encode('utf-8')
    if bcrypt.checkpw(provided_pw, db_hash):
        return user
    else:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

async def add_payment_card(
        payment_data: PaymentBase,
        session: AsyncSession,
        current_user: User,
):
    new_payment = Payment(
        card_number=payment_data.card_number,
        card_expiration_date=payment_data.card_expiration_date,
        card_CVC=payment_data.card_CVC,
        user_id=current_user.id
    )
    session.add(new_payment)
    await session.commit()
    await session.refresh(new_payment)

    return new_payment

async def get_user_by_email(email: str, session: AsyncSession):
    query = (
        select(User).where(User.email == email).options(selectinload(User.payment_cards))
    )

    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

async def get_my_profile(user_data: User, session: AsyncSession):
    query = select(User).where(User.id == user_data.id).options(selectinload(User.payment_cards))
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user