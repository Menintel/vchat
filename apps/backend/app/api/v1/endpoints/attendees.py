"""Attendee API endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import attendee_crud, room_crud
from app.schemas.attendee import AttendeeCreate, AttendeeResponse, AttendeeUpdate

router = APIRouter(prefix="/attendees", tags=["attendees"])


@router.post("/", response_model=AttendeeResponse, status_code=status.HTTP_201_CREATED)
async def check_in(
    attendee_in: AttendeeCreate,
    user_id: uuid.UUID = Query(..., description="ID of the user checking in"),
    db: AsyncSession = Depends(get_db),
) -> AttendeeResponse:
    """Check in to a room."""
    # Verify room exists
    room = await room_crud.get_room(db, attendee_in.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    # Check if already checked in
    existing = await attendee_crud.get_attendee_by_room_and_user(
        db, attendee_in.room_id, user_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in to this room",
        )
    attendee = await attendee_crud.create_attendee(db, attendee_in, user_id)
    return AttendeeResponse.model_validate(attendee)


@router.get("/room/{room_id}", response_model=list[AttendeeResponse])
async def list_room_attendees(
    room_id: uuid.UUID,
    approved_only: bool = False,
    db: AsyncSession = Depends(get_db),
) -> list[AttendeeResponse]:
    """List attendees in a room."""
    # Verify room exists
    room = await room_crud.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    attendees = await attendee_crud.get_attendees_by_room(
        db, room_id, approved_only=approved_only
    )
    return [AttendeeResponse.model_validate(a) for a in attendees]


@router.patch("/{attendee_id}", response_model=AttendeeResponse)
async def update_attendee(
    attendee_id: uuid.UUID,
    attendee_in: AttendeeUpdate,
    db: AsyncSession = Depends(get_db),
) -> AttendeeResponse:
    """Update an attendee (e.g., approve)."""
    attendee = await attendee_crud.get_attendee(db, attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee not found",
        )
    attendee = await attendee_crud.update_attendee(db, attendee, attendee_in)
    return AttendeeResponse.model_validate(attendee)


@router.delete("/{attendee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_attendee(
    attendee_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove an attendee from a room."""
    attendee = await attendee_crud.get_attendee(db, attendee_id)
    if not attendee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendee not found",
        )
    await attendee_crud.delete_attendee(db, attendee)
