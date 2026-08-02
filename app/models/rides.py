from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

if TYPE_CHECKING:
    from app.models.scooter import Scooter

from base import Base

class Rides(Base):
    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    scooter_id: Mapped[int] = mapped_column(ForeignKey("scooters.id"))

    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)

    scooter: Mapped[Scooter] = relationship(back_populates="rides")