"""User schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    display_name: str
    photo_url: str | None = None


class UserCreate(UserBase):
    """Schema for creating a user."""

    firebase_uid: str | None = None


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    display_name: str | None = None
    photo_url: str | None = None


class UserResponse(UserBase):
    """Schema for user response."""

    id: uuid.UUID
    firebase_uid: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
