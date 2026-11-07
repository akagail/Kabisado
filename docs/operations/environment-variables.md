# Environment Variables

**Status:** Foundation
**Owner:** Engineering
**Last updated:** 2026-11-06

## 1. Rules

- Never commit real values. Commit only `.env.example`.
- Names are `UPPER_SNAKE_CASE`.
- Backend variables are server-only.
- Frontend variables prefixed `NEXT_PUBLIC_` are embedded in the browser bundle.
  Never put a secret there.
- Production values live in the hosting provider's secret store.
- Rotate any value that may have been exposed.
- Fail fast at startup when a required production variable is missing.

## 2. Backend

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `DJANGO_SECRET_KEY` | Yes (prod) | dev-only fallback | Signing key; unique per environment |
| `DJANGO_DEBUG` | No | `false` | Debug mode; must be false in production |
| `DJANGO_ALLOWED_HOSTS` | Yes (prod) | `localhost,127.0.0.1` | Comma-separated hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | No | `FRONTEND_URL` | Comma-separated trusted origins; defaults to the app origin for the same-origin proxy |
| `FRONTEND_URL` | No | `http://localhost:3000` | Base URL used in password-reset links |
| `SESSION_INACTIVITY_SECONDS` | No | `1800` | Sliding inactivity timeout (ADR-0004) |
| `ENABLE_BREACHED_PASSWORD_CHECK` | No | `false` | HIBP k-anonymity validator; enable before alpha |
| `PASSWORD_RESET_TIMEOUT` | No | `259200` | Reset-token lifetime in seconds |
| `DATABASE_URL` | No | SQLite file | PostgreSQL connection URL |
| `REDIS_URL` | No | empty | Celery broker/cache (when enabled) |
| `CORS_ALLOWED_ORIGINS` | No | empty | Only if a cross-origin client is added |
| `EMAIL_BACKEND` | No | console | Django email backend |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USER`, `EMAIL_PASSWORD` | No | empty | Transactional email |
| `DEFAULT_FROM_EMAIL` | No | `noreply@localhost` | Sender address |
| `S3_ENDPOINT_URL` | No | empty | S3-compatible endpoint |
| `S3_REGION` | No | empty | Bucket region |
| `S3_BUCKET` | No | empty | Private bucket name |
| `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY` | No | empty | Storage credentials |
| `AI_PROVIDER` | No | `fake` | Adapter key |
| `AI_BASE_URL` | No | empty | Provider endpoint |
| `AI_API_KEY` | No | empty | Provider secret |
| `AI_MODEL_DEFAULT` | No | empty | Default model |
| `AI_MODEL_CHEAP` | No | empty | Cheaper model for drafts |
| `AI_EMBEDDING_MODEL` | No | empty | Embedding model |
| `AI_EMBEDDING_DIMENSION` | No | `1536` | Must match the model |
| `AI_DAILY_USER_TOKEN_LIMIT` | No | unset | Per-user quota |
| `AI_DAILY_GLOBAL_COST_LIMIT_USD` | No | unset | Global spend cap |
| `SENTRY_DSN` | No | empty | Error reporting (if adopted) |
| `LOG_LEVEL` | No | `INFO` | Root log level |

Example `backend/.env`:

```text
DJANGO_SECRET_KEY=local-only-change-me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:3000
DATABASE_URL=postgres://kabisado:kabisado@localhost:5432/kabisado
```

## 3. Frontend

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `BACKEND_INTERNAL_URL` | Yes | `http://localhost:8000` | Server-side/proxy target; never exposed |
| `NEXT_PUBLIC_APP_URL` | Yes | `http://localhost:3000` | Canonical public URL |
| `NEXT_PUBLIC_API_BASE_PATH` | No | `/api/v1` | Browser API path |
| `NEXT_PUBLIC_SENTRY_DSN` | No | empty | Public error-reporting DSN (if adopted) |

Example `frontend/.env`:

```text
BACKEND_INTERNAL_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_PATH=/api/v1
```

## 4. Compose

`compose.yaml` reads these from the shell or a root `.env`:

| Variable | Default |
| --- | --- |
| `POSTGRES_DB` | `kabisado` |
| `POSTGRES_USER` | `kabisado` |
| `POSTGRES_PASSWORD` | `kabisado` |
| `POSTGRES_PORT` | `5432` |

These are local-only credentials and must never be reused in a deployed
environment.

## 5. Production requirements

Minimum required before a production deploy:

- `DJANGO_SECRET_KEY` (32+ random bytes, unique)
- `DJANGO_DEBUG=false`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL` with TLS
- `S3_*` for uploads
- `EMAIL_*` for verification/reset
- `FRONTEND_URL` (password-reset link origin)
- `ENABLE_BREACHED_PASSWORD_CHECK=true` before public alpha
- AI provider variables if generation is enabled
- `REDIS_URL` if workers are enabled

## 6. Rotation

1. Create the new value in the secret store.
2. Deploy so the app reads it.
3. Verify.
4. Revoke the old value.
5. Record the rotation in the operations log.

For `DJANGO_SECRET_KEY`, rotation invalidates sessions and password-reset tokens;
plan for a re-login.

## 7. Never

- Commit `.env`, `.env.local`, or provider credential files.
- Put a backend secret in a `NEXT_PUBLIC_*` variable.
- Share production secrets in chat, tickets, or screenshots.
- Use the same secret across environments.
- Log environment values at startup.
