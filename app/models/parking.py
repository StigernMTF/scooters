from typing import Any

from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column

from base import Base

class Parking(Base):
    __tablename__ = 'parking'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)

    area: Mapped[Any] = mapped_column(Geometry(geometry_type='POLYGON', srid=4326, spatial_index=True), nullable=False)

    def __repr__(self) -> str:
        return f"Parking(parking_name={self.name!r}, area={self.area!r})"