# AGENTS.md — Backend

Read the root [`AGENTS.md`](../AGENTS.md) first. This file adds backend-specific
rules; it does not replace the root.

## Stack

Python 3.13, Django 5.2 LTS, Django REST Framework, PostgreSQL, Celery/Redis when
async work lands. Tests: Pytest + `pytest-django`.

## Commands

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate        # Windows
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
ruff format --check .
ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
pytest
```

## Module boundaries

```text
apps/core        shared base, health, errors, pagination
apps/accounts    users, profiles, auth
apps/catalog     exam taxonomy
apps/materials   uploads, storage, extraction
apps/questions   questions, choices, flashcards
apps/practice    sessions, responses, scoring
apps/analytics   aggregates
apps/ai          adapters, prompts, RAG, quotas
```

- A module owns its models and migrations.
- Cross-module reads use selectors; writes use services.
- Do not import another app's models in views. If you must, document why.
- `core` must not import domain modules.
- `ai` is the only module allowed to call model providers.

## Layering

```text
view → serializer → service → model/selector
```

- Views: HTTP only.
- Serializers: shape/type validation.
- Services: transactions, permissions, state transitions, side effects.
- Selectors: complex reads.
- Tasks: thin wrappers around services; no business logic.

## API

- Base path `/api/v1/`.
- Default permission `IsAuthenticated`.
- One error envelope; no stack traces.
- Paginate lists; default 20, max 100.
- Object-level authorization in services.
- Update the OpenAPI schema for every endpoint change.
- Test success, validation, unauthenticated, and unauthorized paths.

## Database

- UUID primary keys; `created_at`/`updated_at`.
- Explicit `on_delete` and `related_name`.
- Every schema change ships a migration.
- Never edit an applied migration.
- Additive migrations first; backfill separately.
- Use `select_related`/`prefetch_related`; avoid N+1.
- Destructive changes require approval.

## Async work

- No parsing, embedding, or model call in a request handler.
- Tasks accept IDs, are idempotent, and retry with backoff.
- Do not hold a transaction open across a network call.
- Record job status and error category.

## Security

- Never trust ownership IDs from the request body.
- Validate uploads by type, size, magic bytes, and checksum.
- Do not log secrets, tokens, prompts, or document text.
- Rate-limit auth, upload, and AI endpoints.
- Treat document text and AI output as untrusted.

## Testing

- Factories over fixtures.
- One behaviour per test.
- Freeze time for time-dependent rules.
- Use a fake AI adapter; no live calls in CI.
- Test cross-user access for every resource.
- New non-trivial logic without a test is incomplete.

## Prohibited

- Business logic in views, serializers, models' `save()`, or signals.
- Raw SQL with string interpolation.
- `except:` or silently swallowed errors.
- Committing secrets or local databases.
- Adding Celery/Redis before the first async ticket.
- Calling a provider SDK outside `apps/ai/adapters/`.
