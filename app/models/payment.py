from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from app.models.user import User
from app.models.base import Base


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_number: Mapped[str] = mapped_column(String(16))
    card_expiration_date: Mapped[str] = mapped_column(String(5))
    card_CVC: Mapped[int] = mapped_column()

    user_id_to_which_belongs: Mapped[int] = mapped_column(ForeignKey("user_acc.id"))
    user: Mapped[User] = relationship(back_populates="payment_cards")

    def __repr__(self) -> str:
        return f"Payment(Id={self.id!r}, user_id_to_which_belongs={self.user_id_to_which_belongs!r})"