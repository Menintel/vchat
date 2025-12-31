"""Room API endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.core.livekit import generate_room_token
from app.core.config import get_settings
from app.crud import room_crud
from app.schemas.room import RoomCreate, RoomResponse, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["rooms"])
settings = get_settings()


@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_in: RoomCreate,
    user_id: uuid.UUID = Query(..., description="ID of the user creating the room"),
    db: AsyncSession = Depends(get_db),
) -> RoomResponse:
    """Create a new room."""
    room = await room_crud.create_room(db, room_in, user_id)
    return RoomResponse.model_validate(room)


@router.get("/", response_model=list[RoomResponse])
async def list_rooms(
    skip: int = 0,
    limit: int = 100,
    public_only: bool = False,
    db: AsyncSession = Depends(get_db),
) -> list[RoomResponse]:
    """List all rooms."""
    rooms = await room_crud.get_rooms(
        db, skip=skip, limit=limit, public_only=public_only
    )
    return [RoomResponse.model_validate(r) for r in rooms]


@router.get("/user/{user_id}", response_model=list[RoomResponse])
async def list_user_rooms(
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[RoomResponse]:
    """List rooms created by a specific user."""
    rooms = await room_crud.get_rooms_by_user(db, user_id, skip=skip, limit=limit)
    return [RoomResponse.model_validate(r) for r in rooms]


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> RoomResponse:
    """Get a room by ID."""
    room = await room_crud.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return RoomResponse.model_validate(room)


@router.patch("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: uuid.UUID,
    room_in: RoomUpdate,
    db: AsyncSession = Depends(get_db),
) -> RoomResponse:
    """Update a room."""
    room = await room_crud.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    room = await room_crud.update_room(db, room, room_in)
    return RoomResponse.model_validate(room)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a room."""
    room = await room_crud.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    await room_crud.delete_room(db, room)


@router.post("/{room_id}/join")
async def join_room(
    room_id: uuid.UUID,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Join a room and get a LiveKit access token.

    Requires authentication via Firebase token.
    """
    # Verify room exists
    room = await room_crud.get_room(db, room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )

    # Get user info from Firebase token
    participant_identity = current_user["uid"]
    participant_name = current_user.get("name") or current_user.get(
        "email", "Anonymous"
    )

    # Generate LiveKit token
    token = generate_room_token(
        room_name=str(room_id),
        participant_identity=participant_identity,
        participant_name=participant_name,
    )

    return {
        "token": token,
        "livekit_url": settings.livekit_url,
        "room": RoomResponse.model_validate(room),
        "participant_identity": participant_identity,
        "participant_name": participant_name,
    }
