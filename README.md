# osu-heatmap

Was, once upon a time, a lightweight web app that fetched osu! user statistics and rendered per-player heatmaps and score summaries across all modes. This repository contains a Python/Flask backend (API + data sync) and a Svelte frontend client.

## Features

- OAuth2 login via osu! (v2)
- Per-user heatmaps for `osu`, `taiko`, `fruits` (catch), and `mania`
- Scheduled background updates of player statistics
- Simple search and profile pages
- Serves the compiled Svelte frontend from the Flask backend in production

## Repo layout

- `backend/` — Flask API, DB models, migration scripts, and scheduling
- `client/` — Svelte frontend (Rollup build)

## Requirements

- Python 3.10+ (for the backend)
- Node.js 16+ and npm (for the frontend)
- MySQL (or compatible) for production database; ensure a compatible DB driver (mysqlclient) is installed
- Redis (default session store at `redis://localhost:6379`)

## Environment variables / configuration

The backend reads configuration from environment variables. Create these in your shell or a `.env` file (and load them before running):

- `CLIENT_ID` — osu! OAuth client id
- `CLIENT_SECRET` — osu! OAuth client secret
- `SESSIONS_SECRET` — secret used for Flask sessions
- `DB_URI` — SQLAlchemy database URI (example: `mysql+mysqldb://user:password@host:3306/dbname`)
- Optionally adjust endpoints in `backend/config/server_config.py` for dev/prod

Redis is expected at `redis://localhost:6379` by default; modify `backend/server.py` if needed.

## Development

Backend

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\\Scripts\\activate      # Windows
# or
source .venv/bin/activate   # macOS / Linux
```

2. Install Python dependencies:

```bash
pip install -r backend/requirements.txt
```

3. Populate environment variables (see section above). Ensure your DB is reachable.

4. Run database migrations (Alembic must be configured with the same env):

```bash
cd backend
alembic upgrade head
```

5. Start the backend (serves built frontend from `client/public`):

```bash
python backend/server.py
```

Frontend

1. Install Node dependencies:

```bash
cd client
npm install
```

2. Development (watch + local server):

```bash
npm run dev
```

This runs Rollup in watch mode and launches `sirv` to serve `public/` (default port 5000). The backend runs separately (default Flask port 5000) — if both listen on the same port in your environment, adjust ports or the `frontend` endpoint in `backend/config/server_config.py`.

Production build

1. From `client/` run:

```bash
npm run build
```

2. Ensure built assets are in `client/public/` and start the backend; the Flask app serves the static files.

## Running the project together

- For production-like local testing: build the frontend, ensure DB and Redis are running, set env vars, run migrations, then start the backend. The backend serves the static files and exposes the API.
- For active development: run frontend `npm run dev` and backend `python backend/server.py` in parallel.
