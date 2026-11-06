# KAB-001: Initialize the Agentic Engineering Kit

**Status:** REVIEW
**Type:** task
**Priority:** P0
**Epic:** E0 Foundation
**Owner:** Engineering
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (foundation)
**Related ADRs:** ADR-0001 … ADR-0006
**GitHub issue:** https://github.com/akagail/Kabisado/issues/30

## 1. Description

Create the documentation-first, ticket-driven engineering foundation for
Kabisado: agent instructions, product documentation, architecture, ADRs,
standards, templates, initial backlog, CI, Docker Compose, and minimal
application scaffolds with health checks.

## 2. Business justification

Future development must be traceable, reviewable, testable, and safe for both
human and AI contributors. Without this foundation, product work would begin
without agreed scope, architecture, or quality gates.

## 3. Scope

In:

- Root `AGENTS.md`, scoped agent instructions, README, CONTRIBUTING.
- Product overview, users, requirements, CSE reference, MVP scope, roadmap.
- System/frontend/backend/database/AI architecture and six ADRs.
- Coding, git, testing, CI/CD, security, documentation standards and DoD.
- Specification, ADR, design, plan, test-plan, ticket, and PR templates.
- Ticket lifecycle, epics, and initial backlog.
- Local development, environment, and deployment docs.
- Minimal Next.js and Django scaffolds with health endpoints.
- GitHub Actions: backend CI, frontend CI, E2E.
- Dockerfiles and `compose.yaml`.

Out:

- Any examination feature.
- Authentication implementation.
- AI provider integration.
- Production deployment activation.
- Hosting/provider selection.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| Empty repository | prerequisite | resolved |
| Stack proposal in brief | decision input | used as proposed |
| Human approval of ADRs/MVP | decision | pending KAB-002 |

## 5. Acceptance criteria

- [x] Repository structure exists and contains no empty placeholder documents.
- [x] Root and scoped agent instructions exist and are internally consistent.
- [x] Product, architecture, engineering, operations, and ticket docs exist.
- [x] Six ADRs are drafted with status `Proposed`.
- [x] Reusable templates exist for specs, designs, ADRs, plans, tests, tickets,
      and PRs.
- [x] Initial backlog is small, prioritized, and dependency-aware.
- [x] CI workflows exist for backend, frontend, and E2E.
- [x] Docker Compose and Dockerfiles exist for local development.
- [x] Minimal scaffolds expose health endpoints and pass their checks.
- [ ] Human review of the initialization report.

## 6. Implementation checklist

- [x] Create root files and directory structure.
- [x] Write agent instructions and standards.
- [x] Write product and architecture documentation.
- [x] Write ADRs and templates.
- [x] Create ticket lifecycle and initial tickets.
- [x] Scaffold backend and frontend.
- [x] Add CI and local container setup.
- [ ] Address review feedback.

## 7. Testing checklist

- [x] Backend lint, Django checks, migration check, Pytest.
- [x] Frontend lint, typecheck, Vitest, production build.
- [x] Playwright E2E passes locally (1 test, Chromium).
- [ ] Docker Compose smoke test (Docker unavailable in the initialization
      environment; must be run by a human or CI with Docker).

## 8. Validation evidence

Recorded in `docs/plans/initialization-report.md`. Do not claim checks that were
not executed.

## 9. Risks and notes

- The repository is not yet pushed to GitHub; CI has not run remotely.
- Docker was unavailable during initialization, so the Compose stack is
  unvalidated at runtime.
- ADRs and MVP scope require human approval before product work.

## 10. References

- `docs/plans/initialization-report.md`
- `AGENTS.md`
- `docs/architecture/`
- `tickets/EPICS.md`
