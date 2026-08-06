from typing import Optional, TYPE_CHECKING

from psycopg.types import none
from sqlalchemy import ForeignKey, DateTime, func, Numeric, null
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime

from app.models.user import User

if TYPE_CHECKING:
    from app.models.scooter import Scooter

from app.models.base import Base

class Rides(Base):
    __tablename__ = "rides"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_acc.id"))
    scooter_id: Mapped[int] = mapped_column(ForeignKey("scooters.id"))

    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)

    scooter: Mapped["Scooter"] = relationship(back_populates="rides")
    user: Mapped["User"] = relationship(back_populates="rides")

    def __repr__(self) -> str:
        return f"Rides(user_id={self.user_id!r}, start_time={self.start_time!r}, end_time={self.end_time!r})"