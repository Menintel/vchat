# VChat — Project Specification 📘

## Overview
**VChat** is a small, Vue-based web application for real-time group chat and event check-ins. It supports rooms, user authentication, attendee check-in, and basic room management. The app uses a Firebase/Firestore backend (inferred from previous commits) to store users, rooms, messages, and attendees.

## Objectives 🎯
- Provide reliable, low-latency chat experience for rooms.
- Allow event organizers to manage check-ins and attendees.
- Secure access to data with authentication and Firestore rules.

## Core features
- **Authentication** — register/login (email + optionally Google OAuth).
- **Rooms** — create, list, join, delete rooms.
- **Chat** — real-time messages per room, message history, timestamps.
- **Check-In / Attendees** — users can check in to an event; organizers can view/delete attendees.
- **Responsive UI** — desktop and mobile support.

## User stories
- As a user, I can register and log in so my identity is saved.
- As a user, I can join a room and see live messages in that room.
- As an organizer, I can view and remove attendees from the check-in list.
- As a user, I see presence indicators and message timestamps.

## Data model (Firestore collections)
- `users`:
  - `uid` (string)
  - `displayName`, `email`, `photoURL` (strings)
  - `createdAt` (timestamp)
- `rooms`:
  - `id`, `name`, `description`, `createdBy`, `createdAt`
  - `capacity` (optional), `isPublic` (boolean)
- `messages` (subcollection under `rooms/{roomId}/messages`):
  - `id`, `senderId`, `text`, `createdAt`
- `attendees` (collection or `rooms/{roomId}/attendees`):
  - `id`, `userId`, `name`, `checkedInAt`

## Security & rules (high level)
- Authenticated users can read public rooms and write messages in rooms they joined.
- Only room creators / organizers can delete rooms or remove attendees.
- Limit message rate per user to prevent abuse (rate limiting at app level).

## UI / Page specifications
- `HomeView` — app intro, login/register CTAs, list of public rooms.
- `LoginPage` / `RegisterPage` — standard auth flows and error handling.
- `RoomsPage` — list of rooms, search, create room modal.
- `ChatPage` — message list, input box, room info, attendee toggle.
- `CheckInPage` — check-in form and organizer controls.

## Components to implement
- `NavigationBar` — top nav, login state, links.
- `RoomList`, `RoomCard` — reusable listing components.
- `ChatMessage`, `MessageList`, `MessageInput` — chat components.
- `AttendeeList`, `CheckInForm` — check-in flow components.

## API / DB access patterns
- Keep DB calls in `src/db.js` with methods: `getRooms()`, `createRoom()`, `getMessages(roomId)`, `sendMessage(roomId, message)`, `getAttendees(roomId)`, `checkIn(roomId, user)`.
- Use Firestore listeners for real-time updates where appropriate.

## Testing strategy
- Unit tests for `src/db.js` (mock Firestore), router guards, and key components.
- E2E tests for flows: register/login, create/join room, send message, check-in.
- CI pipeline: run ESLint, unit tests, build step on PRs.

## Deployment & environment
- Deploy static assets via Netlify/Vercel/GitHub Pages combined with Firebase hosting if needed for cloud functions.
- Keep Firebase config in environment variables / secrets.

## Acceptance criteria (detailed)
- Chat latency: messages appear under 1 second for local tests.
- Data integrity: messages persist and load when a user joins a room.
- Security: Firestore rules deny unauthorized writes/reads.
- UX: Mobile & desktop layouts are usable and accessible.

## Future enhancements
- Reactions, read receipts, file attachments.
- Moderation tools (ban, mute, report).
- Analytics & usage metrics dashboard.

---

> Implementation note: `src/db.js` should be the single point of contact for Firestore and should be mocked during testing. If you want, I can add example Firestore rules and a CI YAML next.