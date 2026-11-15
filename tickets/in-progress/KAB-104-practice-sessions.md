# KAB-104: Practice Sessions and Scoring

**Status:** IN PROGRESS
**Type:** feature
**Priority:** P1
**Epic:** E4 Practice
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-15
**Specification:** SPEC-0004 (approved 2026-11-07)
**Related ADRs:** ADR-0003, ADR-0007
**GitHub issue:** https://github.com/akagail/Kabisado/issues/17

## 1. Description

Implement untimed and timed practice sessions, item snapshots, answer
persistence, idempotent submission, scoring, and results with explanations.

## 2. Business justification

This is the core learning loop and the primary reason users return.

## 3. Scope

In:

- Start session by subject/topic, with item count and mode.
- Snapshot selected items into the session.
- Save/update responses before submit.
- Submit and score exactly once (idempotent).
- Auto-submit on timer expiry.
- Results: score, correct choice, explanation, source.
- Resume an active untimed session after refresh.
- Session history list.
- API and UI states (loading, empty, error, expired).

Out:

- Full mock exam with section breaks.
- Adaptive item selection.
- Flashcards.
- AI explanations (KAB-108).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-101 | auth | done |
| KAB-103 | question bank | merged |

## 5. Acceptance criteria

- [x] A user can start an untimed session by topic.
- [ ] A user can start a timed session with a visible countdown. (API supports
      timed sessions and returns `expires_at`; the countdown UI is not built.)
- [x] Answers survive refresh.
- [x] Submission is idempotent.
- [ ] Submission is race-safe. (No row lock/`select_for_update` yet; concurrent
      submits are untested.)
- [x] Timed sessions auto-submit at expiry (check-on-read/submit path).
- [x] Results show score and explanations with sources.
- [x] An expired/abandoned session cannot be resumed as active.
- [x] A user cannot access another user's session (IDOR).
- [x] Scoring treats unanswered as incorrect.
- [x] Tests cover boundaries and duplicate submit.

## 6. Implementation checklist

- [x] Write and approve the specification.
- [ ] Write the technical design. (Design lives in SPEC-0004; no separate
      technical-design document was written.)
- [x] Implement models and migrations.
- [x] Implement selection and snapshot service.
- [x] Implement response upsert and submit service.
- [x] Implement timer/expiry handling.
- [ ] Implement API and UI. (API done; frontend practice screens are not built.)
- [x] Update docs and OpenAPI.

## 7. Testing checklist

- [x] Scoring unit tests.
- [x] Duplicate submit test.
- [x] Timer expiry test (session expiry simulated by updating `expires_at`, not
      frozen time).
- [x] IDOR tests.
- [ ] E2E: start → answer → submit → results. (Needs the frontend screens.)
- [ ] Mobile and keyboard check. (Needs the frontend screens.)

## 8. Validation evidence

```text
backend/.venv/Scripts/python.exe -m pytest backend/apps/practice/tests
24 passed

backend/.venv/Scripts/python.exe -m pytest backend/apps
101 passed

backend/.venv/Scripts/python.exe -m ruff format --check backend
83 files already formatted

backend/.venv/Scripts/python.exe -m ruff check backend
All checks passed!

backend/.venv/Scripts/python.exe backend/manage.py check
System check identified no issues (0 silenced).

backend/.venv/Scripts/python.exe backend/manage.py makemigrations --check --dry-run
No changes detected

backend/.venv/Scripts/python.exe backend/manage.py spectacular --validate
Schema generated with 0 warnings and 0 errors.
```

## 9. Risks and notes

- Use a transaction and row lock for submit.
- Do not trust client timestamps; clamp elapsed time.
- Snapshot items so question edits do not change history.
- Timed sessions use a fixed 60-second limit until the per-exam duration is
  specified.
- History accepts `page`/`page_size` but returns a flat list, not the standard
  pagination envelope.
- Frontend practice UI and Playwright E2E remain before this ticket can move to
  review.

## 10. References

- `docs/specifications/SPEC-0004-practice-and-results.md`
- `docs/architecture/api-contracts.md` §5
- `docs/architecture/database-design.md`
- `docs/engineering/phase-4-clearance-model.md` — Category A gate dependency
