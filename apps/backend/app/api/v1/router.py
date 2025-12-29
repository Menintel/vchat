"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import attendees, messages, rooms, users

router = APIRouter(prefix="/api/v1")

router.include_router(users.router)
router.include_router(rooms.router)
router.include_router(messages.router)
router.include_router(attendees.router)
