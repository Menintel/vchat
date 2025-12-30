# VChat Project Plan — Video Conferencing Platform 🎥

> **Last Updated:** 2025-12-30  
> **Status:** Planning Phase — Major Architecture Redesign

---

## Target Project Structure

```
VChat/
│
├── apps/
│   ├── web/                          # Vue 3 Frontend
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── main.ts           # App bootstrap
│   │   │   │   └── router.ts         # Vue Router config
│   │   │   │
│   │   │   ├── pages/
│   │   │   │   ├── Login.vue         # Auth pages
│   │   │   │   ├── Register.vue
│   │   │   │   ├── Lobby.vue         # Room browser / create
│   │   │   │   └── Room.vue          # Video conference room
│   │   │   │
│   │   │   ├── components/
│   │   │   │   ├── conference/
│   │   │   │   │   ├── VideoGrid.vue
│   │   │   │   │   ├── ParticipantTile.vue
│   │   │   │   │   └── ActiveSpeaker.vue
│   │   │   │   │
│   │   │   │   ├── controls/
│   │   │   │   │   ├── MicToggle.vue
│   │   │   │   │   ├── CameraToggle.vue
│   │   │   │   │   ├── ScreenShare.vue
│   │   │   │   │   └── LeaveButton.vue
│   │   │   │   │
│   │   │   │   ├── room/
│   │   │   │   │   ├── RoomCard.vue
│   │   │   │   │   ├── RoomList.vue
│   │   │   │   │   └── CreateRoomModal.vue
│   │   │   │   │
│   │   │   │   └── common/
│   │   │   │       ├── Button.vue
│   │   │   │       ├── Modal.vue
│   │   │   │       └── Navbar.vue
│   │   │   │
│   │   │   ├── livekit/
│   │   │   │   ├── client.ts         # Room connect / disconnect
│   │   │   │   ├── tracks.ts         # Audio/video helpers
│   │   │   │   ├── events.ts         # Participant events
│   │   │   │   └── layout.ts         # Grid / speaker logic
│   │   │   │
│   │   │   ├── firebase/
│   │   │   │   ├── config.ts         # Firebase init
│   │   │   │   └── auth.ts           # Firebase Auth helpers
│   │   │   │
│   │   │   ├── services/
│   │   │   │   ├── auth.service.ts   # Auth business logic
│   │   │   │   ├── room.service.ts   # Room CRUD
│   │   │   │   └── livekit.service.ts # Backend token calls
│   │   │   │
│   │   │   ├── store/
│   │   │   │   ├── auth.store.ts     # Pinia auth state
│   │   │   │   └── room.store.ts     # Pinia room state
│   │   │   │
│   │   │   ├── types/
│   │   │   │   ├── participant.ts
│   │   │   │   ├── room.ts
│   │   │   │   └── user.ts
│   │   │   │
│   │   │   └── styles/
│   │   │       ├── variables.css
│   │   │       └── main.css
│   │   │
│   │   ├── index.html
│   │   ├── vite.config.ts
│   │   ├── tsconfig.json
│   │   └── package.json
│   │
│   └── api/                          # FastAPI Backend
│       ├── app/
│       │   ├── main.py               # FastAPI app
│       │   ├── config.py             # Settings (env vars)
│       │   │
│       │   ├── core/
│       │   │   ├── firebase.py       # Verify Firebase tokens
│       │   │   ├── livekit.py        # JWT generation
│       │   │   └── security.py       # Auth dependencies
│       │   │
│       │   ├── routes/
│       │   │   ├── auth.py           # /auth endpoints
│       │   │   ├── rooms.py          # /rooms + /join
│       │   │   └── health.py         # /health check
│       │   │
│       │   └── schemas/
│       │       ├── room.py
│       │       ├── token.py
│       │       └── user.py
│       │
│       ├── requirements.txt
│       ├── Dockerfile
│       └── pytest.ini
│
├── infra/
│   ├── livekit/
│   │   ├── livekit.yaml              # LiveKit server config
│   │   └── docker-compose.yml        # Local dev setup
│   │
│   ├── nginx/
│   │   └── nginx.conf                # Reverse proxy
│   │
│   └── docker-compose.yml            # Full stack compose
│
├── firebase/
│   ├── firebase.json                 # Firebase project config
│   ├── firestore.rules               # Security rules
│   └── firestore.indexes.json        # Indexes
│
├── .env.example
├── .gitignore
├── pnpm-workspace.yaml               # Monorepo config
├── Makefile
└── README.md
```

---

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Vue 3 | 3.5+ | UI Framework |
| | TypeScript | 5.x | Type Safety |
| | Vite | 6.x | Build Tool |
| | Pinia | 2.x | State Management |
| | Vue Router | 4.x | Navigation |
| | LiveKit Vue | Latest | Video Components |
| **Backend** | FastAPI | 0.115+ | REST API |
| | Python | 3.12+ | Runtime |
| | livekit-api | Latest | Token Generation |
| | firebase-admin | Latest | Token Verification |
| **Video** | LiveKit | 1.8+ | WebRTC SFU |
| **Auth** | Firebase Auth | Latest | User Authentication |
| **Database** | Firestore | Latest | Document DB |
| **Infra** | Docker | Latest | Containerization |
| | NGINX | Latest | Reverse Proxy |

---

## Migration Notes

### Current State
- Simple Firebase-only chat app
- Rooms stored under `users/{uid}/rooms`
- No video conferencing
- No backend API

### Target State
- Full video conferencing with LiveKit
- Public room discovery
- FastAPI backend for token generation
- Docker-based local development

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `pnpm dev` | Start all services |
| `pnpm dev:web` | Start frontend only |
| `pnpm dev:api` | Start backend only |
| `make livekit` | Start LiveKit server |
| `make test` | Run all tests |

---

> **See:** [vchat.md](./vchat.md) for detailed 12-phase implementation plan.