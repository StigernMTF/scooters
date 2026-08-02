from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rides import Rides
from app.models.user import User


async def get_rides(current_user: User, session: AsyncSession):
    query = select(Rides).where(Rides.user_id == current_user.id)
    result = await session.execute(query)
    rides = result.scalars().all()

    if rides is None:
        raise HTTPException(status_code=404, detail="No rides found")

    if not rides:
        return "History of rise is empty"

    return rides