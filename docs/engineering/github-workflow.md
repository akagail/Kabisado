# GitHub Workflow

**Status:** Approved for foundation use
**Owner:** Engineering
**Last updated:** 2026-11-06

GitHub Issues and the Kabisado project board mirror the local Markdown tickets.
They are a working view, not a second source of truth.

## 1. Source of truth

- `tickets/<status>/KAB-NNN-*.md` is authoritative for the full description,
  scope, acceptance criteria, and checklists.
- The GitHub issue mirrors the ticket and stores the same text; the local file
  stores the issue URL.
- Never keep different acceptance criteria in the two places. Edit the local
  ticket first, then update the issue in the same working day.
- Do not close an issue unless the ticket is in `tickets/completed/` and the
  definition of done is met.

## 2. Project board

- URL: <https://github.com/users/akagail/projects/1>
- Title: `Kabisado`
- One issue per ticket. One project item per issue. No draft items.
- Status is the only board field maintained manually; labels and the local
  folder must agree with it.

| Local folder | Project status |
| --- | --- |
| `tickets/backlog/` | Backlog |
| `tickets/ready/` | Ready |
| `tickets/in-progress/` | In Progress |
| `tickets/review/` | In Review |
| `tickets/completed/` | Done |

Move the local file and update the project status together. Do not use status
labels; the project field is the single status signal.

## 3. Issue format

- Title: `KAB-NNN: <ticket title>` — exactly the local H1 without the `#`.
- Body: the local ticket from the first metadata line onward, plus a footer:

```text
---

**Local ticket:** `tickets/ready/KAB-002-....md`
**Depends on:** #30 (KAB-001), #29 (KAB-005)
```

- `Depends on` links are generated from the local dependency table. The table
  remains authoritative; the links are a convenience.
- Do not add a second checklist in the issue. Checkboxes are copied from the
  ticket on migration and reconciled from the local file afterwards.

## 4. Labels

Only labels that carry information the board and title do not already carry.

| Group | Labels | Rule |
| --- | --- | --- |
| Type | `feature`, `task`, `security`, `documentation` | Exactly one, from the ticket `Type` field. `bug` and `improvement` exist for future use. |
| Priority | `priority:P0`, `priority:P1`, `priority:P2` | Exactly one, from the ticket `Priority` field. Add `priority:P3` only when a P3 ticket exists. |
| Area | `area:backend`, `area:frontend`, `area:ai`, `area:data`, `area:infra`, `area:docs` | One or more, from where the work lands. |

Rules:

- No `status:*` labels.
- No epic labels; the epic lives in the ticket metadata.
- Do not create a label for a single issue. Reuse an existing area first.
- Default GitHub labels (`bug`, `documentation`, `duplicate`, etc.) stay unless a
  cleanup is explicitly approved.

## 5. Creating and updating issues

Before creating an issue, search for the ticket ID:

```bash
gh issue list --repo akagail/Kabisado --state all --search "KAB-010 in:title"
```

If an issue exists, update it; never create a second one. New ticket flow:

1. Create the local ticket from `tickets/TEMPLATE.md` in `tickets/backlog/`.
2. Create the issue with the title and body rules above.
3. Apply type, priority, and area labels.
4. Add it to project `Kabisado` and set the status to match the folder.
5. Write the issue URL into the local `**GitHub issue:**` field.

Status changes: move the file, update the project status, and comment on the
issue when the reason is not obvious. Closing requires `completed/`.

## 6. Branch and pull request links

- Branch: `<type>/<ticket-id>-<short-slug>` (see `git-workflow.md`).
- Reference the ticket in the PR body with `Refs: KAB-NNN` and the issue with
  `Closes #NN` only when the ticket is genuinely done.
- One ticket per branch and PR.

## 7. Permissions and automation

- `gh` must be authenticated with `repo`, `project`, and `read:org` scopes.
- Issue creation and project updates are manual until a workflow is approved.
- Do not store tokens in the repository or in CI logs.
- The token used for migration is a user credential; CI must use a dedicated
  token with the minimum required scopes.

## 8. Migration record

The first migration (17 tickets, 2026-11-06) is recorded in
[`docs/plans/github-migration-report.md`](../plans/github-migration-report.md).
