from datetime import datetime
from uuid import UUID
from typing import TYPE_CHECKING

from sqlalchemy import String, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .refresh_token import RefreshTokenModel
    from .subjects import SubjectModel
    from .revision_cycle import RevisionCycleModel


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
    subjects: Mapped[list["SubjectModel"]] = relationship(
        "SubjectModel", back_populates="user", cascade="all, delete-orphan"
    )
    revision_cycles: Mapped[list["SubjectModel"]] = relationship(
        "RevisionCycleModel", back_populates="user", cascade="all, delete-orphan"
    )
