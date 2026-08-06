from typing import Any

from pydantic import BaseModel

class Parkinglot(BaseModel):
    name: str
    points: list[tuple[float, float]]

class ParkingLotCreated(BaseModel):
    message: str
    name: str
    id: int