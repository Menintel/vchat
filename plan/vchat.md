# VChat Implementation Plan — 12-Phase Roadmap 🚀

> **Project:** VChat Video Conferencing Platform  
> **Last Updated:** 2025-12-30  
> **Estimated Duration:** 8-12 weeks

---

## Executive Summary

VChat is a Vue 3-based video conferencing platform using **LiveKit** for real-time video/audio, **Firebase** for authentication, and **FastAPI** for backend services. This document outlines a 12-phase implementation plan from requirements through deployment.

---

## Requirements

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | Users can register/login via email or Google OAuth | P0 |
| FR-02 | Users can create public or private video rooms | P0 |
| FR-03 | Users can browse and join available public rooms | P0 |
| FR-04 | Users can share camera, microphone, and screen | P0 |
| FR-05 | Room hosts can manage participants (mute, remove) | P1 |
| FR-06 | Real-time participant status indicators | P1 |
| FR-07 | Text chat alongside video | P2 |
| FR-08 | Room scheduling and invitations | P2 |
| FR-09 | Recording functionality | P3 |
| FR-10 | Virtual backgrounds | P3 |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Video latency | < 300ms |
| NFR-02 | Join time | < 3 seconds |
| NFR-03 | Concurrent participants | 50+ per room |
| NFR-04 | Browser support | Chrome, Firefox, Safari, Edge |
| NFR-05 | Mobile responsive | iOS Safari, Android Chrome |
| NFR-06 | Security | Firebase Auth + HTTPS |

---

## Phase 1: Environment Setup & Monorepo Configuration

**Duration:** 3-4 days  
**Goal:** Establish the development environment and project structure

### Tasks

- [ ] Initialize pnpm workspace monorepo
- [ ] Create `apps/web` with Vite + Vue 3 + TypeScript
- [ ] Create `apps/api` with FastAPI + Python 3.12
- [ ] Configure shared ESLint, Prettier, and TypeScript settings
- [ ] Set up development Docker Compose
- [ ] Create `.env.example` with all required variables
- [ ] Configure Git hooks with Husky + lint-staged

### Key Files

```bash
pnpm-workspace.yaml
apps/web/package.json
apps/web/vite.config.ts
apps/web/tsconfig.json
apps/api/requirements.txt
apps/api/app/main.py
docker-compose.yml
```

### Acceptance Criteria

- [ ] `pnpm install` works from root
- [ ] `pnpm dev:web` starts Vite dev server
- [ ] `pnpm dev:api` starts FastAPI with hot reload
- [ ] ESLint/Prettier run on pre-commit

---

## Phase 2: Firebase Integration & Authentication

**Duration:** 4-5 days  
**Goal:** Implement secure user authentication

### Tasks

- [ ] Create Firebase project and configure Auth providers
- [ ] Implement `firebase/config.ts` with modular SDK
- [ ] Create Pinia auth store with state machine pattern
- [ ] Build Login.vue with email + Google OAuth
- [ ] Build Register.vue with validation
- [ ] Implement Vue Router navigation guards
- [ ] Add loading states and error handling
- [ ] Store user profiles in Firestore

### Key Files

```bash
apps/web/src/firebase/config.ts
apps/web/src/firebase/auth.ts
apps/web/src/store/auth.store.ts
apps/web/src/pages/Login.vue
apps/web/src/pages/Register.vue
apps/web/src/app/router.ts
firebase/firestore.rules
```

### State Machine

```
UNAUTHENTICATED → INITIALIZING → READY (authenticated)
                              → UNAUTHENTICATED (no user)
```

### Acceptance Criteria

- [ ] Users can register with email/password
- [ ] Users can login with Google OAuth
- [ ] Protected routes redirect to login
- [ ] Auth state persists across page refreshes
- [ ] Proper error messages for failed auth

---

## Phase 3: FastAPI Backend Foundation

**Duration:** 3-4 days  
**Goal:** Set up secure backend API for token generation

### Tasks

- [ ] Configure FastAPI app with CORS, logging
- [ ] Implement Firebase token verification middleware
- [ ] Create `/health` endpoint
- [ ] Create `/auth/verify` endpoint
- [ ] Set up Pydantic schemas for request/response
- [ ] Add pytest configuration
- [ ] Create Dockerfile for backend

### Key Files

```bash
apps/api/app/main.py
apps/api/app/config.py
apps/api/app/core/firebase.py
apps/api/app/core/security.py
apps/api/app/routes/auth.py
apps/api/app/routes/health.py
apps/api/app/schemas/user.py
apps/api/requirements.txt
apps/api/Dockerfile
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/auth/verify` | Verify Firebase token |

### Acceptance Criteria

- [ ] API starts and responds to health check
- [ ] Firebase tokens are validated correctly
- [ ] Invalid tokens return 401
- [ ] CORS allows frontend origin

---

## Phase 4: LiveKit Server Setup

**Duration:** 2-3 days  
**Goal:** Deploy and configure LiveKit media server

### Tasks

- [ ] Create LiveKit configuration file
- [ ] Set up Docker Compose for LiveKit
- [ ] Generate API key and secret
- [ ] Configure TURN servers for NAT traversal
- [ ] Test basic room creation via CLI
- [ ] Document local development setup

### Key Files

```bash
infra/livekit/livekit.yaml
infra/livekit/docker-compose.yml
infra/docker-compose.yml
```

### LiveKit Configuration

```yaml
# livekit.yaml
port: 7880
rtc:
  port_range_start: 50000
  port_range_end: 60000
  use_external_ip: true
keys:
  APIxxxxxxxx: <secret>
```

### Acceptance Criteria

- [ ] LiveKit server starts via Docker
- [ ] Can connect from LiveKit CLI
- [ ] Room can be created programmatically
- [ ] API keys are stored securely in .env

---

## Phase 5: LiveKit Token Generation API

**Duration:** 2-3 days  
**Goal:** Backend generates secure room access tokens

### Tasks

- [ ] Install `livekit-api` Python SDK
- [ ] Implement token generation utility
- [ ] Create `/rooms/join` endpoint
- [ ] Create `/rooms/create` endpoint
- [ ] Add participant identity validation
- [ ] Configure token expiration and grants

### Key Files

```bash
apps/api/app/core/livekit.py
apps/api/app/routes/rooms.py
apps/api/app/schemas/room.py
apps/api/app/schemas/token.py
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/rooms/create` | Create room, return token |
| POST | `/rooms/join` | Join room, return token |
| GET | `/rooms` | List available rooms |

### Token Grants

```python
VideoGrants(
    room_join=True,
    room=room_name,
    can_publish=True,
    can_subscribe=True,
    can_publish_data=True
)
```

### Acceptance Criteria

- [ ] Token generates successfully for authenticated users
- [ ] Token includes correct room and identity
- [ ] Token expires after configured duration
- [ ] Proper error handling for missing rooms

---

## Phase 6: Room Management & Lobby UI

**Duration:** 4-5 days  
**Goal:** Users can create, browse, and join rooms

### Tasks

- [ ] Create Lobby.vue with room list
- [ ] Build RoomCard.vue component
- [ ] Build CreateRoomModal.vue component
- [ ] Implement room service for API calls
- [ ] Create Pinia room store
- [ ] Add room filtering (public/private)
- [ ] Implement Firestore for room persistence

### Key Files

```bash
apps/web/src/pages/Lobby.vue
apps/web/src/components/room/RoomCard.vue
apps/web/src/components/room/RoomList.vue
apps/web/src/components/room/CreateRoomModal.vue
apps/web/src/services/room.service.ts
apps/web/src/services/livekit.service.ts
apps/web/src/store/room.store.ts
```

### Room Data Model (Firestore)

```typescript
interface Room {
  id: string;
  name: string;
  hostId: string;
  hostName: string;
  isPublic: boolean;
  maxParticipants: number;
  createdAt: Timestamp;
  activeParticipants: number;
}
```

### Acceptance Criteria

- [ ] Public rooms visible to all authenticated users
- [ ] Users can create new rooms
- [ ] Real-time room list updates
- [ ] Room cards show participant count
- [ ] Private rooms hidden from browse

---

## Phase 7: LiveKit Vue Integration

**Duration:** 5-6 days  
**Goal:** Core video conferencing functionality

### Tasks

- [ ] Install `@livekit/components-vue` and `livekit-client`
- [ ] Create Room.vue with LiveKitRoom component
- [ ] Implement client.ts for room connection
- [ ] Implement tracks.ts for media handling
- [ ] Build VideoGrid.vue with dynamic layout
- [ ] Build ParticipantTile.vue component
- [ ] Handle connection states and errors

### Key Files

```bash
apps/web/src/pages/Room.vue
apps/web/src/livekit/client.ts
apps/web/src/livekit/tracks.ts
apps/web/src/livekit/events.ts
apps/web/src/livekit/layout.ts
apps/web/src/components/conference/VideoGrid.vue
apps/web/src/components/conference/ParticipantTile.vue
apps/web/src/components/conference/ActiveSpeaker.vue
```

### LiveKit Composables

```typescript
// Key composables from @livekit/components-vue
useLiveKitRoom()
useParticipants()
useTracks()
useLocalParticipant()
useRemoteParticipants()
```

### Acceptance Criteria

- [ ] Two users can join same room
- [ ] Video streams display correctly
- [ ] Audio works bidirectionally
- [ ] Connection errors handled gracefully
- [ ] Grid layout adapts to participant count

---

## Phase 8: Media Controls

**Duration:** 3-4 days  
**Goal:** Full control over audio, video, and screen sharing

### Tasks

- [ ] Build MicToggle.vue with mute/unmute
- [ ] Build CameraToggle.vue with enable/disable
- [ ] Build ScreenShare.vue with screen capture
- [ ] Build LeaveButton.vue with confirmation
- [ ] Add device selection dropdowns
- [ ] Implement local preview before join
- [ ] Handle permission errors

### Key Files

```bash
apps/web/src/components/controls/MicToggle.vue
apps/web/src/components/controls/CameraToggle.vue
apps/web/src/components/controls/ScreenShare.vue
apps/web/src/components/controls/LeaveButton.vue
apps/web/src/components/controls/DeviceSelector.vue
apps/web/src/livekit/tracks.ts
```

### Control States

| Control | States |
|---------|--------|
| Microphone | Muted, Unmuted, Unavailable |
| Camera | Off, On, Unavailable |
| Screen | Not Sharing, Sharing |

### Acceptance Criteria

- [ ] Mute/unmute works instantly
- [ ] Camera toggle shows/hides video
- [ ] Screen share works on desktop browsers
- [ ] Proper feedback for denied permissions
- [ ] Device switching works without reconnect

---

## Phase 9: Participant Management

**Duration:** 3-4 days  
**Goal:** Host controls and participant status

### Tasks

- [ ] Build participant list sidebar
- [ ] Implement host controls (mute, remove)
- [ ] Add speaking indicators
- [ ] Show connection quality indicators
- [ ] Implement participant events handling
- [ ] Add participant join/leave notifications

### Key Files

```bash
apps/web/src/components/conference/ParticipantList.vue
apps/web/src/components/conference/ParticipantItem.vue
apps/web/src/components/conference/SpeakingIndicator.vue
apps/web/src/livekit/events.ts
```

### Host Permissions

| Action | Host | Participant |
|--------|------|-------------|
| Mute others | ✅ | ❌ |
| Remove participant | ✅ | ❌ |
| End meeting | ✅ | ❌ |
| Screen share | ✅ | ✅ |

### Acceptance Criteria

- [ ] Participant list shows all users
- [ ] Speaking indicator activates on voice
- [ ] Host can mute any participant
- [ ] Host can remove participants
- [ ] Removed users redirected to lobby

---

## Phase 10: UI Polish & Responsive Design

**Duration:** 4-5 days  
**Goal:** Professional, responsive interface

### Tasks

- [ ] Implement dark/light theme
- [ ] Create mobile-responsive layouts
- [ ] Add animations and transitions
- [ ] Implement toast notifications
- [ ] Add keyboard shortcuts
- [ ] Accessibility audit (a11y)
- [ ] Loading skeletons and states

### Key Files

```bash
apps/web/src/styles/variables.css
apps/web/src/styles/main.css
apps/web/src/styles/themes.css
apps/web/src/components/common/Toast.vue
apps/web/src/components/common/Skeleton.vue
```

### Responsive Breakpoints

| Breakpoint | Layout |
|------------|--------|
| < 640px | Single column, simplified controls |
| 640-1024px | 2-column, compact sidebar |
| > 1024px | Full layout, all features |

### Acceptance Criteria

- [ ] Works on mobile browsers
- [ ] Theme toggle persists
- [ ] All interactions animated
- [ ] WCAG 2.1 AA compliance
- [ ] Keyboard navigation works

---

## Phase 11: Testing & Quality Assurance

**Duration:** 4-5 days  
**Goal:** Comprehensive test coverage

### Tasks

- [ ] Unit tests for stores and services
- [ ] Component tests for key components
- [ ] API integration tests
- [ ] E2E tests for critical flows
- [ ] Performance testing
- [ ] Security audit

### Test Coverage Targets

| Area | Target |
|------|--------|
| Pinia Stores | 90%+ |
| API Routes | 80%+ |
| Components | 70%+ |
| E2E Flows | 100% of critical paths |

### Critical E2E Flows

1. Register → Login → Create Room → Join Room
2. Two users join same room and see each other
3. Screen share starts and is visible to others
4. Host removes participant

### Acceptance Criteria

- [ ] All tests pass in CI
- [ ] No critical security issues
- [ ] Performance meets NFRs
- [ ] Cross-browser testing complete

---

## Phase 12: Deployment & Documentation

**Duration:** 3-4 days  
**Goal:** Production-ready deployment

### Tasks

- [ ] Configure production Docker Compose
- [ ] Set up NGINX reverse proxy
- [ ] Deploy to cloud provider
- [ ] Configure SSL certificates
- [ ] Set up monitoring and logging
- [ ] Write user documentation
- [ ] Create developer README

### Key Files

```bash
infra/nginx/nginx.conf
infra/docker-compose.prod.yml
README.md
docs/CONTRIBUTING.md
docs/DEPLOYMENT.md
```

### Deployment Architecture

```
[Users] → [NGINX (SSL)] → [Frontend (Static)]
                       → [FastAPI]
                       → [LiveKit Server]
```

### Acceptance Criteria

- [ ] Application accessible via HTTPS
- [ ] All services healthy
- [ ] Monitoring alerts configured
- [ ] Documentation complete
- [ ] Rollback procedure documented

---

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| 1. Environment Setup | 3-4 days | — |
| 2. Firebase Auth | 4-5 days | Phase 1 |
| 3. FastAPI Backend | 3-4 days | Phase 1 |
| 4. LiveKit Setup | 2-3 days | Phase 3 |
| 5. Token API | 2-3 days | Phase 4 |
| 6. Room Management | 4-5 days | Phase 2, 5 |
| 7. Video Integration | 5-6 days | Phase 5, 6 |
| 8. Media Controls | 3-4 days | Phase 7 |
| 9. Participant Mgmt | 3-4 days | Phase 7 |
| 10. UI Polish | 4-5 days | Phase 8, 9 |
| 11. Testing | 4-5 days | Phase 10 |
| 12. Deployment | 3-4 days | Phase 11 |

**Total Estimate:** 41-52 days (8-12 weeks)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| LiveKit compatibility issues | Use official Vue components |
| NAT traversal failures | Configure TURN servers |
| Firebase quota limits | Monitor usage, set alerts |
| Browser WebRTC support | Feature detection, fallbacks |
| Scalability | Use LiveKit Cloud for production |

---

## Future Enhancements (Post-MVP)

- [ ] Recording to cloud storage
- [ ] Virtual backgrounds
- [ ] Breakout rooms
- [ ] Waiting room / lobby mode
- [ ] Chat with reactions
- [ ] Whiteboard collaboration
- [ ] Calendar integration
- [ ] Mobile native apps

---

> **Next Step:** Approve this plan and begin Phase 1 — Environment Setup