"""Attendee model."""

import uuid

from sqlalchemy import Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Attendee(Base, UUIDMixin, TimestampMixin):
    """Attendee model for room check-ins."""

    __tablename__ = "attendees"

    approved: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Foreign keys
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Unique constraint: one user can only check in once per room
    __table_args__ = (
        UniqueConstraint("room_id", "user_id", name="uq_attendee_room_user"),
    )

    # Relationships
    room = relationship("Room", back_populates="attendees", lazy="selectin")
    user = relationship("User", back_populates="attendances", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Attendee user={self.user_id} room={self.room_id} approved={self.approved}>"
