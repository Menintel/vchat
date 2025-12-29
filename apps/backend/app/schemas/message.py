"""Message schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class MessageBase(BaseModel):
    """Base message schema."""

    text: str


class MessageCreate(MessageBase):
    """Schema for creating a message."""

    room_id: uuid.UUID


class MessageResponse(MessageBase):
    """Schema for message response."""

    id: uuid.UUID
    room_id: uuid.UUID
    sender_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageWithSender(MessageResponse):
    """Message response with sender details."""

    sender_name: str | None = None
