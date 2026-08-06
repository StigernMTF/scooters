from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

class RidesBase(BaseModel):
    user_id: int
    scooter_id: int
    cost: float | None

class RidesCreate(RidesBase):
    start_time: datetime
    end_time: datetime

class RideSuccess(BaseModel):
    message: str
    ride_id: int
    start_time: datetime

class RideEnd(BaseModel):
    message: str
    duration: datetime
    is_in_parking: bool
    cost: Decimal