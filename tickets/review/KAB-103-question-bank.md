# KAB-103: Question Bank and Review Workflow

**Status:** REVIEW
**Type:** feature
**Priority:** P1
**Epic:** E3 Question Bank
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-10
**Specification:** SPEC-0003 (approved 2026-11-07)
**Related ADRs:** ADR-0003, ADR-0007 (attempt snapshots)
**Branch:** `feat/KAB-103-question-bank`
**GitHub issue:** https://github.com/akagail/Kabisado/issues/16
**Pull request:** https://github.com/akagail/Kabisado/pull/38

## 1. Description

Implement multiple-choice questions, choices, explanations, provenance, a staff
review workflow, and user flagging.

## 2. Business justification

Practice quality depends on reviewed questions with correct answers and useful
explanations. Provenance is required for trust and copyright compliance.

## 3. Scope

In:

- Question and choice models with an exactly-one-correct constraint.
- Explanation, provenance, difficulty, and duplicate-stem hash.
- Statuses: `draft`, `in_review`, `published`, `retired`.
- Origin: `human`, `ai_assisted`, `ai_generated` (only `human` is authored in
  MVP; AI generation is KAB-108).
- Staff review/approve/reject/retire services with audit entries.
- User flagging and staff resolution.
- Read API for published items (answers withheld from learners).
- Admin review and flag queues.

Out:

- Bulk import (SPEC-0003 §3 non-goal; the earlier ticket text was wrong).
- AI generation (KAB-108).
- Adaptive selection.
- Identification/essay items.
- Public question authoring by learners.
- Dedicated frontend curator screens (the staff API and Django admin are the
  curator UI for this ticket).
- Item content and sample-content review (blocked by KAB-004 approval).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-102 | catalogue | completed 2026-11-10 (topics seeded) |
| KAB-004 | content plan | pending — blocks item authoring and sample review, not the bank itself |
| KAB-104 | practice | external — blocks two practice-set ACs only |

## 5. Acceptance criteria

- [x] A question has 2–6 choices and exactly one correct answer.
- [x] Every approved question has an explanation and a source reference.
- [ ] Import rejects invalid rows — **not applicable:** bulk import is a
      non-goal in SPEC-0003 §3; creation rejects invalid rows instead (tested).
- [ ] Staff can review, approve, retire, and correct items — review, approve,
      and retire are implemented and audited. **Correction is deferred:** there
      is no edit/revision endpoint in SPEC-0003 §8; the current path is retire
      and recreate. Needs a decision.
- [x] Staff actions are audited.
- [x] Learners see only published items.
- [x] Learners can flag an item; staff can resolve flags.
- [x] Duplicate stems are detectable (normalized hash).
- [x] API tests cover permissions and shape.
- [ ] Published items appear in practice sets — **deferred:** KAB-104.
- [ ] Retired items remain in historical results — **deferred:** KAB-104.

## 6. Implementation checklist

- [x] Write and approve the specification (SPEC-0003, 2026-11-07).
- [x] Technical design — SPEC-0003 §7–8 plus §19 implementation notes.
- [x] Implement models, constraints, indexes.
- [x] Implement creation validation (2–6 options, one correct, difficulty 1–5).
- [x] Implement review services and admin.
- [x] Implement flagging.
- [x] Implement read API.
- [x] Update docs and OpenAPI.

## 7. Testing checklist

- [x] Constraint tests (one correct answer, difficulty range, open-flag
      uniqueness).
- [x] Creation validation tests (option count, correct index, 404 topic).
- [x] Permission tests (learner vs staff).
- [x] Flag lifecycle tests (create, duplicate 409, resolve, re-flag, audit).
- [x] Duplicate detection test (normalized whitespace/case).
- [ ] Sample content review — **deferred:** needs KAB-004 approval and authored
      items.

## 8. Validation evidence

```text
backend    ruff format --check   clean
           ruff check            clean
           manage.py check       no issues
           makemigrations --check no changes
           pytest                77 passed (26 in apps/questions)
schema     manage.py spectacular --validate  clean; 6 question-bank paths
```

## 9. Risks and notes

- A wrong approved answer is a trust incident; corrections currently mean
  retiring the item and recreating it. Published rows are never edited.
- Self-review is blocked in the service, not only in the UI.
- Learners never receive `is_correct`, `rationale`, `explanation`, or
  `provenance`; KAB-104 scoring reads the key server-side.
- Duplicate stems are detectable via `stem_hash`, not blocked. Decide during
  authoring whether a duplicate should be a hard error.
- Flag resolution/dismissal lives in the Django admin because SPEC-0003 §8
  declares no resolve endpoint. A dedicated endpoint can be added later.
- No content is seeded; the 300-item gate is a KAB-004 decision.
- `source_material_id`, `source_chunk_id`, `generated_by_user_id`, and
  `ai_generation_id` are beta fields in the database design, not implemented.
- Frontend curator screens and the learner flag UI are not in this ticket; the
  learner flag screen belongs with the KAB-104 results view.

## 10. References

- `docs/specifications/SPEC-0003-question-bank-and-review.md`
- `docs/architecture/api-contracts.md` §4 Question bank
- `docs/architecture/database-design.md` §5 Question bank
- `docs/product/content-sourcing-plan.md` — item rules (Draft)
- `docs/engineering/phase-4-clearance-model.md` — Category A gate dependency
