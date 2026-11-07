# KAB-103: Question Bank and Review Workflow

**Status:** BACKLOG
**Type:** feature
**Priority:** P1
**Epic:** E3 Question Bank
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** SPEC-0003 (draft, awaiting approval)
**Related ADRs:** ADR-0003
**GitHub issue:** https://github.com/akagail/Kabisado/issues/16

## 1. Description

Implement multiple-choice questions, choices, explanations, provenance, a staff
review workflow, import tooling, and user flagging.

## 2. Business justification

Practice quality depends on reviewed questions with correct answers and useful
explanations. Provenance is required for trust and copyright compliance.

## 3. Scope

In:

- Question and choice models with exactly-one-correct constraint.
- Explanation and source attribution fields.
- Statuses: draft, in_review, approved, retired.
- Origin: human, ai_assisted, ai_generated.
- Staff review/approve/retire actions with audit log.
- Import command for reviewed content (CSV/JSON).
- User flagging and staff resolution.
- API for approved items (read only for learners).
- Admin review queue.

Out:

- AI generation (KAB-108).
- Adaptive selection.
- Identification/essay items.
- Public question authoring by learners.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-102 | catalogue | pending |
| KAB-004 | content plan | pending |

## 5. Acceptance criteria

- [ ] A question has 2–6 choices and exactly one correct answer.
- [ ] Every approved question has an explanation and a source reference.
- [ ] Import rejects invalid rows with a clear report.
- [ ] Staff can review, approve, retire, and correct items.
- [ ] Staff actions are audited.
- [ ] Learners see only approved items.
- [ ] Learners can flag an item; staff can resolve flags.
- [ ] Duplicate stems are detectable (normalized hash).
- [ ] API tests cover permissions and shape.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement models, constraints, indexes.
- [ ] Implement import and validation.
- [ ] Implement review services and admin.
- [ ] Implement flagging.
- [ ] Implement read API.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Constraint tests (one correct answer, choice count).
- [ ] Import success/failure tests.
- [ ] Permission tests (learner vs staff).
- [ ] Flag lifecycle tests.
- [ ] Duplicate detection test.
- [ ] Sample content review.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- A wrong approved answer is a trust incident; require second review for
  corrections.
- Do not publish unreviewed AI items in the shared pool.
- Keep explanations concise and source-linked.

## 10. References

- `docs/specifications/SPEC-0003-question-bank-and-review.md`
- `docs/architecture/api-contracts.md` §Question bank
- `docs/architecture/database-design.md`
