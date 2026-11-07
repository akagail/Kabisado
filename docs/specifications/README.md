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
| SPEC-0001 | Accounts & Profile | Draft | KAB-101 |
| SPEC-0002 | CSE Catalogue | Draft | KAB-102 |
| SPEC-0003 | Question Bank & Review | Draft | KAB-103 |
| SPEC-0004 | Practice & Results | Draft | KAB-104 |
| SPEC-0005 | Progress Analytics & Weak Topics | Draft | KAB-105 |

All MVP specs are **Draft** — awaiting Phase 3 final approval before implementation.

## Required content

Use [`docs/templates/feature-specification.md`](../templates/feature-specification.md).
At minimum: problem, goals, non-goals, users/permissions, flows, edge cases,
error states, data, API, security, acceptance criteria, out of scope, rollout.

## Rules

- Acceptance criteria must be testable.
- Do not silently expand scope during implementation.
- Link the spec from the ticket and the PR.
- Update the spec if behaviour changes during implementation; record why.
