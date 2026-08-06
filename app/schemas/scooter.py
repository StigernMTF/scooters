from typing import Any

from pydantic import BaseModel

from app.models.scooter import ScooterStatus

class ScooterCreate(BaseModel):
    battery_level: int
    is_in_use: ScooterStatus
    id: int