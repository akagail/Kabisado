# KAB-104: Practice Sessions and Scoring

**Status:** BACKLOG
**Type:** feature
**Priority:** P1
**Epic:** E4 Practice
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** SPEC-0004 (draft, awaiting approval)
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
| KAB-101 | auth | pending |
| KAB-103 | question bank | pending |

## 5. Acceptance criteria

- [ ] A user can start an untimed session by topic.
- [ ] A user can start a timed session with a visible countdown.
- [ ] Answers survive refresh.
- [ ] Submission is idempotent and race-safe.
- [ ] Timed sessions auto-submit at expiry.
- [ ] Results show score and explanations with sources.
- [ ] An expired/abandoned session cannot be resumed as active.
- [ ] A user cannot access another user's session (IDOR).
- [ ] Scoring treats unanswered as incorrect.
- [ ] Tests cover boundaries and duplicate submit.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement models and migrations.
- [ ] Implement selection and snapshot service.
- [ ] Implement response upsert and submit service.
- [ ] Implement timer/expiry handling.
- [ ] Implement API and UI.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Scoring unit tests.
- [ ] Duplicate submit test.
- [ ] Timer expiry test with frozen time.
- [ ] IDOR tests.
- [ ] E2E: start → answer → submit → results.
- [ ] Mobile and keyboard check.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Use a transaction and row lock for submit.
- Do not trust client timestamps; clamp elapsed time.
- Snapshot items so question edits do not change history.

## 10. References

- `docs/specifications/SPEC-0004-practice-and-results.md`
- `docs/architecture/api-contracts.md` §Practice
- `docs/architecture/database-design.md`
