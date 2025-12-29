"""Room model."""

import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Room(Base, UUIDMixin, TimestampMixin):
    """Room model for VChat."""

    __tablename__ = "rooms"

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Foreign keys
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    creator = relationship("User", back_populates="rooms", lazy="selectin")
    messages = relationship(
        "Message", back_populates="room", lazy="selectin", cascade="all, delete-orphan"
    )
    attendees = relationship(
        "Attendee", back_populates="room", lazy="selectin", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Room {self.name}>"
