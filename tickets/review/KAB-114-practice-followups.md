# KAB-114: Practice Follow-ups: Faults, Gaps, and Cleanups

**Status:** REVIEW
**Type:** task
**Priority:** P1
**Epic:** E4 Practice
**Owner:** unassigned
**Created:** 2026-11-16
**Updated:** 2026-11-17
**Specification:** SPEC-0004 (approved 2026-11-07)
**Related ADRs:** ADR-0003, ADR-0007
**GitHub issue:** none (maintainer creates; agents do not)
**Pull request:** https://github.com/akagail/Kabisado/pull/53

## 1. Description

Collects the defects, missing coverage, contract mismatches, and housekeeping
found while delivering KAB-104 (practice API) and the practice frontend. None of
these are new features; they close the gap between the merged practice work and
the approved specification.

## 2. Business justification

One defect changes user data incorrectly: a saved answer cannot be changed, even
though the spec says answers are editable before submit. The rest are contract,
race-safety, and process gaps that will otherwise be rediscovered later.

## 3. Scope

In:

### Correctness

- Fix `save_answer` so an existing answer can be changed. It currently only
  writes when the answer is empty.
- Return `error.code = "session_expired"` (not the generic `conflict`) when a
  timed answer arrives after the deadline, per SPEC-0004 and the error catalogue.
- Make submit race-safe with `select_for_update` and cover it with a test.
- Add the missing `answer_saved` and `result_viewed` audit events listed in
  SPEC-0004, or record why they are deferred.

### Contract and configuration

- Decide history pagination: implement the standard envelope or remove the
  unused `page`/`page_size` parameters. Update `api-contracts.md` §5 either way.
- Replace the hardcoded 60-second timed limit with a configured value. This
  needs a decision on where the duration lives (exam version vs setting).
- Decide whether practice responses should be wrapped as `{session}` /
  `{result}` per the contract, or whether the documented flat shape becomes the
  contract.

### Frontend gaps

- E2E for an expired timed session auto-submitting to results.
- E2E for another learner's session showing not-found.
- Mobile-width and keyboard-only verification of the practice flow.
- Evaluate debouncing answer saves; keep one request per selection only if it
  measures fine.

### Cleanup

- Renumber `KAB-113-practice-frontend` to **KAB-115** and rename its file. KAB-113
  is already used by `KAB-113-typescript-eslint-compatibility`. Update the PR
  #49 body, ticket title, and any references.
- Remove the unused `ChoiceSnapshotSerializer` and the unused
  `items__question__choices` prefetch in `get_session_results`.
- Move KAB-104 and the practice frontend ticket to `tickets/review/` and then
  `tickets/completed/` once the Definition of Done is met.
- Close issue #17 and create the missing GitHub issue for the frontend ticket.

Out:

- Analytics (KAB-105), AI study aids (KAB-108), flashcards (KAB-109).
- Full mock exam, adaptive selection, offline support.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-104 | practice API | merged (PR #48) |
| KAB-115 practice frontend | UI | merged (PR #49) |
| SPEC-0004 | approved specification | approved |
| ADR-0007 | snapshot model | accepted |

## 5. Acceptance criteria

- [x] Changing a saved answer through the API persists and is returned on the
      next read; a regression test fails before the fix.
- [x] Saving an answer after the deadline returns `409` with
      `error.code = "session_expired"`.
- [x] Concurrent submit test shows scoring happens once and one submit audit
      event is written.
- [x] History pagination matches the documented contract, and the docs no longer
      contradict the implementation.
- [x] The timed limit comes from configuration, not a literal `60`.
- [x] E2E: an expired timed session auto-submits and shows results.
- [x] E2E: another learner's session shows not-found.
- [x] Practice flow verified at mobile width and with keyboard-only input.
- [x] No ticket or branch uses `KAB-113` for two different pieces of work.
- [ ] KAB-104 and the practice frontend ticket are in the correct folder, issue
      #17 is closed, and the frontend ticket has a GitHub issue. (Tickets moved
      to `tickets/review/`; issue closure and creation are maintainer actions.)
- [x] `pytest`, `ruff`, and the frontend checks pass.

## 6. Implementation checklist

- [x] Fix `save_answer` update path and add the regression test.
- [x] Add the `session_expired` error code.
- [x] Add row locking to submit and the concurrency test.
- [x] Add or defer the missing audit events with a written reason.
- [x] Implement or remove history pagination.
- [x] Move the timed limit into configuration.
- [x] Resolve the response-shape deviation in the contract.
- [x] Renumber and rename the frontend ticket.
- [x] Add the missing E2E tests.
- [x] Remove the dead serializer and prefetch.
- [x] Update `docs/architecture/api-contracts.md` §5 and any spec notes.
- [ ] Move tickets and close/open the GitHub issues. (Tickets moved; issues are
      left to the maintainer.)

## 7. Testing checklist

- [x] Regression test for changing an answer.
- [x] Error-code test for expired saves.
- [x] Concurrency test for submit. (PostgreSQL-only; skipped on local SQLite and
      runs in backend CI.)
- [x] Pagination test for history.
- [x] Configured timed-limit test.
- [x] E2E expired session.
- [x] E2E not-found session.
- [x] Mobile and keyboard check.
- [x] Full backend and frontend suites.

## 8. Validation evidence

```text
cd backend
ruff format --check .  84 files already formatted
ruff check .          All checks passed!
manage.py check       System check identified no issues (0 silenced).
makemigrations --check --dry-run   No changes detected
pytest                107 passed, 1 skipped (PostgreSQL-only concurrency test)
pytest apps/practice  31 passed, 1 skipped

cd frontend
npm run lint          passed
npm run typecheck     passed
npm test -- --run     15 files, 38 tests passed
npm run build         passed
npx playwright test   10 passed
```

## 9. Risks and notes

- Row locking inside the existing transaction may interact with the audit write;
  keep the lock scope small and verify no deadlock in the test. The lock is taken
  before the status check, so a concurrent submit re-reads `submitted`.
- Renumbering a merged ticket touches links; it is done in one commit and no
  reference to the old practice-frontend KAB-113 remains.
- Pagination changes required a small frontend update; `SessionHistory` now
  reads `data.results` and the unit/E2E mocks use the envelope.
- The timed-duration decision is still open. The setting ships with the current
  60-second default; a per-exam duration needs a product decision.
- Debouncing answer saves was not measured; one request per selection is kept
  unchanged.
- `session_abandoned` is deferred because there is no abandon action.

## 10. References

- `backend/apps/practice/services.py`
- `backend/apps/practice/serializers.py`
- `backend/apps/practice/tests/`
- `frontend/src/components/practice/`
- `frontend/tests/e2e/practice.spec.ts`
- `docs/specifications/SPEC-0004-practice-and-results.md`
- `docs/architecture/api-contracts.md` §5
- KAB-104, KAB-115 (practice frontend), KAB-113 (TypeScript ESLint compatibility)
