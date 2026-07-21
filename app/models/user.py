from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.models.Payment import Payment
from app.models.base_models import Base


class User(Base):
    __tablename__ = "user_acc"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_card: Mapped[List["Payment"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"