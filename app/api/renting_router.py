from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db import get_session
from app.models.user import User
from app.schemas.rides import RidesBase, RidesCreate
from app.service.auth2_service import get_user_by_token

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/", response_model=RidesCreate)
async def get_rides(
        current_user: User = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_session)
):
    return await get_rides(current_user, session)