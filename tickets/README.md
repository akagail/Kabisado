# Tickets

Local Markdown tickets are the working source of truth during the foundation
phase. If GitHub Issues/Projects are enabled later, the synchronization rules
below apply.

## 1. Lifecycle

```text
BACKLOG → READY → IN PROGRESS → REVIEW → COMPLETED
```

| Status | Meaning | Folder |
| --- | --- | --- |
| BACKLOG | Captured, not yet ready | `tickets/backlog/` |
| READY | Refined, unblocked, ready to start | `tickets/ready/` |
| IN PROGRESS | Actively being worked | `tickets/in-progress/` |
| REVIEW | Implementation done, awaiting review | `tickets/review/` |
| COMPLETED | Merged and accepted | `tickets/completed/` |

Move the file when the status changes. Do not keep duplicates in two folders.

## 2. Ticket IDs

`KAB-NNN`, sequential and never reused. Feature tickets may use blocks
(`KAB-1xx`) to group by epic, but the sequence must stay unique.

## 3. Definition of Ready

A ticket is ready only when it has:

- ID, title, type, priority.
- Description and business justification.
- In-scope and out-of-scope.
- Dependencies, each resolved or explicitly unblocked.
- Acceptance criteria that are observable and testable.
- Implementation checklist.
- Testing checklist.
- Links to the approved specification, ADRs, and related tickets.
- An owner or an explicit "unassigned".

If the ticket needs a specification and none is approved, it stays in BACKLOG.

## 4. Definition of Done

See [`docs/engineering/definition-of-done.md`](../docs/engineering/definition-of-done.md).
A ticket is completed only when the PR is merged, checks pass, docs are updated,
and acceptance criteria are verified.

## 5. Epics

Epics group related features. They are tracked in
[`EPICS.md`](EPICS.md). An epic is not a ticket; it has no code of its own.

## 6. GitHub synchronization

When GitHub Issues/Projects are enabled:

- One issue per ticket; title starts with `KAB-NNN`.
- The local file stores the issue URL.
- Local file is authoritative for the full description and checklist.
- GitHub status maps to the folder:

| Local folder | GitHub Project column |
| --- | --- |
| `backlog/` | Backlog |
| `ready/` | Ready |
| `in-progress/` | In Progress |
| `review/` | In Review |
| `completed/` | Done |

- Update both within one working day.
- Closing an issue requires the file in `completed/`.
- Do not maintain conflicting acceptance criteria in two places. Copy the
  approved text verbatim or link to the local file.

## 7. Work in progress

- Limit work in progress to what the team can review.
- One ticket per branch and PR.
- Split a ticket that cannot be reviewed in one sitting.
- Do not start a ticket whose dependencies are unresolved.

## 8. Priority

| Priority | Meaning |
| --- | --- |
| P0 | Blocks the foundation or launch; do next |
| P1 | Required for the current milestone |
| P2 | Important, can follow the milestone |
| P3 | Nice to have |

## 9. Types

`feature`, `bug`, `task`, `improvement`, `security`, `documentation`.

## 10. Current state

- `review/`: KAB-001 (foundation initialization)
- `ready/`: decisions and unblocked documentation work
- `backlog/`: feature-level tickets awaiting specification

See [`EPICS.md`](EPICS.md) for the dependency-aware backlog.
