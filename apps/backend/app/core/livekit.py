from livekit import api
from app.core.config import get_settings

settings = get_settings()


def generate_room_token(
    room_name: str,
    participant_identity: str,
    participant_name: str | None = None,
    can_publish: bool = True,
    can_subscribe: bool = True,
) -> str:
    """
    Generate a LiveKit access token for a participant to join a room.

    Args:
        room_name: Name of the room to join
        participant_identity: Unique identifier for the participant (usually user ID)
        participant_name: Display name for the participant
        can_publish: Whether the participant can publish audio/video
        can_subscribe: Whether the participant can subscribe to other participants

    Returns:
        JWT token string
    """
    token = api.AccessToken(
        api_key=settings.LIVEKIT_API_KEY,
        api_secret=settings.LIVEKIT_API_SECRET,
    )

    token.with_identity(participant_identity)

    if participant_name:
        token.with_name(participant_name)

    token.with_grants(
        api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=can_publish,
            can_subscribe=can_subscribe,
            can_publish_data=True,
        )
    )

    return token.to_jwt()


def create_room(room_name: str) -> None:
    """
    Create a new LiveKit room.

    Note: Rooms are typically created automatically when the first participant joins.
    This function is for explicit room creation if needed.
    """
    room_service = api.RoomServiceClient(
        settings.LIVEKIT_URL.replace("ws://", "http://").replace("wss://", "https://"),
        api_key=settings.LIVEKIT_API_KEY,
        api_secret=settings.LIVEKIT_API_SECRET,
    )
    room_service.create_room(api.CreateRoomRequest(name=room_name))


def list_rooms() -> list:
    """
    List all active LiveKit rooms.
    """
    room_service = api.RoomServiceClient(
        settings.LIVEKIT_URL.replace("ws://", "http://").replace("wss://", "https://"),
        api_key=settings.LIVEKIT_API_KEY,
        api_secret=settings.LIVEKIT_API_SECRET,
    )
    response = room_service.list_rooms(api.ListRoomsRequest())
    return response.rooms
