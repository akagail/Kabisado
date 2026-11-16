# KAB-113: Practice Frontend: Session, Timer, Results, and History

**Status:** IN PROGRESS
**Type:** feature
**Priority:** P1
**Epic:** E4 Practice
**Owner:** unassigned
**Created:** 2026-11-15
**Updated:** 2026-11-16
**Specification:** SPEC-0004 (approved 2026-11-07)
**Related ADRs:** ADR-0003, ADR-0007
**GitHub issue:** none (create when moved to READY)
**Pull request:** https://github.com/akagail/Kabisado/pull/49

## 1. Description

Build the learner-facing practice flow against the KAB-104 API: start a session
from a topic, answer questions, submit, view results, and browse session
history. Covers the loading, empty, error, and unauthorized states for each
screen.

## 2. Business justification

The backend practice loop exists but learners cannot use it. Without these
screens KAB-104 delivers no user value, and the E2E journey required by the
Definition of Done cannot run.

## 3. Scope

In:

- Start controls on the topic page: mode (untimed/timed) and size.
- Session screen: position/total, stem, options, save-answer on select, resume
  after refresh.
- Countdown for timed sessions driven by the server `expires_at`; auto-submit
  when it reaches zero and show results.
- Submit with confirmation; safe against double submit.
- Results screen: score, per-item correctness, explanation, provenance.
- History list with status, score, and a link to results; empty state.
- URL state for mode, size, and pagination where applicable.
- Loading, empty, error, unauthorized, and not-found states.
- Responsive layout and keyboard-accessible options.

Out:

- Analytics dashboard and weak topics (KAB-105).
- AI explanations (KAB-108).
- Flashcards (KAB-109).
- Full mock exam with section breaks.
- Offline support and service workers.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-104 | practice API | in review (PR #48) |
| SPEC-0004 | approved specification | approved |
| ADR-0007 | snapshot model | accepted |
| KAB-101 | auth/session | done |

## 5. Acceptance criteria

- [x] A learner can start an untimed session from a topic and is taken to the
      session screen.
- [ ] A learner can start a timed session and sees a countdown based on the
      server deadline. (Countdown implemented; not yet covered by E2E or manual
      verification.)
- [x] Selecting an option saves the answer; reloading the session restores it.
- [x] The session screen shows current position, total items, and navigation
      between items.
- [x] Submitting asks for confirmation and cannot double-submit.
- [ ] A timed session at zero auto-submits and shows results. (Implemented via
      the countdown callback; not yet verified end to end.)
- [x] Results show the score, each item's correctness, the explanation, and the
      provenance.
- [x] History lists the learner's sessions with status and score; an empty
      history shows an empty state.
- [x] Another learner's session shows a not-found state, not their data.
- [x] Every data view has loading, error, and unauthorized states.
- [ ] The flow works at mobile width and with keyboard-only input. (Not yet
      checked manually.)

## 6. Implementation checklist

- [x] Specification approved (SPEC-0004).
- [x] Technical design reviewed (route and component plan recorded here).
- [x] API types added to the shared client from the OpenAPI schema.
- [x] Topic start controls implemented.
- [x] Session screen and answer saving implemented.
- [x] Timed countdown and auto-submit implemented.
- [x] Results screen implemented.
- [x] History screen implemented.
- [x] Loading/empty/error/unauthorized states implemented.
- [x] Documentation updated (frontend architecture route notes).
- [x] No backend or schema change required.

## 7. Testing checklist

- [x] Component tests for start controls, session, results, and history.
- [x] Network-boundary mocks for API errors and unauthorized responses.
- [x] E2E: start, answer, submit, results.
- [ ] E2E: expired timed session auto-submits. (Not written yet; countdown and
      auto-submit are implemented but unverified end to end.)
- [ ] E2E: history empty state and another user's session is not found. (Empty
      state is covered by E2E; not-found is a component test only.)
- [ ] Accessibility check (labels, focus order, keyboard options).
- [ ] Manual verification on mobile width.

## 8. Validation evidence

```text
cd frontend
npm run typecheck
tsc --noEmit: passed

npm run lint
eslint .: passed

npm test -- --run
14 files, 35 tests passed

npm run build
Next.js build passed; /practice, /practice/[id], /practice/[id]/results generated

npx playwright test
5 tests passed
```

## 9. Risks and notes

- Countdown must use the server `expires_at`, never a client-computed deadline.
- Autosave needs debouncing and a retry/error state; the last write wins.
- Timed sessions currently use a fixed 60-second limit; keep the UI driven by
  `time_limit_seconds` so a spec change needs no frontend work.
- Submit is idempotent in the API but has no row lock; the UI should still
  disable the button after the first click.
- History returns a flat list today; do not build pagination UI until the API
  contract changes.
- Answers save on selection without debouncing; rapid changes issue one request
  per selection and the last response wins.
- The countdown and expired-session auto-submit are implemented but have no
  component or E2E coverage yet.

## 10. References

- `docs/specifications/SPEC-0004-practice-and-results.md`
- `docs/architecture/api-contracts.md` §5
- `docs/architecture/frontend-architecture.md`
- `docs/architecture/decisions/` (ADR-0003, ADR-0007)
- KAB-104 (backend practice API), KAB-105 (analytics)
