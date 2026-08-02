from datetime import datetime

from pydantic import BaseModel

class RidesBase(BaseModel):
    user_id: int
    scooter_id: int
    cost: float | None

class RidesCreate(RidesBase):
    start_time: datetime
    end_time: datetime