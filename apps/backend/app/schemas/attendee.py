"""Attendee schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class AttendeeBase(BaseModel):
    """Base attendee schema."""

    approved: bool = False


class AttendeeCreate(BaseModel):
    """Schema for creating an attendee (check-in)."""

    room_id: uuid.UUID


class AttendeeUpdate(BaseModel):
    """Schema for updating an attendee."""

    approved: bool


class AttendeeResponse(AttendeeBase):
    """Schema for attendee response."""

    id: uuid.UUID
    room_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime  # This is the check-in time

    model_config = {"from_attributes": True}


class AttendeeWithUser(AttendeeResponse):
    """Attendee response with user details."""

    user_name: str | None = None
