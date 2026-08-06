from typing import Any, List

from geoalchemy2 import Geometry, Geography
import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.rides import Rides
from app.models.base import Base

class ScooterStatus(str, enum.Enum):
    AVAILABLE = 'AVAILABLE'
    RENTED = 'RENTED'
    SERVICE = 'SERVICE'


class Scooter(Base):
    __tablename__ = 'scooters'

    id: Mapped[int] = mapped_column(primary_key=True)
    battery_level: Mapped[int] = mapped_column(nullable=False)
    is_in_use: Mapped[ScooterStatus] = mapped_column(nullable=False)

    coordinates: Mapped[Any] = mapped_column(Geography(geometry_type='POINT', srid=4326, spatial_index=True))

    rides: Mapped[List["Rides"]] = relationship(back_populates="scooter")

    def __repr__(self) -> str:
        return f"Scooter(battery_level={self.battery_level!r}, coordinates={self.coordinates!r})"