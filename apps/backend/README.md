# VChat Backend (FastAPI)

This is a minimal FastAPI scaffold for the VChat project.

## Run locally
1. Create and activate a virtual environment:

```sh
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Unix
source .venv/bin/activate
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

3. Start the server (development):

```sh
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Endpoints:
- `GET /health` — health check
- `GET /api/rooms` — sample read-only rooms list

Notes:
- When ready, replace the sample room handler with Firestore or your DB access in `app/main.py`.
- Add CI or Dockerfile as needed for deployment.
