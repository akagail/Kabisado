# KAB-004: CSE Content Sourcing, Review, and Attribution Plan

**Status:** IN PROGRESS
**Type:** documentation
**Priority:** P1
**Epic:** E0 Foundation / Content Operations
**Owner:** Product / Content
**Created:** 2026-11-06
**Updated:** 2026-11-10
**Specification:** not required (operations plan)
**Related ADRs:** none
**GitHub issue:** https://github.com/akagail/Kabisado/issues/28
**Pull request:** https://github.com/akagail/Kabisado/pull/37

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
| `docs/product/cse-exam-reference.md` | reference | verified for the 2027 bulletin (2026-11-06) |
| KAB-002 (launch exam) | decision | resolved for planning — CSE Professional is the launch exam (`roadmap.md`) |

## 5. Acceptance criteria

- [ ] `docs/product/content-sourcing-plan.md` exists and is approved. — drafted
      2026-11-10; approval is a human action.
- [x] Every source category has a permitted/prohibited rule (§1–2).
- [x] The attribution record schema is defined (§3).
- [x] Reviewer roles and a second-review requirement are defined (§4).
- [x] A takedown and correction workflow is documented (§8).
- [x] The increment 1 seed target and quality bar are stated (§5–6).
- [x] AI-assisted authoring disclosure rules are stated (§7).
- [x] A named accountable content reviewer is recorded — **Repository owner
      confirmed as initial alpha curator (2026-11-07), subject to manageable
      workload.**

## 6. Implementation checklist

- [x] Re-check the current official CSC bulletin and record its date/URL
      (`cse-exam-reference.md` §1).
- [x] Define source categories and rights.
- [x] Define the item schema and review checklist.
- [x] Define the takedown workflow and response SLA.
- [ ] Estimate authoring effort and cost — capacity and budget remain open
      questions (§10).
- [ ] Get product/owner approval.

## 7. Testing checklist

- [ ] Every seeded item has a source or original-author record. — applies once
      KAB-103 seeds items.
- [ ] Every licensed item has licence, territory, and expiry. — no licensed
      items yet.
- [x] No official or leaked exam item is present — nothing is seeded; the
      catalogue contains coverage-area names only.
- [ ] A sample of 20 items passes the review checklist. — needs items.
- [x] The takedown contact and process are reachable (§8).

## 8. Validation evidence

```text
docs/product/content-sourcing-plan.md written 2026-11-10.
Sections: sources, no-reproduction rule, item schema, review workflow,
quality bar, 300-item volume plan, AI rules, takedown, operations, risks.
Open items: approval, curator capacity, Subprofessional timing, licensing budget.
```

## 9. Risks and notes

- Coverage details can change between bulletins.
- AI-generated items require human review; do not publish unreviewed shared
  content.
- Do not mirror third-party content behind a paywall or access control.

## 10. References

- `docs/product/cse-exam-reference.md`
- `docs/engineering/security-guidelines.md` §15
