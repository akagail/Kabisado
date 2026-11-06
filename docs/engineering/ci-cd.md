# CI/CD

**Status:** Foundation implemented; deployment not activated
**Owner:** Engineering
**Last updated:** 2026-11-06

## 1. Current pipelines

| Workflow | Trigger | Jobs |
| --- | --- | --- |
| `.github/workflows/backend-ci.yml` | PR/push touching `backend/` | Ruff, Django checks, migration check, Pytest (PostgreSQL) |
| `.github/workflows/frontend-ci.yml` | PR/push touching `frontend/` | npm ci, ESLint, typecheck, Vitest, production build |
| `.github/workflows/e2e.yml` | PR/push touching `frontend/` or `backend/` | Playwright Chromium against a built app |

All workflows run on pull requests to `main` and on pushes to `main`.

## 2. Required checks

Branch protection should require:

- `backend`
- `frontend`
- `e2e` for PRs that change user flows

A check that is skipped because of path filters is not a pass. Configure branch
protection so required checks report success when the relevant paths are
unchanged, or run a lightweight no-op job.

## 3. Backend CI

```yaml
services:
  postgres:
    image: postgres:17
    env:
      POSTGRES_DB: kabisado_test
      POSTGRES_USER: kabisado
      POSTGRES_PASSWORD: kabisado
    ports: ["5432:5432"]
    options: >-
      --health-cmd "pg_isready -U kabisado"
      --health-interval 5s
      --health-timeout 5s
      --health-retries 10
```

Steps:

1. Checkout.
2. Set up Python 3.13 with pip cache.
3. Install `requirements-dev.txt`.
4. `ruff format --check .`
5. `ruff check .`
6. `python manage.py check`
7. `python manage.py makemigrations --check --dry-run`
8. `pytest`

Environment:

```text
DJANGO_SECRET_KEY=ci-only-not-a-real-secret
DJANGO_DEBUG=false
DATABASE_URL=postgres://kabisado:kabisado@localhost:5432/kabisado_test
```

The CI secret is a placeholder, not a production credential.

## 4. Frontend CI

Steps:

1. Checkout.
2. Set up Node 24 with npm cache.
3. `npm ci`
4. `npm run lint`
5. `npm run typecheck`
6. `npm test -- --run`
7. `npm run build`

No secrets are required for the build. If a public build-time variable is needed,
use a non-sensitive placeholder.

## 5. E2E CI

Steps:

1. Checkout.
2. Set up Node 24.
3. `npm ci` in `frontend/`.
4. Install Chromium: `npx playwright install --with-deps chromium`.
5. Start the frontend (Playwright `webServer`) against a stub API or a seeded
   backend, depending on the test.
6. `npx playwright test`.

At the foundation stage the E2E suite covers the static landing page only.
Backend-dependent journeys are added with their features.

## 6. Caching

- Python: `actions/setup-python` with `cache: pip`.
- Node: `actions/setup-node` with `cache: npm` and `cache-dependency-path:
  frontend/package-lock.json`.
- Playwright: cache `~/.cache/ms-playwright` keyed by the Playwright version.
- Do not cache `.next/cache` across unrelated branches.

## 7. Secrets

- Store secrets in GitHub Environments, not repository variables.
- Use separate values for staging and production.
- Never echo secrets in logs.
- Rotate on exposure; assume any committed secret is compromised.
- CI uses placeholder values for tests.
- Do not grant workflows write permissions by default; set
  `permissions: contents: read` and elevate per job only when needed.

## 8. Branch protection recommendations

- Require PRs and one approval.
- Require the checks above.
- Require up-to-date branches.
- Dismiss stale approvals.
- Block force pushes and branch deletion.
- Restrict who can push to `main`.
- Enable secret scanning and Dependabot alerts.

## 9. Deployment design (not activated)

Environments:

| Environment | Frontend | Backend | Data | Trigger |
| --- | --- | --- | --- | --- |
| Local | `next dev` | `runserver` | Compose Postgres | Manual |
| CI | build only | test only | ephemeral Postgres | Push/PR |
| Staging | Vercel preview/production | container host | staging DB/bucket | Manual approval |
| Production | Vercel production | container host | production DB/bucket | Manual approval + tag |

Pipeline design:

1. Build and test on PR.
2. On merge to `main`, build immutable artifacts (frontend deployment, API image
   tagged with the commit SHA).
3. Deploy to staging automatically or with one approval.
4. Run smoke tests against staging.
5. Promote the same artifact to production after manual approval.
6. Run migrations as a separate, explicit step before starting the new API.
7. Verify health/readiness and a smoke journey.
8. Keep the previous image tag for rollback.

Not activated because:

- Production hosting is not selected.
- Credentials and environments are not configured.
- The MVP has no deployable domain yet.
- The owner has not approved production deployment.

## 10. Migrations in deployment

- Run `migrate` once per release, not per replica.
- Use a one-off job or release command.
- Migrations must be backward compatible with the previous app version during
  rollout.
- Destructive changes use expand/contract across releases.
- Back up before destructive migrations.
- If a migration fails, stop the rollout and roll back the app; do not run a
  partial manual fix without a ticket.

## 11. Rollback

- Frontend: promote the previous Vercel deployment.
- Backend: redeploy the previous image tag.
- Database: restore from backup only if the migration is not backward compatible;
  this is a last resort with data-loss implications.
- Document the incident and follow up with a root-cause ticket.

## 12. Failure reporting

- Job names and steps are descriptive.
- Failures print the failing command and a short, non-secret diagnostic.
- Do not upload full environment dumps or document contents.
- Test reports are uploaded as artifacts when useful.
- A red pipeline blocks merge; do not bypass required checks.

## 13. Future additions

- Dependency review and SBOM.
- Container image scanning.
- Secret scanning in CI.
- Lighthouse CI budget.
- Staging smoke tests.
- Deployment approval via GitHub Environments.
- Uptime and error monitoring.

## 14. Open decisions

1. Production backend host and container registry.
2. Staging topology and data seeding.
3. Error-tracking and uptime providers.
4. Whether E2E runs on every PR or on a label.
5. Release cadence and on-call expectations.
