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
| — | No specifications yet | — | — |

## Required content

Use [`docs/templates/feature-specification.md`](../templates/feature-specification.md).
At minimum: problem, goals, non-goals, users/permissions, flows, edge cases,
error states, data, API, security, acceptance criteria, out of scope, rollout.

## Rules

- Acceptance criteria must be testable.
- Do not silently expand scope during implementation.
- Link the spec from the ticket and the PR.
- Update the spec if behaviour changes during implementation; record why.
