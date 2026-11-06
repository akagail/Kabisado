# Initialization Report

**Status:** Review
**Owner:** Engineering
**Last updated:** 2026-11-06
**Ticket:** KAB-001

## 1. Purpose

Record what the engineering foundation contains, what was actually validated,
what was not, and which decisions still need a human before product work starts.
This report is evidence, not a marketing summary: anything not executed is listed
as not executed.

## 2. Starting point

| Item | Finding |
| --- | --- |
| Local repository | Directory existed and was empty; no git repository |
| Remote | `https://github.com/akagail/Kabisado.git` existed and was empty |
| Node / npm | Node 26, npm 10.8 |
| Python | 3.13.1 |
| Git | 2.46 |
| Docker | Not installed; Compose could not be executed |

No secrets, credentials, user data, or third-party review material were present
or added.

## 3. What was created

### Repository root

- `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.gitignore`, `.editorconfig`,
  `.gitattributes`, `.env.example`.

### Documentation (`docs/`)

- `product/`: overview, users, requirements, CSE reference, MVP scope, roadmap.
- `architecture/`: system, frontend, backend, database, AI architecture; six
  Proposed ADRs; decision index.
- `engineering/`: coding standards, git workflow, testing strategy, CI/CD,
  security guidelines, documentation standards, definition of done.
- `operations/`: local development, environment variables, deployment.
- `specifications/`: process and README.
- `templates/`: specification, technical design, ADR, implementation plan,
  test plan, product requirements.
- `plans/`: this report.

### Tickets (`tickets/`)

- Lifecycle README, template, `EPICS.md`, and 17 tickets:
  - `review/`: KAB-001 (this work).
  - `ready/`: KAB-002 approvals, KAB-003 providers, KAB-004 content sourcing,
    KAB-005 threat model.
  - `backlog/`: KAB-101 … KAB-112 across accounts, catalogue, questions,
    practice, analytics, materials, AI, flashcards, observability,
    accessibility/performance, and deployment.
- `in-progress/` and `completed/` exist with `.gitkeep` so the documented
  lifecycle has a real location.

### Application scaffolds

- `backend/`: Django 5.2 project with modular app layout, environment-driven
  settings, SQLite fallback, UUID base model, error envelope, pagination,
  `/api/v1/health/live/`, `/api/v1/health/ready/`, `/api/v1/` root, OpenAPI
  schema endpoint, and four tests.
- `frontend/`: Next.js 16 App Router, React 19, Tailwind 4, TypeScript strict,
  landing page with status and non-affiliation notice, same-origin `/api` rewrite
  proxy, Vitest + Testing Library, Playwright config.
- No examination feature, authentication flow, upload, or AI call is
  implemented.

### Infrastructure and automation

- `infrastructure/docker/`: backend and frontend Dockerfiles.
- `compose.yaml` for local PostgreSQL/backend/frontend.
- GitHub Actions: `backend-ci.yml`, `frontend-ci.yml`, `e2e.yml`.
- Issue forms, pull request template, Dependabot configuration.

## 4. Validation evidence

Executed locally on Windows on 2026-11-06.

### Backend

| Command | Result |
| --- | --- |
| `ruff format --check .` | Pass — 22 files already formatted |
| `ruff check .` | Pass — all checks passed |
| `python manage.py check` | Pass — no issues |
| `python manage.py makemigrations --check --dry-run` | Pass — no changes detected |
| `pytest` | Pass — 4 passed |

`pytest` emits three `UserWarning: No directory at: backend/staticfiles/`
warnings because `STATIC_ROOT` is not populated locally. They are harmless and
do not indicate a failing check; production and CI must run `collectstatic`.

### Frontend

| Command | Result |
| --- | --- |
| `npm run lint` | Pass — no warnings |
| `npm run typecheck` | Pass |
| `npm test -- --run` | Pass — 1 test file, 1 test |
| `npm run build` | Pass — static `/` and `/_not-found` |
| `npx playwright test` | Pass — 1 Chromium test against the dev server |

`npm run build` rewrote `frontend/tsconfig.json`, changing `jsx` from `preserve`
to `react-jsx`. This is Next.js's expected generated value and is kept.

### Not executed

| Check | Reason |
| --- | --- |
| Docker Compose smoke test | Docker is not installed. The Compose stack is structurally reviewed but has never run. |
| GitHub Actions | The repository has not been pushed; no workflow has run remotely. |
| `pip-audit` | Not configured; see `docs/engineering/security-guidelines.md`. |

### Dependency audit

`npm audit` reports 8 moderate-severity advisories, all in the development-only
ESLint/TypeScript-ESLint chain (`minimatch` via `typescript-eslint`). There are
no high or critical advisories, and the packages do not ship to the browser.
`npm audit fix --force` would downgrade `eslint-config-next` from 16.4.5 to
15.5.29, a semver-major downgrade; it was not applied. Track the upstream fix and
re-audit when `typescript-eslint` releases a patched `minimatch` range.

## 5. Decisions recorded as proposed

These are documented, not approved:

- **ADR-0001** Modular monolith.
- **ADR-0002** Django + DRF REST API under `/api/v1/`.
- **ADR-0003** Next.js App Router with the browser using a same-origin proxy.
- **ADR-0004** Session authentication through the same-origin proxy.
- **ADR-0005** Provider-independent AI adapter with RAG.
- **ADR-0006** Presigned S3-compatible uploads.

Provisional versions (Django 5.2 LTS, DRF 3.18, Next.js 16, React 19,
PostgreSQL 17, Node 24–26, Python 3.13) are pinned in the dependency files and
treated as a starting point, not a permanent commitment.

## 6. Open decisions requiring a human

| Gate | Decision needed | Recommendation |
| --- | --- | --- |
| Architecture | Approve or amend ADR-0001 … ADR-0006 | Approve as Proposed, then change status to Approved |
| MVP scope | Approve increments and launch examination | Approve CSE-only MVP; keep other exams out until after launch |
| Authentication | Session vs token, registration policy, verification | Session auth via same-origin proxy (ADR-0004) |
| Providers | AI provider, object storage, backend host | Decide in KAB-003 with cost and data-residency notes |
| Hosting | Production backend host and frontend hosting | Do not select yet; Vercel frontend is a proposal only |
| Deployment | Activate production deployment | Not yet; requires KAB-112 |
| Repository | First push and branch protection | Push after this report is reviewed |
| Content | Source and licence of question bank | Decide in KAB-004 before any content is added |

## 7. Known gaps

- The Compose stack has not run; expect small fixes on first execution.
- No GitHub issue exists for KAB-001 until the first push; `tickets/` remains the
  local source of truth and GitHub issues must link back to ticket IDs.
- `docs/product/cse-reference.md` cites official CSC pages but every format
  detail must be re-verified against the current bulletin before content work.
- Accessibility and performance have standards but no automated checks yet;
  KAB-111 covers this.

## 8. Recommended next actions

1. Human review of this report and the six ADRs.
2. Approve or amend MVP scope (KAB-002).
3. Select providers and record costs (KAB-003).
4. Run the Compose stack on a machine with Docker; record the result in KAB-001.
5. Push the repository, enable branch protection, and open the first issues from
   `tickets/ready/`.
