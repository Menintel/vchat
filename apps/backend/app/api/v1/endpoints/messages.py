"""Message API endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import message_crud, room_crud
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    message_in: MessageCreate,
    sender_id: uuid.UUID = Query(..., description="ID of the user sending the message"),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Create a new message in a room."""
    # Verify room exists
    room = await room_crud.get_room(db, message_in.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    message = await message_crud.create_message(db, message_in, sender_id)
    return MessageResponse.model_validate(message)


@router.get("/room/{room_id}", response_model=list[MessageResponse])
async def list_room_messages(
    room_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[MessageResponse]:
    """List messages in a room."""
    # Verify room exists
    room = await room_crud.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    messages = await message_crud.get_messages_by_room(
        db, room_id, skip=skip, limit=limit
    )
    return [MessageResponse.model_validate(m) for m in messages]


@router.get("/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """Get a message by ID."""
    message = await message_crud.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    return MessageResponse.model_validate(message)


@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a message."""
    message = await message_crud.get_message(db, message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )
    await message_crud.delete_message(db, message)
