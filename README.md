# Kabisado

Kabisado is an AI-assisted examination preparation platform. It starts with the
Philippine Civil Service Examination (CSE) and is designed to extend to
professional licensure, college entrance, government employment, and academic
assessments.

> **Status:** engineering foundation only. No examination features are
> implemented. See [docs/plans/initialization-report.md](docs/plans/initialization-report.md).

## What is in this repository

| Path | Purpose |
| --- | --- |
| `frontend/` | Next.js App Router application (TypeScript, Tailwind CSS, shadcn/ui) |
| `backend/` | Django + Django REST Framework API |
| `infrastructure/` | Dockerfiles and deployment assets; no production provider selected |
| `docs/` | Product, architecture, engineering, specification, plan, and operations docs |
| `tickets/` | Local ticket lifecycle (backlog → ready → in progress → review → completed) |
| `compose.yaml` | Local PostgreSQL + backend + frontend development stack |

## Documentation map

- Start with [`AGENTS.md`](AGENTS.md) if you are an AI agent.
- Humans: [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/product/product-overview.md`](docs/product/product-overview.md).
- Architecture: [`docs/architecture/system-architecture.md`](docs/architecture/system-architecture.md).
- Decisions: [`docs/architecture/decisions/`](docs/architecture/decisions/).
- Local setup: [`docs/operations/local-development.md`](docs/operations/local-development.md).

## Quick start

Prerequisites: Node.js 24+, Python 3.13+, PostgreSQL 17+ (or Docker), Git.

```bash
# Backend
cd backend
python -m venv .venv
.venv/Scripts/activate        # Windows; use source .venv/bin/activate elsewhere
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend
npm ci
npm run dev
```

The frontend runs on `http://localhost:3000`; the API on `http://localhost:8000`.
Full instructions, including Docker Compose, are in
[`docs/operations/local-development.md`](docs/operations/local-development.md).

## Contributing

Work is ticket-driven and specification-first. Read
[`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`docs/engineering/git-workflow.md`](docs/engineering/git-workflow.md) before
opening a pull request.

## License

Not yet selected. Do not add a license without owner approval.
