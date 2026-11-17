# KAB-115: Practice Frontend: Session, Timer, Results, and History

**Status:** REVIEW
**Type:** feature
**Priority:** P1
**Epic:** E4 Practice
**Owner:** unassigned
**Created:** 2026-11-15
**Updated:** 2026-11-17
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
- [x] A learner can start a timed session and sees a countdown based on the
      server deadline. (E2E covers an expired timed session in KAB-114.)
- [x] Selecting an option saves the answer; reloading the session restores it.
- [x] The session screen shows current position, total items, and navigation
      between items.
- [x] Submitting asks for confirmation and cannot double-submit.
- [x] A timed session at zero auto-submits and shows results. (E2E added in
      KAB-114.)
- [x] Results show the score, each item's correctness, the explanation, and the
      provenance.
- [x] History lists the learner's sessions with status and score; an empty
      history shows an empty state.
- [x] Another learner's session shows a not-found state, not their data. (E2E
      added in KAB-114.)
- [x] Every data view has loading, error, and unauthorized states.
- [x] The flow works at mobile width and with keyboard-only input. (E2E at
      360 px with keyboard-only input added in KAB-114.)

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
- [x] E2E: expired timed session auto-submits. (Added in KAB-114.)
- [x] E2E: history empty state and another user's session is not found. (Both
      covered; not-found added in KAB-114.)
- [x] Accessibility check (labels, focus order, keyboard options). (Keyboard-only
      E2E added in KAB-114.)
- [x] Manual verification on mobile width. (360 px E2E added in KAB-114.)

## 8. Validation evidence

```text
cd frontend
npm run lint
eslint .: passed

npm run typecheck
tsc --noEmit: passed

npm test -- --run
14 files, 35 tests passed

npm run build
Next.js build passed; /practice, /practice/[id], /practice/[id]/results generated

npx playwright test
8 tests passed (5 journeys, including expired auto-submit, not-found, and
360 px keyboard-only practice)
```

The frontend suite was re-run on the KAB-114 branch after history moved to the
standard pagination envelope; the new E2E cases were added there.

## 9. Risks and notes

- Countdown must use the server `expires_at`, never a client-computed deadline.
- Autosave needs debouncing and a retry/error state; the last write wins.
- The timed limit comes from `PRACTICE_TIMED_LIMIT_SECONDS`; the UI stays driven
  by `time_limit_seconds` and `expires_at` so a change needs no frontend work.
- Submit locks the session row in the API (KAB-114); the UI also disables the
  button after the first click.
- History returns the standard pagination envelope; the list reads `results`
  only. Pagination UI is deferred until the history screen needs it.
- Answers save on selection without debouncing; rapid changes issue one request
  per selection and the last response wins.

## 10. References

- `docs/specifications/SPEC-0004-practice-and-results.md`
- `docs/architecture/api-contracts.md` §5
- `docs/architecture/frontend-architecture.md`
- `docs/architecture/decisions/` (ADR-0003, ADR-0007)
- KAB-104 (backend practice API), KAB-105 (analytics)
