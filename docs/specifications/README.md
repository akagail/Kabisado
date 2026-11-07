# Specifications

Approved feature specifications live here. A significant feature must not be
implemented without an approved specification.

## Naming

```text
SPEC-NNNN-short-title.md
```

## Lifecycle

`Draft → Proposed → Approved → Superseded`

- Agents may draft and propose.
- Only a human approves.
- Implementation starts only after approval.
- Changes after approval require an amendment section or a new spec.

## Index

| ID | Title | Status | Ticket |
| --- | --- | --- | --- |
| SPEC-0001 | Accounts & Profile | **Approved** (2026-11-07) | KAB-101 |
| SPEC-0002 | CSE Catalogue | **Approved** (2026-11-07) | KAB-102 |
| SPEC-0003 | Question Bank & Review | **Approved** (2026-11-07) | KAB-103 |
| SPEC-0004 | Practice & Results | **Approved** (2026-11-07) | KAB-104 |
| SPEC-0005 | Progress Analytics & Weak Topics | **Approved** (2026-11-07) | KAB-105 |

All MVP specs are **Approved** — Phase 4 implementation may begin per the
staged clearance model in
[phase-4-clearance-model.md](../engineering/phase-4-clearance-model.md).

## Required content

Use [`docs/templates/feature-specification.md`](../templates/feature-specification.md).
At minimum: problem, goals, non-goals, users/permissions, flows, edge cases,
error states, data, API, security, acceptance criteria, out of scope, rollout.

## Rules

- Acceptance criteria must be testable.
- Do not silently expand scope during implementation.
- Link the spec from the ticket and the PR.
- Update the spec if behaviour changes during implementation; record why.
