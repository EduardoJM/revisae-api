from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, DateTime, Enum as SAEnum, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .refresh_token import RefreshTokenModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    refresh_tokens: Mapped[list["RefreshTokenModel"]] = relationship(
        "RefreshTokenModel", back_populates="user", cascade="all, delete-orphan"
    )
