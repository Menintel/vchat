"""Message CRUD operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.schemas.message import MessageCreate


async def get_message(db: AsyncSession, message_id: uuid.UUID) -> Message | None:
    """Get a message by ID."""
    result = await db.execute(select(Message).where(Message.id == message_id))
    return result.scalar_one_or_none()


async def get_messages_by_room(
    db: AsyncSession,
    room_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> list[Message]:
    """Get messages in a room, ordered by creation time."""
    result = await db.execute(
        select(Message)
        .where(Message.room_id == room_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def create_message(
    db: AsyncSession,
    message_in: MessageCreate,
    sender_id: uuid.UUID,
) -> Message:
    """Create a new message."""
    message = Message(
        text=message_in.text,
        room_id=message_in.room_id,
        sender_id=sender_id,
    )
    db.add(message)
    await db.flush()
    await db.refresh(message)
    return message


async def delete_message(db: AsyncSession, message: Message) -> None:
    """Delete a message."""
    await db.delete(message)
    await db.flush()
