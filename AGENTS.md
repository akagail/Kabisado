# AGENTS.md — Kabisado

Primary instruction file for all AI coding agents working in this repository.
Read this file completely before doing anything. When this file conflicts with a
scoped `AGENTS.md` or an approved specification, stop and ask a human.

---

## 1. Project purpose

Kabisado is an AI-assisted examination preparation platform. The first target is
the Philippine Civil Service Examination (CSE); the data model and product design
must allow additional examinations later.

The repository is currently in its **engineering foundation** phase. Product
features must not be implemented until their specification is approved.

## 2. Technology stack

| Layer | Technology | Notes |
| --- | --- | --- |
| Frontend | Next.js (App Router), React, TypeScript, Tailwind CSS, shadcn/ui | `frontend/` |
| Backend | Python, Django, Django REST Framework | `backend/` |
| Database | PostgreSQL | SQLite only for isolated local/test fallback |
| Cache / queue | Redis, Celery | Wired when the first async feature is approved |
| AI | Provider-independent adapter + RAG | No provider SDK in business logic |
| Files | S3-compatible object storage | Presigned uploads/downloads |
| Tests | Pytest, Vitest, Playwright | See `docs/engineering/testing-strategy.md` |
| Infra | Docker, Docker Compose, GitHub Actions, Vercel (frontend) | Backend host not selected |
| Deploy | Modular monolith | No microservices without an approved ADR |

Version pins live in `backend/requirements*.txt` and `frontend/package.json`.
Do not upgrade major versions as part of an unrelated ticket.

## 3. Architecture summary

- **Modular monolith:** one Django project, one Next.js application.
- **Backend modules:** `accounts`, `catalog`, `materials`, `questions`,
  `practice`, `analytics`, `ai`, `core`. Modules communicate through service
  functions, not by importing each other's internals.
- **Frontend:** App Router; server components by default; client components only
  where interactivity requires them.
- **API:** REST under `/api/v1/`; OpenAPI is the contract between frontend and
  backend.
- **Async work:** document extraction, embedding, and AI generation run in Celery
  workers, never in request handlers.
- **AI:** all model calls go through the adapter in `backend/apps/ai/`; prompts
  are versioned files, not inline strings scattered through the codebase.
- **Files:** the browser uploads directly to object storage using a presigned
  URL issued by the API. File bytes do not pass through Next.js serverless
  functions or the Django API.

Read `docs/architecture/system-architecture.md` before changing module
boundaries or data flow.

## 4. Required reading order

Before implementation:

1. This file.
2. The nearest scoped `AGENTS.md` (`frontend/`, `backend/`, `infrastructure/`).
3. The ticket in `tickets/ready/` or `tickets/in-progress/`.
4. The approved specification in `docs/specifications/`.
5. The technical design and relevant ADRs in `docs/architecture/`.
6. Existing code, tests, and migrations in the affected module.

If any of these are missing, stop and report the gap instead of guessing.

## 5. Workflow

### Before touching code

1. Confirm the task has a ticket and an approved specification. If not, create
   the documentation first or ask a human.
2. List every place the change must reach: callers, tests, fixtures, config,
   exports, migrations, docs.
3. Identify user-facing or data-destructive risks.
4. For anything non-trivial, post a short plan: files, approach, tests, risks.
5. Confirm the ticket is in `tickets/in-progress/` (move it there).

### During implementation

1. Stay inside the approved scope. Record newly discovered work as a new ticket;
   do not silently expand.
2. Follow `docs/engineering/coding-standards.md`.
3. Add or update tests in the same change.
4. Add migrations for model changes; never edit an applied migration.
5. Update documentation when behaviour, architecture, or configuration changes.
6. Keep the diff reviewable. Do not refactor unrelated code.

### After implementation

1. Run the checks listed in §13.
2. Verify every acceptance criterion explicitly.
3. Review for security, data loss, and regressions.
4. Update the ticket checklist and move it to `tickets/review/`.
5. Summarize changed files, decisions, validation output, and remaining risks.
6. Never mark a ticket complete while criteria or required checks are unmet.

## 6. Documentation rules

Documentation is part of the product, not an afterthought.

| Change | Required documentation |
| --- | --- |
| New feature | Specification + technical design (if non-trivial) + ticket |
| Architecture change | ADR in `docs/architecture/decisions/` |
| API change | OpenAPI schema update + changelog note in the spec |
| New env var | `docs/operations/environment-variables.md` + `.env.example` |
| New dependency | Justification in the PR and, if significant, an ADR |
| New background job | Architecture doc + failure/retry behaviour |
| Schema change | Migration + `docs/architecture/database-design.md` if conceptual |
| Security-relevant change | `docs/engineering/security-guidelines.md` update if policy changes |

Rules:

- Status labels: `Draft`, `Proposed`, `Approved`, `Superseded`.
- Every document has an owner, status, and last-updated date at the top.
- Do not present assumptions as confirmed requirements. Use
  `**Assumption:**`, `**Recommendation:**`, or `**Needs approval:**`.
- No empty placeholder documents. If a document has no content yet, do not
  create it.

## 7. Ticket and specification workflow

Lifecycle: `BACKLOG → READY → IN PROGRESS → REVIEW → COMPLETED`.

A ticket is **READY** only when it has: ID, type, priority, description,
business justification, in-scope, out-of-scope, dependencies, acceptance
criteria, implementation checklist, testing checklist, and references.

A significant feature needs an approved specification before implementation.
Approval is a human action. Agents may draft, never self-approve.

GitHub Issues and the `Kabisado` project board mirror local tickets. The local
file stays authoritative and stores the issue URL. Follow
`docs/engineering/github-workflow.md`; never create a second issue for a ticket.

See `tickets/README.md`, `tickets/TEMPLATE.md`, and
`docs/specifications/README.md`.

## 8. Naming conventions

### Python / Django

- Modules and packages: `snake_case`.
- Classes: `PascalCase`.
- Functions, variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Django apps: plural nouns (`accounts`, `materials`, `questions`).
- Models: singular nouns (`Material`, `Question`, `PracticeSession`).
- Services: `<verb>_<noun>` (`create_practice_session`).
- Tests: `test_<behaviour>.py`, functions `test_<expected>_when_<condition>`.
- API paths: plural, kebab-case (`/api/v1/practice-sessions/`).

### TypeScript / React

- Files: `kebab-case.ts` / `kebab-case.tsx`; components `PascalCase`.
- Hooks: `use<Thing>`.
- Types/interfaces: `PascalCase`; no `I` prefix.
- Server actions: `verbNounAction`.
- Route segments: `kebab-case`.
- Environment variables exposed to the browser must start with `NEXT_PUBLIC_`
  and must never contain secrets.

### Git

- Branches: `<type>/<ticket-id>-<short-slug>` (e.g. `feat/KAB-012-auth`).
- Commits: Conventional Commits, e.g. `feat(auth): add login endpoint`.
- Ticket IDs: `KAB-###`.

## 9. Directory ownership

| Path | Owns | Must not |
| --- | --- | --- |
| `frontend/` | UI, client state, API consumption, frontend tests | Contain business rules or direct DB/AI access |
| `backend/` | Domain logic, API, persistence, AI orchestration, jobs | Render product UI or hold frontend-only config |
| `infrastructure/` | Dockerfiles, deployment assets, IaC | Contain application logic or secrets |
| `docs/` | Requirements, architecture, standards, specs, plans | Be used as a scratchpad |
| `tickets/` | Local ticket state | Become a second conflicting source of truth |
| `.github/` | CI, issue/PR templates | Contain production credentials |

## 10. API conventions

- Base path: `/api/v1/`; breaking changes require a new version.
- JSON only. Field names `snake_case` in the API; TypeScript types mirror them
  or convert explicitly at one boundary.
- Resource-oriented URLs; verbs only for non-CRUD actions
  (`POST /practice-sessions/{id}/submit/`).
- Use DRF serializers for validation. Never trust client-supplied ownership IDs.
- Errors use a stable envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request could not be processed.",
    "fields": {"email": ["Enter a valid email address."]}
  }
}
```

- List endpoints are paginated. Default page size 20, maximum 100.
- Timestamps are ISO 8601 UTC. IDs are UUIDs.
- Every endpoint declares permissions explicitly; default deny.
- Document every endpoint in the OpenAPI schema and cover it with a test.
- No secrets, internal stack traces, or provider payloads in error responses.

## 11. Database rules

- PostgreSQL is the source of truth; SQLite is a local/test fallback only.
- UUID primary keys (`uuid.uuid4`), `created_at` / `updated_at` on all domain
  tables.
- Use `on_delete=PROTECT` for reference data, `CASCADE` only for owned child
  rows, `SET_NULL` for optional attribution.
- Add indexes for foreign keys and documented query paths, not speculatively.
- Every schema change ships with a migration in the same PR.
- Migrations must be reversible or explicitly documented as irreversible.
- Run `python manage.py makemigrations --check --dry-run` in CI.
- Never edit a migration that has been applied outside local development.
- Destructive migrations require a ticket, a backup plan, and human approval.
- AI-generated content is stored with its source, model, prompt version, and
  generation timestamp. Never overwrite source material.

## 12. Frontend ↔ backend integration

- The browser calls the API through the same-origin `/api` proxy described in
  `docs/architecture/frontend-architecture.md`; do not scatter absolute backend
  URLs through components.
- Shared types should be generated from or checked against OpenAPI; do not
  hand-maintain duplicate contracts.
- Server components fetch on the server; client components use the shared API
  client. One client module owns base URL, auth, error mapping, and retries.
- Uploads use presigned URLs; do not proxy file bytes through Next.js.
- Loading, empty, error, and unauthorized states are required for every data
  view.
- No business logic in components. Validation mirrors the server but the server
  remains authoritative.

## 13. Required checks

Run from the repository root before review.

**Backend**

```bash
cd backend
ruff format --check .
ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
pytest
```

**Frontend**

```bash
cd frontend
npm run lint
npm run typecheck
npm test -- --run
npm run build
```

**End-to-end** (when the change touches a user flow):

```bash
cd frontend
npx playwright test
```

If a check cannot run in the current environment, say so explicitly in the PR
and ticket. Never claim a check passed when it was not executed.

## 14. Testing requirements

- Business logic, permissions, data integrity, and critical workflows require
  tests. New non-trivial logic without a test is incomplete.
- Backend: Pytest + `pytest-django`; factories over large fixtures.
- Frontend: Vitest + Testing Library for components and hooks.
- E2E: Playwright for authentication, upload, practice, and results flows.
- AI behaviour: deterministic unit tests around the adapter and prompt
  assembly; evaluation datasets for model quality, not live API calls in CI.
- Every bug fix includes a regression test that fails before the fix.
- Do not assert on implementation details when behaviour can be asserted.
- No real personal data, API keys, or production dumps in tests.

## 15. Security requirements

- Secrets only through environment variables; never commit `.env` files.
- Validate uploads by extension, MIME type, magic bytes, and size. Store outside
  the web root; serve through short-lived signed URLs.
- Enforce object-level authorization on every read and write.
- Treat uploaded documents and AI output as untrusted input.
- Never interpolate untrusted text into system prompts without delimiting and
  instruction hierarchy.
- Rate-limit authentication, upload, and AI endpoints.
- Do not log passwords, tokens, full documents, or unnecessary PII.
- Use parameterized queries / the ORM. No string-built SQL.
- Keep dependencies patched; CI and Dependabot must pass before release.
- Report suspected vulnerabilities privately to the maintainer, not in a public
  issue.

Full policy: `docs/engineering/security-guidelines.md`.

## 16. Dependency management

- Prefer the standard library and existing project dependencies.
- A new dependency needs a one-line justification in the PR: what it replaces,
  maintenance status, license, and security surface.
- Pin application dependencies; use lockfiles (`package-lock.json`,
  `requirements.txt` with compatible-release pins).
- No dependency for a few lines of code that can be written clearly.
- Paid services or dependencies with ongoing cost require human approval.
- Run audits before adding: `npm audit`, `pip-audit` (when configured).

## 17. Git, review, and CI

- `main` is protected; no direct pushes.
- Short-lived branches from `main`; rebase or merge `main` before review.
- One logical change per PR; link the ticket.
- PRs require: description, ticket link, test evidence, risk notes, and a
  self-review. Squash merge unless history justifies otherwise.
- Required CI checks: backend, frontend, and e2e for user-flow changes.
- Do not force-push shared branches. Do not rewrite published history.
- Deployment is not automatic to production. See `docs/engineering/ci-cd.md`.

## 18. Definition of Done

A ticket is done only when all are true:

- [ ] Acceptance criteria verified.
- [ ] Code implements only the approved scope.
- [ ] Tests added/updated and passing.
- [ ] Required checks in §13 pass.
- [ ] No new security or data-integrity risk left unaddressed.
- [ ] Migrations included and checked.
- [ ] Documentation updated.
- [ ] Ticket checklist completed and moved to `tickets/completed/`.
- [ ] PR reviewed and merged.
- [ ] Follow-up work captured as tickets.

## 19. Prohibited practices

- Implementing features without an approved specification.
- Self-approving a spec, ADR, scope change, or release.
- Committing secrets, credentials, real user data, or production dumps.
- Editing applied migrations or deleting data without approval.
- Adding microservices, queues, caches, or infrastructure without a documented
  reason.
- Calling an AI provider directly from views, components, or Celery tasks
  outside the adapter.
- Storing provider API keys in code, prompts, or the database.
- Copying copyrighted review material into the repository without a recorded
  licence or permission.
- Fake test results, fabricated citations, or claiming unexecuted validation.
- Marking a ticket complete while criteria, tests, or docs are missing.
- Large unrelated refactors bundled into a feature PR.
- `--no-verify`, disabling tests, or suppressing lint rules to make CI pass
  without a documented reason.

## 20. Approval gates

Stop and ask a human before:

1. Finalizing a major architecture decision or ADR.
2. Adding a framework, managed service, or dependency with ongoing cost.
3. Selecting a production hosting provider.
4. Activating production deployment.
5. Changing the approved MVP scope.
6. Implementing examination features.
7. Any destructive repository or data operation.
8. Pushing to a remote for the first time or changing repository settings.

For each gate, present: decision, options, recommendation, trade-offs, risks,
and what happens after approval.

## 21. When uncertain

Ask. A short blocking question is cheaper than an incorrect implementation.
State what you know, what you assumed, and what you need decided. Do not invent
requirements, providers, credentials, or validation results.
