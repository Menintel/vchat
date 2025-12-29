"""User model."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin):
    """User model for VChat."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    firebase_uid: Mapped[str | None] = mapped_column(
        String(128), unique=True, nullable=True, index=True
    )

    # Relationships
    rooms = relationship("Room", back_populates="creator", lazy="selectin")
    messages = relationship("Message", back_populates="sender", lazy="selectin")
    attendances = relationship("Attendee", back_populates="user", lazy="selectin")

    def __repr__(self) -> str:
        return f"<User {self.display_name} ({self.email})>"
