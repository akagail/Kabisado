# Deployment

**Status:** Design only — production deployment not activated
**Owner:** Engineering
**Last updated:** 2026-11-06

## 1. Current state

- Frontend: deployable to Vercel in principle; no project linked.
- Backend: containerizable; no host selected.
- Database, Redis, object storage: no provider selected.
- CI: implemented for validation.
- CD: designed, not active.
- No production credentials exist in this repository.

Do not activate production deployment without owner approval.

## 2. Target topology

```text
Browser
  │ HTTPS
  ▼
Vercel (Next.js)
  │ /api proxy
  ▼
Django API container ──► managed PostgreSQL (+ pgvector)
  │
  ├──► managed Redis ──► Celery worker container
  │                         └──► AI provider
  └──► private S3-compatible bucket
```

Requirements:

- API and worker from the same image, different commands.
- Managed PostgreSQL with point-in-time recovery and the `vector` extension.
- Managed Redis with authentication and private networking.
- Private object storage with lifecycle rules and CORS restricted to the app
  origin.
- TLS everywhere.
- Health checks on `/health/live/` and `/health/ready/`.

## 3. Hosting options (not selected)

| Option | Pros | Cons | Fit |
| --- | --- | --- | --- |
| Railway | Fast setup, managed Postgres/Redis, simple deploys | Less control, cost at scale, regional limits | Good for MVP |
| Render | Managed services, cron/workers, predictable | Cold starts on low tiers, fewer regions | Good for MVP |
| Fly.io | Global regions, containers, volumes | More operational detail, managed DB less turnkey | Good if latency matters |
| AWS ECS + RDS + ElastiCache + S3 | Maximum control, mature | Significant ops and IAM overhead | Later |
| DigitalOcean App Platform | Simple containers + managed DB | Fewer features, region coverage | Viable |
| Self-managed VPS | Cheapest at small scale | Patching, backups, uptime are on us | Not recommended initially |

**Recommendation (pending approval):** a managed container platform with managed
PostgreSQL, Redis, and object storage, selected for the lowest operational burden
that still supports workers, private networking, and backups. Do not choose on
price alone; include on-call cost.

Decision criteria:

- Managed Postgres with pgvector and PITR.
- Background workers and scheduled jobs.
- Private networking and secret management.
- Region close to Philippine users (Singapore or equivalent).
- Predictable egress and storage pricing.
- Exit path (standard containers, standard Postgres, S3 API).

## 4. Environments

| Environment | Purpose | Data | Access |
| --- | --- | --- | --- |
| Local | Development | Synthetic | Developer |
| CI | Automated validation | Ephemeral | CI |
| Staging | Pre-release verification | Synthetic or anonymized | Team |
| Production | Real users | Real | Restricted |

Staging must mirror production topology. It must never share a database, bucket,
Redis instance, or credentials with production.

## 5. Build artifacts

- Frontend: Vercel build from the repository.
- Backend: OCI image tagged with the commit SHA (and a semver tag on release).
- The image is built once and promoted; do not rebuild for production.
- Images run as a non-root user.
- Dependencies are installed from lockfiles/pinned requirements.
- Static files are collected during the image build or release step.

## 6. Release process

1. Merge to `main` with green CI.
2. Build the API image and frontend deployment.
3. Deploy to staging (automatic or one approval).
4. Run migrations on staging.
5. Run smoke tests:
   - health endpoints,
   - register/login,
   - start and submit a practice session,
   - upload a small file (if enabled).
6. Obtain production approval.
7. Back up the production database.
8. Run migrations as a one-off job.
9. Deploy the API, then the worker, then the frontend (or in the order the
   change requires).
10. Verify health and the smoke journey.
11. Tag the release and publish notes.

## 7. Migrations

- Run once per release, not per replica.
- Use a release command or one-off job with the new image.
- Migrations must be backward compatible during rollout.
- Use expand/contract for destructive changes.
- Back up before destructive or large-table migrations.
- If a migration fails, stop; do not manually patch production without a ticket.

## 8. Configuration

- Secrets via the platform's secret store.
- Non-secret config via environment variables.
- `DJANGO_DEBUG=false`.
- `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` set to the real
  domains.
- Session cookie `Secure`.
- Database connections use TLS.
- Object storage bucket is private.
- CORS allows only the frontend origin.

## 9. Static and media files

- Frontend assets are served by Vercel.
- Django admin/static files are served by WhiteNoise or the platform.
- User uploads are never served from the app container; use signed URLs.
- Set far-future caching for hashed static assets; no caching for signed URLs.

## 10. Health, monitoring, and alerts

- Liveness: process responds.
- Readiness: database (and cache, if required) reachable.
- Uptime check every minute.
- Alerts: 5xx rate, p95 latency, queue depth, failed jobs, DB connections, disk,
  AI spend.
- Logs retained per policy; no document contents.
- Error tracking with release/commit tagging.

## 11. Rollback

| Layer | Action |
| --- | --- |
| Frontend | Promote the previous Vercel deployment |
| API/worker | Redeploy the previous image tag |
| Database | Restore only if the migration is not backward compatible; last resort |
| Config | Revert the environment change and restart |

After rollback: verify health, record the incident, and open a root-cause ticket.

## 12. Backup and restore

- Daily automated backups.
- Point-in-time recovery if available.
- Encrypted backups.
- Restore drill before public launch and quarterly thereafter.
- Document the restore procedure and the responsible person.
- Test that account deletion and material deletion propagate to backups per the
  retention policy.

## 13. Security checklist before production

- [ ] HTTPS and HSTS.
- [ ] `DEBUG=false`.
- [ ] Secrets in a secret store, unique per environment.
- [ ] Database and Redis not publicly reachable.
- [ ] Bucket private; CORS restricted.
- [ ] Session and CSRF settings verified.
- [ ] Rate limits enabled.
- [ ] Dependency and image scans pass.
- [ ] Admin access restricted and audited.
- [ ] Backups and restore tested.
- [ ] Privacy policy and terms published.
- [ ] Incident contact documented.

## 14. Launch checklist

- [ ] Hosting provider approved.
- [ ] Domains and DNS configured.
- [ ] Production environment variables set.
- [ ] Migrations applied.
- [ ] Seed data loaded (catalogue only; no fake users).
- [ ] Smoke tests pass.
- [ ] Monitoring and alerts active.
- [ ] Backups verified.
- [ ] Support and takedown process ready.
- [ ] Rollback rehearsed.
- [ ] Release notes published.

## 15. Not yet decided

1. Backend host and region.
2. Container registry.
3. Managed Postgres/Redis/object storage vendors.
4. Email provider.
5. Error tracking and uptime monitoring.
6. Domain names and DNS owner.
7. On-call and incident ownership.
8. Budget ceiling for infrastructure and AI.
