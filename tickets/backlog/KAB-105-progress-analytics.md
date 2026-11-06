# KAB-105: Progress Analytics and Weak Topics

**Status:** BACKLOG
**Type:** feature
**Priority:** P1
**Epic:** E5 Analytics
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** required before implementation
**Related ADRs:** ADR-0003
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
| KAB-104 | practice + responses | pending |

## 5. Acceptance criteria

- [ ] Aggregates are correct for a known fixture.
- [ ] Weak topics use the documented rule and boundary values.
- [ ] A user sees accuracy by subject and topic.
- [ ] A user sees recent sessions with dates and scores.
- [ ] Empty state is useful and not an error.
- [ ] Another user's analytics cannot be read (IDOR).
- [ ] Aggregates update after a submitted session.
- [ ] Query count is bounded for the dashboard.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design (aggregate vs. on-the-fly).
- [ ] Implement selectors/aggregates.
- [ ] Implement endpoints.
- [ ] Build dashboard/progress UI.
- [ ] Add indexes.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Boundary tests for the weak-topic rule.
- [ ] Aggregate correctness test.
- [ ] IDOR test.
- [ ] Query-count test.
- [ ] Frontend states test.
- [ ] E2E: submit → see progress.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Start with on-the-fly queries; denormalize only when measured slow.
- Do not expose other users' data in aggregate endpoints.
- Make the threshold configurable and documented.

## 10. References

- `docs/architecture/database-design.md` §3
- `docs/product/product-requirements.md` ANL-01…ANL-05
