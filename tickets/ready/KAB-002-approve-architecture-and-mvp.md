# KAB-002: Approve Architecture, ADRs, and MVP Scope

**Status:** READY
**Type:** task
**Priority:** P0
**Epic:** E0 Foundation
**Owner:** Repository owner
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (decision ticket)
**Related ADRs:** ADR-0001 … ADR-0006
**GitHub issue:** https://github.com/akagail/Kabisado/issues/26

## 1. Description

Review the proposed architecture, six ADRs, product requirements, and MVP scope.
Record an explicit decision for each: approve, amend, or reject.

This is a human decision gate. An agent must not self-approve.

## 2. Business justification

Product implementation must not start on unapproved architecture or scope.
Ambiguity here causes expensive rework and inconsistent agent behaviour.

## 3. Scope

In:

- ADR-0001 modular monolith.
- ADR-0002 technology stack and versions.
- ADR-0003 REST/DRF.
- ADR-0004 session auth + same-origin proxy.
- ADR-0005 AI adapter + RAG.
- ADR-0006 presigned uploads.
- `docs/product/mvp-scope.md` increments and exclusions.
- `docs/product/product-requirements.md` priorities.
- CSE Professional as the launch exam.

Out:

- Implementing any decision.
- Selecting vendors (KAB-003).
- Content sourcing (KAB-004).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-001 | ticket | in review |

## 5. Acceptance criteria

- [ ] Each ADR has an explicit status: Approved, Proposed with changes, or
      Rejected with rationale.
- [ ] Auth model is approved or replaced with a documented alternative.
- [ ] MVP increments and out-of-scope list are approved or amended.
- [ ] Launch exam and level are confirmed.
- [ ] Required amendments are applied to the docs.
- [ ] Decisions are recorded in the ticket and dated.

## 6. Implementation checklist

- [ ] Review ADR index and each ADR.
- [ ] Review product requirements and MVP scope.
- [ ] Review architecture docs for contradictions.
- [ ] Record decisions.
- [ ] Update ADR statuses and docs.
- [ ] Unblock KAB-101+ tickets.

## 7. Testing checklist

- [ ] Documentation links resolve.
- [ ] No contradictory statements remain between roadmap, MVP scope, and
      requirements.
- [ ] Decision record is complete enough for a new agent to proceed.

## 8. Validation evidence

Decision record:

```text
ADR-0001: pending
ADR-0002: pending
ADR-0003: pending
ADR-0004: pending
ADR-0005: pending
ADR-0006: pending
MVP scope: pending
Launch exam: pending
```

## 9. Risks and notes

- Delaying this blocks all product work.
- Approving without reading the trade-offs shifts the risk to implementation.

## 10. References

- `docs/architecture/decisions/README.md`
- `docs/product/mvp-scope.md`
- `docs/product/product-requirements.md`
