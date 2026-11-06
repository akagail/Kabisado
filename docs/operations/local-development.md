# Local Development

**Status:** Foundation
**Owner:** Engineering
**Last updated:** 2026-11-06

## 1. Prerequisites

| Tool | Version | Notes |
| --- | --- | --- |
| Node.js | 24 LTS or newer | `node --version` |
| npm | 10+ | Ships with Node |
| Python | 3.13 | `python --version` |
| PostgreSQL | 17+ | Or use Docker Compose |
| Docker | Current | Optional; not required if Postgres is local |
| Git | Current | |

Windows note: commands below use PowerShell. Use `.venv\Scripts\activate`.
On macOS/Linux, use `source .venv/bin/activate`.

## 2. Repository layout

```text
backend/    Django API
frontend/   Next.js app
docs/       documentation
tickets/    work items
compose.yaml
```

## 3. Environment files

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env
```

Fill in local values. Never commit `.env`. See
[environment-variables.md](environment-variables.md).

## 4. Backend setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is at `http://localhost:8000`.
Health checks:

- `http://localhost:8000/health/live/`
- `http://localhost:8000/health/ready/`

### Database

Default local behavior:

- If `DATABASE_URL` is set, use it.
- Otherwise use `backend/db.sqlite3` for a zero-setup start.

PostgreSQL is required for CI and should be used for any migration or query work:

```powershell
# Start only the database from Compose
docker compose up -d db

# Then set in backend/.env
DATABASE_URL=postgres://kabisado:kabisado@localhost:5432/kabisado
```

SQLite is a convenience, not a substitute for testing PostgreSQL-specific
behavior.

## 5. Frontend setup

```powershell
cd frontend
npm ci
npm run dev
```

The app is at `http://localhost:3000`. It proxies `/api/*` to
`BACKEND_INTERNAL_URL` (default `http://localhost:8000`).

## 6. Docker Compose

```powershell
docker compose up --build
```

Services:

- `db` — PostgreSQL 17 on `localhost:5432`
- `backend` — Django dev server on `localhost:8000`
- `frontend` — Next.js dev server on `localhost:3000`

The stack is for local development only. It uses development settings, bind
mounts, and no production secrets.

To reset local data:

```powershell
docker compose down -v
```

This deletes the local database volume. Do not run it against anything but local
development.

## 7. Tests and checks

```powershell
# Backend
cd backend
ruff format --check .
ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
pytest

# Frontend
cd frontend
npm run lint
npm run typecheck
npm test -- --run
npm run build

# E2E (requires Playwright browsers)
npx playwright install chromium
npx playwright test
```

## 8. Common tasks

### Create a migration

```powershell
cd backend
python manage.py makemigrations <app>
python manage.py migrate
```

Never edit an applied migration.

### Open a Django shell

```powershell
python manage.py shell
```

### Create an admin user

```powershell
python manage.py createsuperuser
```

Admin: `http://localhost:8000/admin/`.

### Add a shadcn component

```powershell
cd frontend
npx shadcn@latest add button
```

Components are copied into `src/components/ui/`. Review the diff before
committing.

### Regenerate the OpenAPI schema

```powershell
cd backend
python manage.py spectacular --file ../docs/api/openapi.yaml
```

(The command is added with the API schema ticket.)

## 9. Troubleshooting

| Symptom | Check |
| --- | --- |
| `ModuleNotFoundError` | Virtualenv active? `pip install -r requirements-dev.txt` |
| Database connection refused | Is Postgres running? Is `DATABASE_URL` correct? |
| CORS/CSRF error | `CSRF_TRUSTED_ORIGINS`, proxy config, CSRF token header |
| Frontend cannot reach API | `BACKEND_INTERNAL_URL` and the `/api` proxy |
| Port already in use | Change the port or stop the other process |
| Playwright browser missing | `npx playwright install chromium` |
| Migration check fails | Run `makemigrations`, review, commit the file |

## 10. What not to do

- Do not commit `.env` or local database files.
- Do not use production credentials locally.
- Do not copy production data into local or test environments.
- Do not disable tests or lint to get a local run green.
- Do not run `docker compose down -v` unless you accept deleting local data.
