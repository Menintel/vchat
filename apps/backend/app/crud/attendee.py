"""Attendee CRUD operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendee import Attendee
from app.schemas.attendee import AttendeeCreate, AttendeeUpdate


async def get_attendee(db: AsyncSession, attendee_id: uuid.UUID) -> Attendee | None:
    """Get an attendee by ID."""
    result = await db.execute(select(Attendee).where(Attendee.id == attendee_id))
    return result.scalar_one_or_none()


async def get_attendee_by_room_and_user(
    db: AsyncSession,
    room_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Attendee | None:
    """Get an attendee by room and user."""
    result = await db.execute(
        select(Attendee).where(
            Attendee.room_id == room_id,
            Attendee.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def get_attendees_by_room(
    db: AsyncSession,
    room_id: uuid.UUID,
    approved_only: bool = False,
) -> list[Attendee]:
    """Get all attendees in a room."""
    query = select(Attendee).where(Attendee.room_id == room_id)
    if approved_only:
        query = query.where(Attendee.approved == True)  # noqa: E712
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_attendee(
    db: AsyncSession,
    attendee_in: AttendeeCreate,
    user_id: uuid.UUID,
) -> Attendee:
    """Create a new attendee (check-in)."""
    attendee = Attendee(
        room_id=attendee_in.room_id,
        user_id=user_id,
        approved=False,
    )
    db.add(attendee)
    await db.flush()
    await db.refresh(attendee)
    return attendee


async def update_attendee(
    db: AsyncSession,
    attendee: Attendee,
    attendee_in: AttendeeUpdate,
) -> Attendee:
    """Update an attendee (e.g., approve)."""
    update_data = attendee_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attendee, field, value)
    await db.flush()
    await db.refresh(attendee)
    return attendee


async def delete_attendee(db: AsyncSession, attendee: Attendee) -> None:
    """Delete an attendee."""
    await db.delete(attendee)
    await db.flush()
