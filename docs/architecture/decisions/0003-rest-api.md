# ADR-0003: REST API with Django REST Framework

**Status:** Approved
**Date:** 2026-11-06
**Approved:** 2026-11-07
**Deciders:** Engineering
**Supersedes:** none

## Context

The frontend and backend are separate deployments. We need a stable contract that
is easy to document, test, and consume from Next.js, and that supports future
clients (mobile, partners).

## Decision

Use a **versioned REST API** implemented with Django REST Framework:

- Base path `/api/v1/`.
- JSON request/response bodies.
- Resource-oriented URLs; explicit action endpoints for non-CRUD operations.
- OpenAPI 3 schema generated with `drf-spectacular`.
- Pagination, filtering, and ordering are explicit and allowlisted.
- A single error envelope for all failures.
- Breaking changes require `/api/v2/`; additive changes are allowed in v1.

## Alternatives considered

| Option | Why not now |
| --- | --- |
| GraphQL | Adds schema/resolver complexity and caching challenges for little MVP benefit |
| tRPC | Couples the API to TypeScript and prevents non-Next.js clients |
| Django server-rendered templates | The product needs a modern interactive study UI and a separate frontend deployment |
| gRPC | Poor browser support and unnecessary for CRUD |

## Consequences

Positive:

- Mature tooling, authentication, permissions, and admin.
- Clear contract and generated schema.
- Easy to test with `APIClient` and Playwright.

Negative:

- Over-fetching/under-fetching is possible; endpoints may need composition.
- Client types must be generated or kept in sync.
- Versioning discipline is required.

## Approval

Requires human approval.
