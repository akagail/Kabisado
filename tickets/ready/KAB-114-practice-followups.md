# KAB-114: Practice Follow-ups: Faults, Gaps, and Cleanups

**Status:** READY
**Type:** task
**Priority:** P1
**Epic:** E4 Practice
**Owner:** unassigned
**Created:** 2026-11-16
**Updated:** 2026-11-17
**Specification:** SPEC-0004 (approved 2026-11-07)
**Related ADRs:** ADR-0003, ADR-0007
**GitHub issue:** none (create when work starts)

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
| KAB-113 practice frontend | UI | merged (PR #49) |
| SPEC-0004 | approved specification | approved |
| ADR-0007 | snapshot model | accepted |

## 5. Acceptance criteria

- [ ] Changing a saved answer through the API persists and is returned on the
      next read; a regression test fails before the fix.
- [ ] Saving an answer after the deadline returns `409` with
      `error.code = "session_expired"`.
- [ ] Concurrent submit test shows scoring happens once and one submit audit
      event is written.
- [ ] History pagination matches the documented contract, and the docs no longer
      contradict the implementation.
- [ ] The timed limit comes from configuration, not a literal `60`.
- [ ] E2E: an expired timed session auto-submits and shows results.
- [ ] E2E: another learner's session shows not-found.
- [ ] Practice flow verified at mobile width and with keyboard-only input.
- [ ] No ticket or branch uses `KAB-113` for two different pieces of work.
- [ ] KAB-104 and the practice frontend ticket are in the correct folder, issue
      #17 is closed, and the frontend ticket has a GitHub issue.
- [ ] `pytest`, `ruff`, and the frontend checks pass.

## 6. Implementation checklist

- [ ] Fix `save_answer` update path and add the regression test.
- [ ] Add the `session_expired` error code.
- [ ] Add row locking to submit and the concurrency test.
- [ ] Add or defer the missing audit events with a written reason.
- [ ] Implement or remove history pagination.
- [ ] Move the timed limit into configuration.
- [ ] Resolve the response-shape deviation in the contract.
- [ ] Renumber and rename the frontend ticket.
- [ ] Add the missing E2E tests.
- [ ] Remove the dead serializer and prefetch.
- [ ] Update `docs/architecture/api-contracts.md` §5 and any spec notes.
- [ ] Move tickets and close/open the GitHub issues.

## 7. Testing checklist

- [ ] Regression test for changing an answer.
- [ ] Error-code test for expired saves.
- [ ] Concurrency test for submit.
- [ ] Pagination test for history.
- [ ] Configured timed-limit test.
- [ ] E2E expired session.
- [ ] E2E not-found session.
- [ ] Mobile and keyboard check.
- [ ] Full backend and frontend suites.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Row locking inside the existing transaction may interact with the audit write;
  keep the lock scope small and verify no deadlock in the test.
- Renumbering a merged ticket touches links; do it in one docs commit so no
  reference is missed.
- Pagination changes may require a small frontend update; coordinate with the
  practice history screen.
- The timed-duration decision is a product/spec question, not only code. If it
  is unresolved, ship a setting with the current 60-second default and record
  the open decision.

## 10. References

- `backend/apps/practice/services.py`
- `backend/apps/practice/serializers.py`
- `backend/apps/practice/tests/`
- `frontend/src/components/practice/`
- `frontend/tests/e2e/practice.spec.ts`
- `docs/specifications/SPEC-0004-practice-and-results.md`
- `docs/architecture/api-contracts.md` §5
- KAB-104, KAB-113 (practice frontend), KAB-113 (TypeScript ESLint compatibility)
