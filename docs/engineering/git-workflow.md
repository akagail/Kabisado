# Git Workflow

**Status:** Approved for foundation use
**Owner:** Engineering
**Last updated:** 2026-11-06

## 1. Model

**GitHub Flow** with a protected `main`:

- `main` is always deployable.
- Work happens on short-lived branches.
- Changes merge through pull requests.
- Releases are tags on `main`; no long-lived release branches at MVP.

## 2. Branch naming

```text
<type>/<ticket-id>-<short-slug>
```

Examples:

- `feat/KAB-012-registration`
- `fix/KAB-034-timer-autosubmit`
- `docs/KAB-007-adr-auth`
- `chore/KAB-002-ci-cache`

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `security`,
`perf`.

## 3. Commits

Conventional Commits:

```text
<type>(<scope>): <imperative summary>

Optional body: why, trade-offs, migration notes.
Refs: KAB-012
```

Rules:

- Summary ≤ 72 characters, imperative mood, no trailing period.
- One logical change per commit.
- Do not commit generated build output, secrets, or large binaries.
- Squash on merge unless the history is intentionally multi-commit and clean.

Examples:

- `feat(auth): add email/password registration`
- `fix(practice): prevent duplicate session submission`
- `docs(adr): propose session authentication`
- `ci(backend): run migrations check`

## 4. Pull requests

Every PR:

- Links the ticket and the approved specification.
- States what changed and why.
- Lists validation commands and results.
- Calls out security, data, and migration risks.
- Includes screenshots for UI changes.
- Lists deliberate follow-ups.

Size guidance:

- Target ≤ 400 changed lines excluding generated files.
- Split mechanical refactors from behaviour changes.
- If a PR cannot be reviewed in one sitting, split it.

Draft PRs are encouraged for early feedback. A draft cannot merge.

## 5. Review

- At least one approving review is required; two for security-sensitive changes.
- The author resolves conversations; the reviewer re-checks.
- Review correctness, authorization, error handling, tests, and scope.
- Style comments must reference a documented standard.
- Do not approve with failing required checks.
- Do not merge your own PR without a review unless the repository owner
  explicitly allows it for a documented emergency.

## 6. Merge

- Squash merge by default.
- The squash commit uses the Conventional Commit format.
- Delete the branch after merge.
- Do not force-push `main`.
- Do not rewrite published history.

## 7. Keeping up to date

- Rebase your branch on `main` before review, or merge `main` if the branch is
  shared.
- Resolve conflicts locally and run the affected checks again.
- Do not resolve conflicts by discarding the other side without understanding it.

## 8. Releases and tags

- Tag production releases `v<major>.<minor>.<patch>`.
- A release note lists user-visible changes, migrations, and rollback notes.
- Hotfixes branch from the release tag, then merge back to `main`.
- No release without a green pipeline and a completed launch checklist.

## 9. Ticket synchronization

Local Markdown tickets are the working source of truth during the foundation
phase. If GitHub Issues/Projects are enabled:

- One GitHub issue per local ticket; the title starts with the ticket ID.
- The local file stores the issue URL.
- Status changes update both within the same working day.
- Do not maintain different acceptance criteria in the two places; link to the
  local file or copy the approved text verbatim.
- Closing an issue requires the ticket to be in `tickets/completed/`.

See `tickets/README.md`.

## 10. Branch protection (recommended)

For `main`:

- Require a pull request before merging.
- Require at least one approval.
- Dismiss stale approvals on new commits.
- Require status checks: `backend`, `frontend`, and `e2e` (for user-flow PRs).
- Require branches to be up to date before merging.
- Require conversation resolution.
- Block force pushes and deletions.
- Restrict who can push.
- Require signed commits if the team adopts signing.

## 11. Forbidden

- Committing `.env`, keys, tokens, or production data.
- Pushing directly to `main`.
- `--no-verify` to bypass hooks.
- Disabling a failing test without a ticket.
- Mixing a dependency upgrade with a feature.
- Committing generated lockfile changes unrelated to the dependency change.
