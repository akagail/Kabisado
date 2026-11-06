# ADR-0002: Initial Technology Stack

**Status:** Proposed
**Date:** 2026-11-06
**Deciders:** Engineering, Product
**Supersedes:** none

## Context

The product brief proposes Next.js, Django, PostgreSQL, Redis, Celery, S3, and
provider-independent AI. We need concrete initial versions and a policy for
upgrades so the repository is reproducible.

## Decision

Adopt the following initial stack:

| Layer | Choice |
| --- | --- |
| Frontend | Next.js 16 (App Router), React 19, TypeScript 5.x/7.x as installed, Tailwind CSS 4 |
| UI | shadcn/ui, copied into the repo |
| Backend | Python 3.13, Django 5.2 LTS, Django REST Framework 3.18 |
| Database | PostgreSQL 17 |
| Vectors | pgvector (when RAG lands) |
| Queue | Celery + Redis 7 (when async work lands) |
| Files | S3-compatible object storage |
| Tests | Pytest, Vitest, Playwright |
| CI | GitHub Actions |
| Local | Docker Compose, npm, pip/venv |
| Frontend hosting | Vercel |
| Backend hosting | Not selected |

Version policy:

- Pin exact versions in lockfiles/manifests.
- Patch/minor upgrades are routine; major upgrades need a ticket and CI pass.
- Django stays on an LTS line; do not adopt a feature release without an ADR.
- Node uses an active LTS line in CI even if local Node is newer.

## Alternatives considered

| Option | Why not now |
| --- | --- |
| Next.js Pages Router | App Router is the current default and supports server components |
| Django 6.x feature release | LTS gives a longer support window; revisit at the next LTS |
| FastAPI | The brief selects Django/DRF; admin and auth are useful for a small team |
| Separate vector DB | pgvector is sufficient at MVP scale |
| SQLite in production | Concurrency and operational needs require PostgreSQL |

## Consequences

- The team must maintain two runtimes (Node and Python).
- Django admin provides a fast back office.
- Vercel's serverless model constrains long-running frontend work; uploads and
  AI are handled by the backend/workers.
- `pgvector` requires a Postgres extension available in the chosen provider.

## Approval

Requires human approval, especially the Django LTS and Node LTS choices.
