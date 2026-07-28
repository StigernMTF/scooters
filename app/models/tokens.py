from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.models.base import Base
from app.models.user import User


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_acc.id"))
    expires_at: Mapped[datetime] = mapped_column()
    refresh_token_hashed: Mapped[str] = mapped_column(unique=True)

    user: Mapped[User] = relationship(back_populates="ref_token")

    def __repr__(self) -> str:
        return f"Ref_tokens(Expires_at={self.expires_at!r}, user_id={self.user_id!r})"