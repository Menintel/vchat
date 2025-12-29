from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="VChat Backend (FastAPI)")

class Room(BaseModel):
    id: str
    name: str
    description: str = ""

# Simple health endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Read-only endpoint returning sample rooms
@app.get("/api/rooms", response_model=List[Room])
async def get_rooms():
    # Replace this with a real DB call when backend auth/db is configured
    return [
        {"id": "1", "name": "General", "description": "General discussion"},
        {"id": "2", "name": "Check-in", "description": "Event check-ins"},
    ]
