# Project Plan — VChat ✅

## Repository structure (tree)
```
.
├─ .gitignore
├─ eslint.config.js
├─ index.html
├─ jsconfig.json
├─ package.json
├─ package-lock.json
├─ README.md
├─ vite.config.js
├─ public/
│  └─ favicon.ico
├─ plan/
│  ├─ plan.md
│  └─ vchat.md
└─ src/
   ├─ App.vue
   ├─ db.js
   ├─ main.js
   ├─ assets/
   │  ├─ base.css
   │  ├─ main.css
   │  └─ logo.svg
   ├─ components/
   │  ├─ HelloWorld.vue
   │  ├─ NavigationBar.vue
   │  └─ icons/
   │     ├─ IconCommunity.vue
   │     ├─ IconDocumentation.vue
   │     ├─ IconEcosystem.vue
   │     ├─ IconSupport.vue
   │     └─ IconTooling.vue
   ├─ router/
   │  └─ index.js
   └─ views/
      ├─ AboutView.vue
      ├─ ChatPage.vue
      ├─ CheckInPage.vue
      ├─ HomeView.vue
      ├─ LoginPage.vue
      ├─ RegisterPage.vue
      └─ RoomsPage.vue
```

### Intent & usage
- This `plan/plan.md` documents the repo layout and short-to-medium term roadmap. Use it to guide implementation, tests, and deployment.

## Short-term roadmap (next 1–2 weeks) 🔜
1. Finalize `vchat.md` spec (complete). ✅
2. Add developer docs: update `README.md` with run/build/test instructions.
3. Add basic CI: lint, unit tests, build on push (GitHub Actions).
4. Configure deployment (Netlify/Vercel) and add environment variables (Firebase/Secrets).

## Medium-term milestones (1–3 months) 📈
- Authentication (email + OAuth), user profiles.
- Real-time chat & room management (messages, presence, typing indicators).
- Check-in flows and attendee management (organizers vs attendees).
- Polishing UI, accessibility, and mobile responsiveness.

## Tasks & conventions
- Add pre-commit hooks (Husky) and formatting (Prettier + ESLint).
- Use semantic commit messages and feature branches for PRs.
- Keep `src/db.js` as the single DB access point for easier testing.

## Acceptance criteria (examples)
- Users can create/join rooms and exchange messages in real time.
- Organizers can view and delete attendees for check-ins.
- All endpoints are protected with appropriate Firestore rules.

---

> Next step: review `vchat.md` and tell me if you'd like additional diagrams (ER, sequence) or a task breakdown into issues.