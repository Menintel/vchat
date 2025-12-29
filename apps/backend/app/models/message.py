"""Message model."""

import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Message(Base, UUIDMixin, TimestampMixin):
    """Message model for VChat."""

    __tablename__ = "messages"

    text: Mapped[str] = mapped_column(Text, nullable=False)

    # Foreign keys
    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Relationships
    room = relationship("Room", back_populates="messages", lazy="selectin")
    sender = relationship("User", back_populates="messages", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Message {self.id} in room {self.room_id}>"
