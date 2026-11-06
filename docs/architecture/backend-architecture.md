# Backend Architecture

**Status:** Proposed — requires approval
**Owner:** Backend
**Last updated:** 2026-11-06

## 1. Stack

- Python 3.13
- Django 5.2 LTS
- Django REST Framework 3.x
- PostgreSQL (via `psycopg`)
- Celery + Redis (wired when the first async feature lands)
- Pytest + `pytest-django`
- Ruff for formatting and linting
- `drf-spectacular` for OpenAPI

## 2. Project layout

```text
backend/
├── manage.py
├── pyproject.toml             # ruff, pytest, coverage config
├── requirements.txt
├── requirements-dev.txt
├── config/
│   ├── __init__.py
│   ├── settings.py            # environment-driven
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py              # added with the first async feature
├── apps/
│   ├── core/
│   │   ├── models.py          # TimeStampedModel, UUIDModel
│   │   ├── pagination.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   ├── views.py           # health/readiness
│   │   └── urls.py
│   ├── accounts/
│   ├── catalog/
│   ├── materials/
│   ├── questions/
│   ├── practice/
│   ├── analytics/
│   └── ai/
└── tests/                     # cross-app integration tests only
```

Each app contains:

```text
<app>/
├── __init__.py
├── apps.py
├── models.py
├── selectors.py               # read queries
├── services.py                # write/domain operations
├── serializers.py
├── views.py
├── urls.py
├── permissions.py
├── tasks.py                   # when async work exists
├── admin.py
├── migrations/
└── tests/
    ├── test_models.py
    ├── test_services.py
    └── test_api.py
```

## 3. Layering rules

```text
HTTP request
  → view / viewset        (HTTP concerns only)
  → serializer            (input/output validation and representation)
  → service               (transaction, business rules, permissions)
  → model / selector      (persistence and queries)
```

- **Views** parse the request, call one service or selector, and return a
  response. No ORM queries beyond simple lookups, no business rules.
- **Serializers** validate shape and types. Cross-field business validation
  belongs in the service or a domain validator.
- **Services** own transactions, authorization checks, state transitions, and
  side-effect scheduling. They accept explicit arguments (IDs, DTOs), not raw
  request objects.
- **Selectors** own complex read queries and return querysets or typed rows.
- **Models** own invariants that must always hold, plus simple properties.
- **Tasks** are thin: validate the job payload, call a service, record the
  result. No business logic in tasks.

Example service signature:

```python
def submit_practice_session(*, session_id: UUID, user_id: UUID) -> PracticeSession:
    ...
```

## 4. Module boundaries

| Module | Public surface (examples) |
| --- | --- |
| `accounts` | `register_user`, `get_profile`, `delete_account` |
| `catalog` | `list_exams`, `get_topic_tree`, `seed_cse_catalog` |
| `materials` | `create_upload`, `complete_upload`, `delete_material`, `get_material` |
| `questions` | `select_practice_items`, `create_question`, `approve_question` |
| `practice` | `start_session`, `save_response`, `submit_session`, `get_results` |
| `analytics` | `topic_accuracy`, `weak_topics`, `recent_attempts` |
| `ai` | `generate_summary`, `generate_flashcards`, `generate_questions` |

Rules:

- Import another app's `models` only inside that app or in migrations; elsewhere
  use services/selectors or a narrow documented exception.
- Never create cross-app circular imports. If two modules need each other,
  extract the shared concept into `core` or invert the dependency.
- Foreign keys may cross modules; query logic should not.

## 5. Settings

- One `config/settings.py`, driven by environment variables.
- No environment-specific Python modules; environments differ by values.
- `DEBUG` defaults to `False`; tests set it explicitly.
- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `CORS_ALLOWED_ORIGINS` come from
  env vars.
- Database via `DATABASE_URL`.
- Static files served by WhiteNoise or the platform; uploads never use Django
  `MEDIA_ROOT` in production.
- Fail fast on missing required production variables.
- Secrets are read once at startup; do not scatter `os.environ` access.

## 6. API conventions

- Base path: `/api/v1/`.
- DRF viewsets for resources; `APIView` for actions that do not fit.
- Trailing slashes are required.
- Default permission: `IsAuthenticated`. Public endpoints opt out explicitly.
- Pagination: page-number pagination, default 20, max 100.
- Filtering: explicit query params with validation; no arbitrary field filtering
  until a need exists.
- Ordering: explicit allowlist.
- Errors: one envelope for all 4xx/5xx responses.

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request could not be processed.",
    "fields": {"email": ["Enter a valid email address."]},
    "request_id": "01J..."
  }
}
```

- Validation errors use HTTP 400. Authentication uses 401. Authorization uses
  403. Missing resources use 404. Conflicts use 409. Rate limits use 429.
- Do not leak whether an email exists on login or password reset.
- OpenAPI schema is generated by `drf-spectacular` and checked into the repo or
  published as a build artifact.
- Every endpoint has an API test covering success, validation failure,
  unauthenticated access, and unauthorized access.

## 7. Authentication

Proposed: Django session authentication.

- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/logout/`
- `GET  /api/v1/auth/me/`
- `GET  /api/v1/auth/csrf/`
- `POST /api/v1/auth/password-reset/`
- `POST /api/v1/auth/password-reset/confirm/`

Details:

- Passwords validated with Django's validators plus a breached-password check
  (implementation decision pending).
- Session rotation on login; logout flushes the session.
- CSRF enforced for unsafe methods.
- Login and reset endpoints rate-limited.
- Email enumeration avoided in responses.
- Staff access uses Django admin with `is_staff` and audit logging.

See [ADR-0004](decisions/0004-authentication.md).

## 8. Authorization

- Permissions are checked in services for object-level operations.
- A user may only read/write their own materials, sessions, responses, and
  generated content.
- Catalogue and approved shared questions are readable by authenticated users.
- Staff-only operations use `IsAdminUser` plus an explicit service check.
- Never trust an `owner_id` or `user_id` from the request body.
- Add tests for cross-user access attempts (IDOR).

## 9. Background jobs

When Celery is introduced:

- Broker: Redis. Result backend: disabled unless a result is actually needed.
- Tasks are idempotent and accept IDs, not model instances.
- Retries: exponential backoff with jitter, max 5 attempts for transient errors;
  no retry for validation errors.
- A `JobRun` record stores status, attempts, error category, and timestamps.
- Queues: `extraction`, `embedding`, `generation`, `maintenance`.
- Workers run with `acks_late=True` and a visibility timeout longer than the
  slowest expected task.
- No task holds a database transaction open across a network call.
- Scheduled jobs use Celery Beat with a single scheduler instance.

## 10. Caching

- Do not cache until a measured need exists.
- When added: Redis, explicit keys, versioned prefixes, short TTLs.
- Never cache user-specific responses in a shared key without user scoping.
- Catalogue and topic trees are good first candidates.
- Invalidate on write through the service that performs the write.

## 11. Logging and observability

- Structured JSON logs in non-local environments.
- Include `request_id`, `user_id` (pseudonymous), route, status, and duration.
- Do not log passwords, tokens, document text, or AI prompts containing user
  content.
- Log AI usage as token counts and cost, not prompt bodies.
- Health endpoints:
  - `GET /health/live/` — process is up.
  - `GET /health/ready/` — database (and cache, if required) reachable.
- Errors are reported to an error tracker when selected.

## 12. Testing

- `pytest` with `pytest-django`.
- `factory_boy` for model factories; no large static fixtures.
- Test database: PostgreSQL in CI; SQLite fallback only for a fast local subset.
- Mark slow/integration tests; keep the default suite fast.
- Use `APIClient` for endpoint tests.
- Freeze time for time-dependent rules.
- Every service has unit tests for success, validation, permission, and
  state-transition failures.
- Target ≥ 80% coverage for domain services; 100% for permission and scoring
  branches. Coverage is a signal, not a goal.

## 13. Migrations

- One migration per logical schema change.
- Additive first: add nullable field → backfill → enforce constraint.
- Never edit an applied migration.
- Destructive changes require approval and a backup plan.
- Run `makemigrations --check --dry-run` in CI.
- Test migrations against a production-like dump before release when they touch
  large tables.
- Use `db_index=True` / `Meta.indexes` deliberately.

## 14. Admin

- Django admin is the MVP back office.
- Staff must use named accounts; no shared logins.
- Read-only fields for generated provenance.
- Actions that publish content require a confirmation step.
- Admin changes to questions and catalogue are logged.

## 15. Dependency policy

- Runtime dependencies are pinned with compatible-release specifiers.
- Dev dependencies are separate.
- New dependencies require justification in the PR.
- Do not add a package for a single trivial helper.
- Run `pip-audit` in CI once configured.

## 16. Open decisions

1. Session auth vs. token auth.
2. Breached-password check provider.
3. Whether to use Django admin or a custom back office for content review.
4. Transactional email provider.
5. Error-tracking vendor.
6. Celery result backend requirements.
