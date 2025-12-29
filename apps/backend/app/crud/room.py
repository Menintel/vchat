"""Room CRUD operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate


async def get_room(db: AsyncSession, room_id: uuid.UUID) -> Room | None:
    """Get a room by ID."""
    result = await db.execute(select(Room).where(Room.id == room_id))
    return result.scalar_one_or_none()


async def get_rooms(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    public_only: bool = False,
) -> list[Room]:
    """Get a list of rooms."""
    query = select(Room)
    if public_only:
        query = query.where(Room.is_public == True)  # noqa: E712
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_rooms_by_user(
    db: AsyncSession,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Room]:
    """Get rooms created by a specific user."""
    result = await db.execute(
        select(Room).where(Room.created_by == user_id).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def create_room(
    db: AsyncSession, room_in: RoomCreate, user_id: uuid.UUID
) -> Room:
    """Create a new room."""
    room = Room(**room_in.model_dump(), created_by=user_id)
    db.add(room)
    await db.flush()
    await db.refresh(room)
    return room


async def update_room(db: AsyncSession, room: Room, room_in: RoomUpdate) -> Room:
    """Update an existing room."""
    update_data = room_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(room, field, value)
    await db.flush()
    await db.refresh(room)
    return room


async def delete_room(db: AsyncSession, room: Room) -> None:
    """Delete a room."""
    await db.delete(room)
    await db.flush()
