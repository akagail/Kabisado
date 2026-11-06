# AGENTS.md — Infrastructure

Read the root [`AGENTS.md`](../AGENTS.md) first. This file adds infrastructure
rules; it does not replace the root.

## Scope

- Dockerfiles, `compose.yaml`, local container setup.
- Deployment assets and future IaC.
- CI/CD infrastructure configuration.
- No application logic.

## Current state

- Local Docker Compose only.
- No production hosting provider selected.
- No production credentials exist.
- CD is designed but not active.

## Rules

- Never commit secrets, credentials, `.env` files, or state files.
- Pin base images by version; avoid `latest` in production.
- Run containers as non-root.
- Keep images small and reproducible.
- Use multi-stage builds where they reduce the runtime surface.
- Do not install build tooling in the final image.
- Expose only required ports.
- Add health checks.
- Use named volumes for local persistence; document destructive commands.
- Do not add a service (Redis, queue, proxy) without a ticket and a documented
  reason.
- Production changes require an ADR and human approval.
- Keep local and production topology aligned at the capability level.

## Validation

```bash
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

If Docker is unavailable, say so; do not claim the stack was validated.

## Prohibited

- `docker compose down -v` against non-local data.
- Public database/Redis ports in deployed environments.
- Root containers.
- Secrets in image layers or build args.
- Activating production deployment without approval.
- Copying production data into local containers.
