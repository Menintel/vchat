"""Room schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel


class RoomBase(BaseModel):
    """Base room schema."""

    name: str
    description: str = ""
    is_public: bool = True
    capacity: int | None = None


class RoomCreate(RoomBase):
    """Schema for creating a room."""

    pass


class RoomUpdate(BaseModel):
    """Schema for updating a room."""

    name: str | None = None
    description: str | None = None
    is_public: bool | None = None
    capacity: int | None = None


class RoomResponse(RoomBase):
    """Schema for room response."""

    id: uuid.UUID
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RoomWithCreator(RoomResponse):
    """Room response with creator details."""

    creator_name: str | None = None
