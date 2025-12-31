# VChat - Completed Tasks

## Phase 1: Environment Setup ✅
*Completed: December 30, 2025*

### Restructure Monorepo
- Migrated frontend from `apps/frontend` to `apps/web`
- Updated root `package.json` and `Makefile` scripts
- Added pnpm workspace configuration

### TypeScript Migration
- Created `tsconfig.json` and `tsconfig.node.json`
- Added `env.d.ts` for type declarations
- Converted `vite.config.js` to `vite.config.ts`

### State Management
- Added Pinia with `store/index.ts`, `auth.store.ts`, `room.store.ts`
- Created LiveKit client modules: `livekit/client.ts`, `livekit/tracks.ts`

### Docker Infrastructure
- Created `infra/livekit/docker-compose.yml` for LiveKit server
- Created `infra/livekit/livekit.yaml` configuration

### Backend Updates
- Updated `requirements.txt` with `livekit-api`, `firebase-admin`
- Added `core/livekit.py` for token generation
- Updated `core/config.py` with LiveKit settings

---

## Phase 2: Firebase Auth & UI Modernization ✅
*Completed: December 30, 2025*

### Firebase Integration
- Created `firebase/config.ts` - Firebase initialization
- Created `firebase/auth.ts` - Auth service (login, register, Google OAuth, logout)
- Integrated Pinia auth store with Firebase `onAuthStateChanged`

### New Entry Points
- Created `app/main.ts` - TypeScript entry with Pinia
- Created `app/router.ts` - Router with navigation guards
- Added `guestOnly` routes for login/register/home
- Added `requiresAuth` routes for protected pages

### UI Modernization (Dark Theme)
- Created `styles/design-system.css` - Full design system with:
  - Dark purple/blue color palette
  - Glassmorphism effects
  - Custom buttons, inputs, alerts
  - Gradient text utilities

- Redesigned pages:
  - **HomeView** - Hero section with video preview, feature cards
  - **LoginPage** - Modern auth form with Google OAuth button
  - **RegisterPage** - Side-by-side password fields, Google signup
  - **NavigationBar** - Glassmorphism nav with custom logo, user avatar
  - **Lobby** - Room cards with live status, create modal

### Cleanup
- Removed old files: `RoomsPage.vue`, `db.js`, `main.js`, `router/index.js`
- Updated ESLint config for TypeScript support

---

## Phase 3: Code Quality & Security ✅
*Completed: December 30, 2025*

### Biome + lint-staged + Husky
- Installed `@biomejs/biome` for linting/formatting
- Installed `lint-staged` for pre-commit file filtering
- Installed `husky` for Git hooks
- Created `biome.json` configuration
- Created `.husky/pre-commit` hook
- Added npm scripts: `lint`, `lint:fix`, `format`, `check`

### Security Fixes
- Added redirect validation in `LoginPage.vue` to prevent open-redirect attacks
- Updated `initAuthListener` in `firebase/auth.ts` to return unsubscribe function

### Accessibility
- Added `focus-visible` styles for all button variants
- Added `@keyframes badge-pulse` animation in `HomeView.vue`

### Cleanup
- Renamed `Lobby.vue` → `LobbyPage.vue` (multi-word component name)
- Added Firestore `onUnmounted` cleanup with error handling
- Updated ESLint config to allow underscore-prefixed unused vars

---

## Phase 4: Backend LiveKit & Auth Integration ✅
*Completed: December 31, 2025*

### Firebase Auth Backend
- Created `app/core/firebase.py` - Firebase Admin SDK token verification
- Created `app/api/deps.py` - `CurrentUser` auth dependency for protected routes

### LiveKit Token Endpoint
- Created `app/api/v1/endpoints/livekit.py` with:
  - `POST /api/v1/livekit/token` - Generate room access token (auth required)
  - `GET /api/v1/livekit/url` - Get LiveKit server URL

### Room Enhancements
- Added `POST /api/v1/rooms/{id}/join` - Join room and get LiveKit token (auth required)
- Fixed import bug in `core/livekit.py`

---

## Commits

| Hash | Message |
|------|---------|
| `bd447d8` | feat: Phase 1 - environment setup and monorepo restructure |
| `dc00898` | feat: Phase 2 - UI modernization and Firebase auth |
| `latest` | chore: add Biome, lint-staged, Husky + security/accessibility fixes |
