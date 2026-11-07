# ADR-0001: Modular Monolith over Microservices

**Status:** Approved
**Date:** 2026-11-06
**Approved:** 2026-11-07
**Deciders:** Engineering, Product
**Supersedes:** none

## Context

Kabisado is a new product with a small team, an unproven feature set, and a
modest expected initial load. The domain has clear modules (accounts, catalogue,
materials, questions, practice, analytics, AI), but the boundaries are still
being discovered. Operational capacity is limited.

## Decision

Build a **modular monolith**:

- One Django project, one database, one API deployment.
- One Celery worker deployment (same codebase) for asynchronous work.
- Modules communicate through service functions and selectors.
- Frontend remains a separate Next.js deployment because of its hosting model.

Microservices, separate databases per module, and event streaming are explicitly
out of scope until a measured constraint justifies them.

## Alternatives considered

| Option | Why not now |
| --- | --- |
| Microservices per domain | Distributed transactions, deployments, observability, and local setup cost exceed the team's capacity |
| Serverless functions per endpoint | Cold starts, local parity, and long-running AI jobs are awkward |
| Modular monolith with separate worker | Chosen; keeps request latency low without splitting the domain |

## Consequences

Positive:

- One codebase, one migration path, one local environment.
- Transactions across modules are simple.
- Refactoring boundaries is cheap while the domain is uncertain.
- Lower infrastructure and operational cost.

Negative:

- A deploy affects all modules.
- Poor discipline can erode module boundaries.
- A runaway module can affect the whole API.

Mitigations:

- Enforce module boundaries in review; use services/selectors.
- Keep the AI and extraction work in workers.
- Extract a module only with an ADR and measured evidence.

## Approval

Requires human approval before implementation relies on this decision.
