import random
from datetime import datetime, tzinfo

import app.config as config

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parking import Parking
from app.models.rides import Rides
from app.models.scooter import Scooter, ScooterStatus
from app.models.user import User
from app.schemas.parking import Parkinglot


async def get_rides(current_user: User, session: AsyncSession):
    query = select(Rides).where(Rides.user_id == current_user.id)
    result = await session.execute(query)
    rides = result.scalars().all()

    if rides is None:
        raise HTTPException(status_code=404, detail="No rides found")

    return rides

async def rent_scooter_start(
        scooter_id: int,
        current_user: User,
        session: AsyncSession
):
    scooter_q = select(Scooter).where(Scooter.id == scooter_id)
    scooter_f = await session.scalar(scooter_q)
    if scooter_f is None:
        raise HTTPException(status_code=404, detail="Scooter not found")

    if scooter_f.is_in_use == ScooterStatus.AVAILABLE:
        new_ride = Rides(
            user_id=current_user.id,
            scooter_id=scooter_id,
            cost=None
        )
        scooter_f.is_in_use = ScooterStatus.RENTED
        #stmt = update(Scooter).where(Scooter.id == u_scooter.id).values(is_in_use = ScooterStatus.RENTED)
        session.add(new_ride)
        await session.commit()
        await session.refresh(new_ride)

        return {
            "message": "Ride successfully rented",
            "ride_id": new_ride.id,
            "start_time": new_ride.start_time,
        }
    else:
        raise HTTPException(status_code=404, detail="Scooter is not available or need to be served")


async def end_renting(
        scooter_id: int,
        lat: float,
        lng: float,
        current_user: User,
        session: AsyncSession
):
    rides_q = select(Rides).where(
        Rides.scooter_id == scooter_id,
        Rides.user_id == current_user.id,
        Rides.end_time.is_(None)
    )
    ride = await session.scalar(rides_q)

    if not ride:
        raise HTTPException(status_code=404, detail="Active ride not found")

    point_wkt = f'SRID=4326;POINT({lng} {lat})'

    parking_q = select(Parking).where(
        func.ST_Contains(
            Parking.area,
            func.ST_GeomFromText(point_wkt)
        )
    ).limit(1)

    zone = await session.scalar(parking_q)
    is_in_parking = zone is not None

    aware_date = ride.start_time.replace(tzinfo=None)

    duration = datetime.now() - aware_date

    PRICE_PER_MINUTE = config.PRICE_PER_MINUTE
    PENALTY_FEE = config.PENALTY_FEE

    total_cost = int(duration.total_seconds()/60) * PRICE_PER_MINUTE

    if not is_in_parking:
        total_cost += PENALTY_FEE

    ride.end_time = datetime.now()
    ride.cost = total_cost

    scooter_q = select(Scooter).where(Scooter.id == scooter_id)
    scooter = await session.scalar(scooter_q)

    scooter.is_in_use = ScooterStatus.AVAILABLE
    scooter.coordinates = point_wkt

    await session.commit()

    return {
        "message": "Ride successfully ended",
        "duration": duration.total_seconds()/60,
        "is_in_parking": is_in_parking,
        "cost": total_cost,
    }

async def create_scooter_admin(session: AsyncSession, admin: User):
    """todo: authorization admin. now we have only authentification"""
    lat, lng = random.uniform(52.2200, 52.2400), random.uniform(21.0000, 21.0300)
    point_wkt = f'SRID=4326;POINT({lng} {lat})'
    new_scooter = Scooter(
        battery_level=100,
        is_in_use=ScooterStatus.AVAILABLE,
        coordinates=point_wkt,
    )

    session.add(new_scooter)
    await session.commit()
    await session.refresh(new_scooter)

    return {
        "battery_level": new_scooter.battery_level,
        "is_in_use": new_scooter.is_in_use,
        "id": new_scooter.id,
    }

async def create_parkinglot(point_wkt: Parkinglot, session: AsyncSession, admin: User) :
    """"todo: the same as above (create_scooter_admin)"""
    if point_wkt.points[0] != point_wkt.points[-1]:
        point_wkt.points.append(point_wkt.points[0])

    wkt_points_list = [f"{lng} {lat}" for lat, lng in point_wkt.points]
    wkt_points_str = ", ".join(wkt_points_list)
    polygon_wkt = f'SRID=4326;POLYGON(({wkt_points_str}))'

    new_parkinglot = Parking(
        name=point_wkt.name,
        area=polygon_wkt
    )

    session.add(new_parkinglot)
    await session.commit()
    await session.refresh(new_parkinglot)

    return {
        "message": "Parking successfully created",
        "name": new_parkinglot.name,
        "id": new_parkinglot.id
    }