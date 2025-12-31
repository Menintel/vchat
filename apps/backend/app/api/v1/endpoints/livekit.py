"""LiveKit token generation endpoint."""

from pydantic import BaseModel, Field
from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.core.livekit import generate_room_token
from app.core.config import get_settings

router = APIRouter(prefix="/livekit", tags=["livekit"])
settings = get_settings()


class TokenRequest(BaseModel):
    """Request body for token generation."""

    room_name: str = Field(..., min_length=1, max_length=100)
    participant_name: str | None = Field(None, max_length=100)


class TokenResponse(BaseModel):
    """Response containing the LiveKit access token."""

    token: str
    livekit_url: str
    room_name: str
    participant_identity: str
    participant_name: str


@router.post("/token", response_model=TokenResponse)
async def get_token(
    request: TokenRequest,
    current_user: CurrentUser,
) -> TokenResponse:
    """
    Generate a LiveKit access token for joining a video room.

    Requires authentication via Firebase token in Authorization header.

    The token allows the user to:
    - Join the specified room
    - Publish audio/video
    - Subscribe to other participants
    """
    # Use user's UID as identity, display name as participant name
    participant_identity = current_user["uid"]
    participant_name = (
        request.participant_name
        or current_user.get("name")
        or current_user.get("email", "Anonymous")
    )

    token = generate_room_token(
        room_name=request.room_name,
        participant_identity=participant_identity,
        participant_name=participant_name,
    )

    return TokenResponse(
        token=token,
        livekit_url=settings.livekit_url,
        room_name=request.room_name,
        participant_identity=participant_identity,
        participant_name=participant_name,
    )


@router.get("/url")
async def get_livekit_url() -> dict:
    """Get the LiveKit server URL for the frontend client."""
    return {"url": settings.livekit_url}
