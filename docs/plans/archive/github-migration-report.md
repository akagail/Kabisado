# GitHub Migration Report

**Status:** Review
**Owner:** Engineering
**Last updated:** 2026-11-06
**Scope:** Phase 1.5 — migrate local tickets to GitHub Issues and configure the
project board. No application features were implemented.

## 1. Summary

| Metric | Result |
| --- | --- |
| Markdown tickets discovered | 17 |
| GitHub Issues created | 17 |
| Existing issues reused | 0 |
| Duplicate issues detected | 0 |
| Failed migrations | 0 |
| Skipped migrations | 0 |
| Project items | 17 |
| Project | <https://github.com/users/akagail/projects/1> |

Repository: <https://github.com/akagail/Kabisado>
Migrated with `gh` 2.103.3 as `akagail`, scopes `repo`, `project`, `read:org`.
The repository had no issues before migration; duplicate prevention also matches
titles by the `KAB-NNN` prefix.

## 2. Project board

- Title: `Kabisado`, number 1, private user project.
- View: `Board`, board layout.
- Status options, in order: `Backlog`, `Ready`, `In Progress`, `In Review`,
  `Done`.
- No status labels were created; the project field is the only status signal.
- Initial status comes from the local folder: `review/` → In Review; `ready/` →
  Ready; `backlog/` → Backlog.

## 3. Labels

Created only labels that are used:

| Group | Labels |
| --- | --- |
| Type | `feature`, `task`, `security` (reused existing `documentation`) |
| Priority | `priority:P0`, `priority:P1`, `priority:P2` |
| Area | `area:backend`, `area:frontend`, `area:ai`, `area:data`, `area:infra`, `area:docs` |

Existing GitHub defaults were left in place. `bug`, `improvement`, and
`priority:P3` were not created because no ticket uses them yet.

## 4. Issue mapping

| Ticket | Issue | Initial status | Labels |
| --- | --- | --- | --- |
| KAB-001 | [#30](https://github.com/akagail/Kabisado/issues/30) | In Review | task, priority:P0, area:backend, area:frontend, area:infra, area:docs |
| KAB-002 | [#26](https://github.com/akagail/Kabisado/issues/26) | Ready | task, priority:P0, area:docs |
| KAB-003 | [#27](https://github.com/akagail/Kabisado/issues/27) | Ready | task, priority:P0, area:infra, area:docs |
| KAB-004 | [#28](https://github.com/akagail/Kabisado/issues/28) | Ready | documentation, priority:P1, area:data, area:docs |
| KAB-005 | [#29](https://github.com/akagail/Kabisado/issues/29) | Ready | security, priority:P0, area:docs |
| KAB-101 | [#14](https://github.com/akagail/Kabisado/issues/14) | Backlog | feature, priority:P1, area:backend, area:frontend |
| KAB-102 | [#15](https://github.com/akagail/Kabisado/issues/15) | Backlog | feature, priority:P1, area:backend, area:data |
| KAB-103 | [#16](https://github.com/akagail/Kabisado/issues/16) | Backlog | feature, priority:P1, area:backend, area:data |
| KAB-104 | [#17](https://github.com/akagail/Kabisado/issues/17) | Backlog | feature, priority:P1, area:backend, area:frontend |
| KAB-105 | [#18](https://github.com/akagail/Kabisado/issues/18) | Backlog | feature, priority:P1, area:backend, area:frontend |
| KAB-106 | [#19](https://github.com/akagail/Kabisado/issues/19) | Backlog | feature, priority:P2, area:backend, area:frontend, area:infra |
| KAB-107 | [#20](https://github.com/akagail/Kabisado/issues/20) | Backlog | feature, priority:P2, area:backend, area:ai, area:infra |
| KAB-108 | [#21](https://github.com/akagail/Kabisado/issues/21) | Backlog | feature, priority:P2, area:backend, area:ai, area:frontend |
| KAB-109 | [#22](https://github.com/akagail/Kabisado/issues/22) | Backlog | feature, priority:P2, area:backend, area:frontend |
| KAB-110 | [#23](https://github.com/akagail/Kabisado/issues/23) | Backlog | task, priority:P1, area:backend, area:infra |
| KAB-111 | [#24](https://github.com/akagail/Kabisado/issues/24) | Backlog | task, priority:P1, area:frontend, area:infra |
| KAB-112 | [#25](https://github.com/akagail/Kabisado/issues/25) | Backlog | task, priority:P1, area:infra |

Issue numbering starts at #14 because GitHub assigned numbers before any issue
existed in this repository; numbering gaps are normal and do not indicate
deleted or hidden tickets.

## 5. Relationships

Every issue footer links its local ticket and its dependency issues:

```text
**Local ticket:** `tickets/backlog/KAB-104-practice-sessions.md`
**Depends on:** #14 (KAB-101), #16 (KAB-103)
```

Dependencies were parsed from each ticket's `## 4. Dependencies` table. The
local table remains authoritative. Native GitHub "blocked by" relationships were
not used because the CLI does not expose a stable command for them; the footer
links plus the ticket text preserve the graph without adding fragile automation.

## 6. Validation

A comparison script checked every ticket against its issue:

- Title equals the local H1.
- Body equals the local ticket from the first metadata line onward, plus the
  migration footer.
- Labels equal the expected type, priority, and area set.
- Project status equals the local folder mapping.
- The local file contains the correct issue URL.
- No duplicate issue titles exist.

Result: 17/17 checked, 0 problems, 17 project items. Local checks ran after the
migration and the repository was re-scanned for duplicate `KAB-` titles.

## 7. Missing or unresolved information

No ticket is missing required metadata (ID, type, priority, scope, dependencies,
acceptance criteria, implementation and testing checklists).

The following are intentionally unresolved and tracked by the tickets
themselves:

- **Owners:** all backlog tickets say `unassigned`; no human has been assigned.
- **KAB-001:** awaiting human review of the initialization report.
- **KAB-002–KAB-005:** human decision gates; no decision recorded yet.
- **KAB-004:** the acceptance criteria reference
  `docs/product/content-sourcing-plan.md`, which is the deliverable of that
  ticket and does not exist yet.
- **KAB-005:** references `docs/engineering/threat-model.md` and
  `docs/operations/data-map.md`, which are deliverables of that ticket.
- **Implementation tickets:** all remain blocked by unapproved specifications and
  provider decisions, as documented in their dependency tables.

## 8. Outstanding configuration

- The remote repository still has no pushed code; the default branch exists but
  is empty. First push needs owner approval.
- Branch protection, required checks, and merge rules are not configured.
- The project is private. Make it public only if the board should be visible
  outside the repository's collaborators.
- No project automation (auto-add or auto-status workflows) exists; updates are
  manual and must follow `docs/engineering/github-workflow.md`.
- The `gh` token is a user credential. CI, when added, needs a dedicated token
  with minimal scopes.

## 9. References

- [`docs/engineering/github-workflow.md`](../engineering/github-workflow.md)
- [`tickets/README.md`](../../tickets/README.md)
- [`tickets/EPICS.md`](../../tickets/EPICS.md)
