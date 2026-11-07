# Kabisado Documentation Index

**Owner:** Engineering / Product
**Last updated:** 2026-11-07

This index explains the purpose of each major document group and where to find
the information you need. Documents cross-link rather than duplicate content.

## Product

| Document | Purpose |
| --- | --- |
| [prd.md](product/prd.md) | **Master product requirements.** Source of truth for problem, goals, requirements (stable IDs AUTH…NFR, AI, etc.) and success metrics. |
| [product-overview.md](product/product-overview.md) | Vision, product principles, MVP summary, key non-goals. |
| [mvp-scope.md](product/mvp-scope.md) | Feature list (F1–F11) with purpose, user story, acceptance criteria, and out-of-scope per feature. |
| [target-users.md](product/target-users.md) | Personas and validation plan. |
| [cse-exam-reference.md](product/cse-exam-reference.md) | Verified CSE examination scope (authoritative source data). |
| [ai-capabilities.md](product/ai-capabilities.md) | **Product-level AI policy** — what AI may do, disclosure, review boundary, quality gates. Implementation details live in [ai-architecture.md](architecture/ai-architecture.md). |
| [product-requirements.md](product/product-requirements.md) | Stable requirement register with IDs, priorities, release mapping. |

## Architecture

| Document | Purpose |
| --- | --- |
| [system-architecture.md](architecture/system-architecture.md) | System context, architectural principles, container diagram, module boundaries. |
| [backend-architecture.md](architecture/backend-architecture.md) | Backend module structure, services, patterns, async boundaries. |
| [frontend-architecture.md](architecture/frontend-architecture.md) | Frontend structure, routing, component patterns, API client. |
| [database-design.md](architecture/database-design.md) | **Canonical database design**: ERD, field tables, constraints, indexes, ownership, migrations. |
| [mvp-data-and-api.md](architecture/mvp-data-and-api.md) | MVP technical requirements, API outline, behavioural rules, data lifecycle. |
| [ai-architecture.md](architecture/ai-architecture.md) | **Technical AI design**: provider adapters, prompts, RAG pipeline, validation, evaluation. Policy lives in ai-capabilities.md. |
| [file-upload-architecture.md](architecture/file-upload-architecture.md) | Presigned upload design (planned). |

## Decisions

| Document | Purpose |
| --- | --- |
| [decisions/README.md](architecture/decisions/README.md) | ADR index with current statuses. |
| [decisions/0001-modular-monolith.md](architecture/decisions/0001-modular-monolith.md) | Approved 2026-11-07. |
| [decisions/0002-technology-stack.md](architecture/decisions/0002-technology-stack.md) | Approved 2026-11-07. |
| [decisions/0003-rest-api.md](architecture/decisions/0003-rest-api.md) | Approved 2026-11-07. |
| [decisions/0004-authentication.md](architecture/decisions/0004-authentication.md) | **Approved** — CSRF via JSON endpoint, session expiry/inactivity, SSR caching, tests (2026-11-07). |
| [decisions/0005-ai-provider-abstraction.md](architecture/decisions/0005-ai-provider-abstraction.md) | Approved in Principle 2026-11-07; conditions apply. |
| [decisions/0006-file-uploads.md](architecture/decisions/0006-file-uploads.md) | **Approved** — ownership, idempotent completion, orphan cleanup, malware scanning (2026-11-07). |
| [decisions/0007-practice-attempt-snapshot.md](architecture/decisions/0007-practice-attempt-snapshot.md) | Approved 2026-11-07 (repository owner delegate). |
| [decisions/0008-exam-version-reuse.md](architecture/decisions/0008-exam-version-reuse.md) | **Draft** — pending approval. |
| [open-decisions.md](decisions/open-decisions.md) | Open decisions O1–O10 (providers, hosting, email, content curation). |

## Specifications

| Document | Purpose |
| --- | --- |
| [specifications/README.md](specifications/specifications-readme.md) | Spec process and SPEC index. |
| [SPEC-0001-accounts-and-profile.md](specifications/SPEC-0001-accounts-and-profile.md) | Accounts, profile, target exam, deletion/export. Ticket KAB-101. |
| [SPEC-0002-cse-catalogue.md](specifications/SPEC-0002-cse-catalogue.md) | CSE catalogue structure. Ticket KAB-102. |
| [SPEC-0003-question-bank-and-review.md](specifications/SPEC-0003-question-bank-and-review.md) | Question bank, review workflow, flags. Ticket KAB-103. |
| [SPEC-0004-practice-and-results.md](specifications/SPEC-0004-practice-and-results.md) | Practice sessions, timed mode, results, snapshots. Ticket KAB-104. |
| [SPEC-0005-progress-analytics-and-weak-topics.md](specifications/SPEC-0005-progress-analytics-and-weak-topics.md) | Progress analytics and rule-based weak-topic diagnosis. Ticket KAB-105. |

## Engineering

| Document | Purpose |
| --- | --- |
| [coding-standards.md](engineering/coding-standards.md) | Language conventions. |
| [testing-strategy.md](engineering/testing-strategy.md) | Testing strategy and verification mapping. |
| [ci-cd.md](engineering/ci-cd.md) | CI pipelines. |
| [security-guidelines.md](engineering/security-guidelines.md) | Security policy. |
| [threat-model.md](engineering/threat-model.md) | Trust boundaries, STRIDE, abuse cases, residual risks (KAB-005). |
| [documentation-standards.md](engineering/documentation-standards.md) | How documentation is maintained and deduplicated. |
| [git-workflow.md](engineering/git-workflow.md) | Branch, commit, PR conventions. |
| [github-workflow.md](engineering/github-workflow.md) | Issue and PR hygiene. |
| [phase-4-clearance-model.md](engineering/phase-4-clearance-model.md) | Staged approval: Category A foundational, B parallel, C release gates. |
| [definition-of-done.md](engineering/definition-of-done.md) | Done criteria. |

## Operations

| Document | Purpose |
| --- | --- |
| [local-development.md](operations/local-development.md) | Local setup. |
| [environment-variables.md](operations/environment-variables.md) | Env var reference. |
| [deployment.md](operations/deployment.md) | Deployment topology and plan. |
| [deployment-hosting-requirements.md](operations/deployment-hosting-requirements.md) | Free-first infra stages, upgrade triggers, provider replacement paths (Draft) |
| [data-map.md](operations/data-map.md) | Personal data inventory, flows, retention, deletion/export (KAB-005). |

## Templates

Reusable document skeletons:

- [feature-specification.md](templates/feature-specification.md)
- [technical-design.md](templates/technical-design.md)
- [adr.md](templates/adr.md)
- [implementation-plan.md](templates/implementation-plan.md)
- [test-plan.md](templates/test-plan.md)
- [product-requirements.md](templates/product-requirements.md)
- [ticket.md](templates/ticket.md)

## Historical

- [plans/archive/](plans/archive/) — Phase 1/2 reports, superseded by current
  plans.

---

Maintainers: update this index in the same change that adds, removes, or moves any
document. Status changes are recorded in the affected document's header and in
the [ADR index](architecture/decisions/README.md).
