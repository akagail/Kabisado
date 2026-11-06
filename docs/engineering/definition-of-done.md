# Definition of Done

**Status:** Approved for foundation use
**Owner:** Engineering
**Last updated:** 2026-11-06

A ticket is done only when every applicable item is true. If an item does not
apply, note why in the ticket rather than deleting it silently.

## Scope

- [ ] The change matches the approved ticket and specification.
- [ ] Out-of-scope work is captured as new tickets, not slipped in.
- [ ] No unrelated refactor or dependency upgrade is bundled.

## Correctness

- [ ] Acceptance criteria are verified individually.
- [ ] Edge cases and error states are handled.
- [ ] Permissions and ownership are enforced.
- [ ] Data integrity is preserved; transactions cover multi-row invariants.
- [ ] Migrations are included and reversible or documented.
- [ ] Idempotency is handled for retried or duplicated requests.

## Tests

- [ ] New behaviour has tests.
- [ ] Bug fixes include a regression test.
- [ ] Permission and cross-user access are tested.
- [ ] Boundary conditions are tested.
- [ ] The relevant suite passes locally.
- [ ] No test is skipped or weakened without a ticket.

## Quality

- [ ] Ruff format and lint pass.
- [ ] Django system and migration checks pass.
- [ ] ESLint and TypeScript pass.
- [ ] Production build passes.
- [ ] No new N+1 or unbounded query on a list endpoint.
- [ ] Frontend loading/empty/error/unauthorized states exist.
- [ ] Accessibility basics are met (labels, focus, keyboard).

## Security

- [ ] No secrets, credentials, or real personal data are committed.
- [ ] Inputs are validated server-side.
- [ ] Uploads are validated and private.
- [ ] AI input is delimited and output validated.
- [ ] Errors do not leak internals.
- [ ] Logs exclude sensitive data.
- [ ] Rate limits exist where abuse is possible.
- [ ] Dependency audit passes.

## Documentation

- [ ] The specification and ticket are updated.
- [ ] Architecture/ADR updated if a decision changed.
- [ ] `docs/operations/environment-variables.md` and `.env.example` updated for
      new variables.
- [ ] API schema updated.
- [ ] User-facing changes are noted for release notes.

## Review and release

- [ ] PR links the ticket and spec.
- [ ] Test evidence is included.
- [ ] Security and data risks are called out.
- [ ] At least one approval is recorded.
- [ ] Required CI checks are green.
- [ ] The ticket is moved to `tickets/completed/`.
- [ ] Follow-up work is ticketed.
- [ ] Deployment notes exist if the change needs a migration or config change.

## Not done if

- CI is red or a required check was skipped without an approved exception.
- Acceptance criteria are partially met.
- Documentation is missing for a behaviour or configuration change.
- A security or data-loss risk is unresolved and unapproved.
- The ticket is marked complete but the PR is unmerged.
