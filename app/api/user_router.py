from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.payment import PaymentResponse, PaymentBase
from app.service.auth2_service import reg_log_token_rotation, get_user_by_token
from app.service.user_service import create_user, add_payment_card, get_user_by_email, user_login, get_my_profile
from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserResponse
from app.models.db import get_session
from app.schemas.jwt_token import Tokens

router = APIRouter()

@router.post("/registration", response_model=Tokens)
async def create_user_router(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    print(f'creating user with data: {user_data}')
    user = await create_user(user_data, session)
    return await reg_log_token_rotation(user, session)


@router.post('/payment', response_model=PaymentResponse)
async def add_payment_card_router(
        payment_data: PaymentBase,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_user_by_token),
):
    return await add_payment_card(payment_data, session, current_user)

@router.post('/login', response_model=Tokens)
async def login_router(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await user_login(user_data, session)
    return await reg_log_token_rotation(user, session)

@router.get('/profile', response_model=UserResponse)
async def get_profile_router(
        current_user: User = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_session),
):
    return await get_my_profile(current_user, session)

@router.get('/{email}', response_model=UserResponse) # ----------------------------------------only workers func xd
async def get_user_by_email_router(email: str, session: AsyncSession = Depends(get_session)):
    return await get_user_by_email(email, session)