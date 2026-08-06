from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_fallback

from app.models.db import get_session
from app.models.scooter import Scooter
from app.schemas.parking import ParkingLotCreated, Parkinglot
from app.schemas.scooter import ScooterCreate
from app.models.user import User
from app.schemas.rides import RidesCreate, RideSuccess, RideEnd
from app.service.auth2_service import get_user_by_token
from app.service.renting_service import get_rides, rent_scooter_start, end_renting, create_scooter_admin, \
    create_parkinglot

router = APIRouter()

@router.get("/", response_model=RidesCreate | tuple)
async def get_rides_router(
        current_user: User = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_session)
):
    return await get_rides(current_user, session)

@router.post("/start", response_model=RideSuccess | tuple)
async def create_ride_router(
        scooter_id: int,
        current_user: User = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_session)
):
 return await rent_scooter_start(scooter_id, current_user, session)

@router.post("/end", response_model=RideEnd | tuple)
async def end_ride_router(
        scooter_id: int,
        lat: float,
        lng: float,
        current_user: User = Depends(get_user_by_token),
        session: AsyncSession = Depends(get_session)
):
    return await end_renting(scooter_id, lat, lng, current_user,session)

@router.post("/scooter", response_model=ScooterCreate | tuple)
async def create_scooter_router(
        session: AsyncSession = Depends(get_session),
        admin: User = Depends(get_user_by_token)
):
    return await create_scooter_admin(session, admin)

@router.post("/parking", response_model=ParkingLotCreated | tuple)
async def create_parking_router(
        point_wkt: Parkinglot,
        session: AsyncSession = Depends(get_session),
        admin: User = Depends(get_user_by_token)
):
    return await create_parkinglot(point_wkt, session, admin)