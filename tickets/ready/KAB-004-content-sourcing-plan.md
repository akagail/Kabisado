# KAB-004: CSE Content Sourcing, Review, and Attribution Plan

**Status:** READY
**Type:** documentation
**Priority:** P1
**Epic:** E0 Foundation / Content Operations
**Owner:** Product / Content
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (operations plan)
**Related ADRs:** none
**GitHub issue:** https://github.com/akagail/Kabisado/issues/28

## 1. Description

Define how Kabisado sources, authors, reviews, attributes, and retires CSE review
content, including the rule for never reproducing copyrighted or leaked exam
items.

## 2. Business justification

Content is the most likely launch bottleneck and the largest legal risk. The
engineering team cannot seed the catalogue without an approved sourcing and
review model.

## 3. Scope

In:

- Source categories: official CSC coverage, original items, licensed third-party
  material, user uploads.
- Permitted and prohibited sources.
- Licence and attribution record fields.
- Authoring workflow and reviewer roles.
- Quality bar for MCQs, explanations, and flashcards.
- Correction, flagging, and takedown process.
- Seed target for increment 1 (e.g. 300 reviewed CSE Professional items).
- Exam-version tracking (bulletin, item count, time limit, passing rate).
- AI-assisted authoring rules and disclosure.

Out:

- Writing the actual item bank.
- Signing licences.
- Building the admin UI (KAB-103).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| `docs/product/cse-exam-reference.md` | reference | drafted |
| KAB-002 (launch exam) | decision | pending |

## 5. Acceptance criteria

- [ ] `docs/product/content-sourcing-plan.md` exists and is approved.
- [ ] Every source category has a permitted/prohibited rule.
- [ ] The attribution record schema is defined.
- [ ] Reviewer roles and a second-review requirement are defined.
- [ ] A takedown and correction workflow is documented.
- [ ] The increment 1 seed target and quality bar are stated.
- [ ] AI-assisted authoring disclosure rules are stated.
- [ ] A named accountable content reviewer is recorded.

## 6. Implementation checklist

- [ ] Re-check the current official CSC bulletin and record its date/URL.
- [ ] Define source categories and rights.
- [ ] Define the item schema and review checklist.
- [ ] Define the takedown workflow and response SLA.
- [ ] Estimate authoring effort and cost.
- [ ] Get product/owner approval.

## 7. Testing checklist

- [ ] Every seeded item has a source or original-author record.
- [ ] Every licensed item has licence, territory, and expiry.
- [ ] No official or leaked exam item is present.
- [ ] A sample of 20 items passes the review checklist.
- [ ] The takedown contact and process are reachable.

## 8. Validation evidence

```text
Plan not yet written.
```

## 9. Risks and notes

- Coverage details can change between bulletins.
- AI-generated items require human review; do not publish unreviewed shared
  content.
- Do not mirror third-party content behind a paywall or access control.

## 10. References

- `docs/product/cse-exam-reference.md`
- `docs/engineering/security-guidelines.md` §15
