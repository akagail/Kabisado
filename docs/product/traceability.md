# Traceability — Index Only

**Status:** Current for Phase 3 (2026-11-07)
**Owner:** Product / Engineering
**Last updated:** 2026-11-07

This file is a lightweight index. The authoritative traceability is maintained in:

- **Requirements register:** [product-requirements.md](product-requirements.md) — stable requirement IDs
- **Feature definitions:** [mvp-scope.md](mvp-scope.md) — feature IDs F1–F11 with acceptance criteria
- **Specifications:** [specifications/](../specifications/) — SPEC-0001..0005 map requirements to behaviour and tests
- **Tickets:** [tickets/](../../tickets/) — KAB-101..112 with implementation checklists and verification

Do not maintain a second detailed matrix here. If a requirement has no spec, ticket,
or verification, that is a planning defect to fix in the source documents.

## Specification map (current)

| Spec | Features | Primary tickets | Release |
| --- | --- | --- | --- |
| SPEC-0001 | F1, F2, F11 | KAB-101 | MVP |
| SPEC-0002 | F3 | KAB-102 | MVP |
| SPEC-0003 | F4, F10 | KAB-103 | MVP |
| SPEC-0004 | F5, F6, F7 | KAB-104 | MVP |
| SPEC-0005 | F8, F9 | KAB-105 | MVP |

## Verification key

`U` unit/service, `A` API/integration, `C` component, `E` E2E, `M` manual, `CI` pipeline, `SEC` security.

## Known gaps (to resolve during spec writing)

| # | Gap | Target |
| --- | --- | --- |
| 1 | AUTH-06 email verification has no ticket | KAB-110 (hardening) |
| 2 | ADM-03 account suspension has no owner | KAB-101 or new ticket |
| 3 | Content seeding execution (300 items) | KAB-004 plan → delivery ticket |
| 4 | Flag resolution UI not in KAB-103 acceptance | SPEC-0003 |
| 5 | KAB-104 snapshot acceptance criteria (ADR-0007) | SPEC-0004 |
| 6 | database-design.md SessionItem snapshot fields | SPEC-0004 |
| 7 | Export format | SPEC-0001 |
