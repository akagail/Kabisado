# KAB-105: Progress Analytics and Weak Topics

**Status:** IN PROGRESS
**Type:** feature
**Priority:** P1
**Epic:** E5 Analytics
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-17
**Specification:** SPEC-0005 (approved 2026-11-07)
**Related ADRs:** ADR-0003, ADR-0007
**GitHub issue:** https://github.com/akagail/Kabisado/issues/18

## 1. Description

Show accuracy by subject and topic, recent practice history, and a rule-based
weak-topic list.

## 2. Business justification

Feedback turns practice into learning. Visible weak areas are the core
personalization promise of the MVP.

## 3. Scope

In:

- Response-derived aggregates per user/topic.
- Accuracy by subject and topic.
- Recent session history.
- Weak-topic rule: ≥ 3 attempts and < 70% accuracy (configurable).
- Dashboard and progress screens.
- Empty state for users without attempts.
- API endpoints with pagination where needed.

Out:

- Predictive readiness scores.
- Cohort comparison.
- Recommendations/study plans.
- ML-based diagnosis.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-104 | practice + responses | merged (PR #48) |
| SPEC-0005 | approved specification | approved 2026-11-07 |

## 5. Acceptance criteria

- [x] Aggregates are correct for a known fixture.
- [x] Weak topics use the documented rule and boundary values.
- [x] A user sees accuracy by subject and topic.
- [x] A user sees recent sessions with dates and scores.
- [x] Empty state is useful and not an error.
- [x] Another user's analytics cannot be read (IDOR).
- [x] Aggregates update after a submitted session.
- [x] Query count is bounded for the dashboard.

## 6. Implementation checklist

- [x] Write and approve the specification.
- [x] Write the technical design (on-the-fly aggregates; no aggregate tables).
- [x] Implement selectors/aggregates.
- [x] Implement endpoints.
- [x] Build dashboard/progress UI (`/progress`).
- [x] Review indexes: no new index needed; existing foreign keys and unique
      constraints cover the joins.
- [x] Update docs and OpenAPI.

## 7. Testing checklist

- [x] Boundary tests for the weak-topic rule.
- [x] Aggregate correctness test.
- [x] IDOR test.
- [x] Query-count test.
- [x] Frontend states test.
- [x] E2E: submit → results → progress (API mocked, matching the suite).

## 8. Validation evidence

```text
cd backend
.venv/Scripts/python.exe -m ruff format --check .
91 files already formatted

.venv/Scripts/python.exe -m ruff check .
All checks passed!

.venv/Scripts/python.exe manage.py check
System check identified no issues (0 silenced).

.venv/Scripts/python.exe manage.py makemigrations --check --dry-run
No changes detected

.venv/Scripts/python.exe -m pytest apps
112 passed

.venv/Scripts/python.exe manage.py spectacular --file schema.yml
Schema generated; /api/v1/analytics/summary/ and /api/v1/analytics/topics/
present.

cd frontend
npm run typecheck
tsc --noEmit: passed

npm run lint
eslint .: passed

npm test -- --run
15 files, 38 tests passed

npm run build
Next.js build passed; /progress generated

npx playwright test
7 tests passed
```

## 9. Risks and notes

- Start with on-the-fly queries; denormalize only when measured slow.
- Do not expose other users' data in aggregate endpoints.
- Make the threshold configurable and documented.
- `attempts` is the number of answered items, not sessions; SPEC-0005 §6's
  "distinct topics attempted" wording is superseded by the topic-row contract.
- Learners with no `target_exam` get empty analytics rather than cross-exam
  aggregates.
- Catalogue topic rows (`/subjects/{id}/topics/`, `/topics/{id}/`) still return
  placeholder `accuracy`/`attempts`; wiring them to this selector is follow-up
  work, not part of this ticket.
- The progress UI lives at `/progress` and reuses the practice history list. The
  per-session weak-topic count shown in SPEC-0005 §9 is not available from the
  API; the history row shows date, mode, and score only.
- E2E tests mock the API, consistent with the rest of the suite; the backend
  aggregation is covered by pytest, not by a live end-to-end run.

## 10. References

- `docs/specifications/SPEC-0005-progress-analytics.md`
- `docs/architecture/api-contracts.md` §6
- `docs/architecture/database-design.md` §3
- `docs/engineering/phase-4-clearance-model.md` — Category A gate dependency
- `backend/apps/analytics/`
- `backend/apps/practice/models.py`
