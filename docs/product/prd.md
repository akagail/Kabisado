# Product Requirements Document

**Status:** Draft — requires approval
**Owner:** Product
**Last updated:** 2026-11-06
**Companion documents:** [product-overview.md](product-overview.md),
[target-users.md](target-users.md), [product-requirements.md](product-requirements.md),
[mvp-scope.md](mvp-scope.md), [cse-exam-reference.md](cse-exam-reference.md)

This PRD is the entry point for product definition. Requirement IDs stay in
[product-requirements.md](product-requirements.md); this document does not
duplicate or renumber them.

Sections marked **Pending** are completed in later Phase 2 checkpoints and must
not be treated as decided.

## 1. Problem

Preparing for Philippine government and professional examinations is expensive,
fragmented, and hard to personalize. Reviewers are static PDFs or unstructured
social-media material. Learners cannot easily tell what they do not know, why an
answer is wrong, or what to study next, and high-quality review content is
scattered across sources with unclear ownership.

For the CSE specifically, the official announcement publishes coverage areas but
no review material, no item-level guidance, and no diagnosis. Learners are left to
infer their own weaknesses.

## 2. Vision and value proposition

Kabisado turns a learner's own review materials and a curated examination
catalogue into a personalized study loop: **study → practice → understand the
mistake → focus on the weak topic → repeat**.

Answers must be explainable, progress visible, and sources attributable. The
product should feel like a competent review coach, not a PDF viewer with a chat
box.

| For | Kabisado provides |
| --- | --- |
| CSE candidates | A structured CSE study path with practice, explanations, and weak-topic feedback |
| Self-directed learners | Their own notes and reviewers turned into flashcards and practice questions |
| Repeat takers | Diagnosis of weak areas instead of restarting from page one |
| Content curators | A traceable pipeline from source material to approved learning items |

## 3. Target users

Personas are **hypotheses**, not validated research. See
[target-users.md](target-users.md) for profiles, assumptions, and the validation
plan.

| Persona | Segment | MVP relevance |
| --- | --- | --- |
| CSE Professional aspirant | Primary | In scope |
| Subprofessional candidate | Secondary | Catalogue coverage only at launch |
| Licensure / entrance-exam candidate | Later | Not in scope; data model must not block |
| Content curator | Internal | In scope (admin and review workflow) |

## 4. Goals and non-goals

**Goals**

1. Help a CSE Professional candidate practise the published coverage areas and
   identify weak subjects and topics.
2. Explain every answer, with a traceable source or authoring rationale.
3. Turn a learner's own reviewer into practice material with provenance and
   review, without leaking it to other users.
4. Model additional examinations without a rewrite.
5. Keep AI output grounded, labelled, and never presented as official CSC
   material.

**Non-goals for the MVP**

- Processing CSC applications, issuing eligibility, or predicting an official
  rating.
- Guaranteeing a passing score.
- A general-purpose chatbot.
- Proctoring, certification, or high-stakes assessment.
- Social feeds, leaderboards, public profiles, or content sharing.
- Native mobile apps, offline mode, or payments.
- Republishing copyrighted reviewers or recalled exam items.

## 5. Launch examination

Verified against Examination Announcement No. 06, s. 2026. Details, sources, and
unverified items: [cse-exam-reference.md](cse-exam-reference.md).

| Field | Value |
| --- | --- |
| Examination | CSE-PPT, 14 March 2027 |
| Levels | Professional and Subprofessional |
| Passing grade | General rating of at least 80.00 |
| Professional coverage | General Information, Verbal, Numerical, Analytical |
| Subprofessional coverage | General Information, Verbal, Numerical, Clerical |
| Item count / time limit | **Unverified** — not published in the announcement |

**Recommendation (needs approval):** launch with CSE Professional content.
Model the Subprofessional catalogue and Clerical Ability, but defer
Subprofessional practice content until after the Professional launch.

## 6. MVP definition

**Pending — Checkpoint 3.** The repository currently defines the MVP three ways:
`product-overview.md` treats materials and AI as MVP, `mvp-scope.md` describes
three increments with public beta requiring increments 1 and 2, and
`product-requirements.md` marks AI requirements `MUST`.

**Recommendation (needs approval):** the MVP is increment 1, the core practice
loop, validated in private alpha. Personal materials and AI study aids follow as
a fast-follow beta, gated by provider selection and content review.

No implementation scope is approved until this section is resolved.

## 7. Functional scope

Functional requirements and stable IDs live in
[product-requirements.md](product-requirements.md):

| Area | Prefix | MVP status |
| --- | --- | --- |
| Authentication and profile | `AUTH` | Pending MVP decision |
| Examination catalogue | `CAT` | Pending MVP decision |
| Materials and extraction | `MAT` | Pending MVP decision |
| AI study aids | `AI` | Pending MVP decision |
| Question bank and review | `QST` | Pending MVP decision |
| Practice sessions | `PRA` | Pending MVP decision |
| Analytics | `ANL` | Pending MVP decision |
| Recommendations | `REC` | Post-MVP |
| Content discovery | `DIS` | Post-MVP |
| Administration | `ADM` | Pending MVP decision |

Known requirement conflicts to resolve in Checkpoint 3:

- `QST-02` requires a source reference for every question; original items have no
  external source. Define source as an external citation **or** authoring
  provenance.
- `AI-05` and the AI architecture disagree on whether a user may practise their
  own unreviewed generated items.
- `PRA-07` (pause/resume) is `SHOULD` while the related ticket promises only
  resume-after-refresh.

## 8. Non-functional requirements

Summarised from `product-requirements.md`; IDs remain there.

- **Security:** object-level authorization on every read and write; uploaded
  files validated by extension, MIME type, magic bytes, and size; no secrets in
  the client; rate limits on auth, upload, and AI endpoints.
- **Privacy:** R.A. 10173 compliance; personal materials private by default; no
  third-party model training on user content without explicit consent; account
  deletion removes derived content.
- **Accessibility:** WCAG 2.2 AA for core study flows; keyboard operable; not
  colour-only; reduced motion respected.
- **Performance:** usable on mid-range Android over intermittent connections;
  practice interactions must not block on AI calls.
- **Reliability:** idempotent practice submission; per-answer persistence;
  migrations reversible or documented.
- **Auditability:** AI calls and generated content store provider, model, prompt
  version, source, and timestamp.

## 9. Success metrics

Single canonical set for Phase 2. Targets are **hypotheses** with no baseline;
they become commitments only after approval and beta data.

| ID | Metric | Definition | Target (proposed) | Increment |
| --- | --- | --- | --- | --- |
| M1 | Activation | New users who complete one practice session within 24 hours of registration | No target until baseline exists | 1 |
| M2 | Learning loop | Median completed practice sessions per user in the first 7 days | ≥ 3 | 1 |
| M3 | Retention | Activated users active on day 7 | ≥ 40% | 1 |
| M4 | Session completion | Median answered items ÷ started items per session | ≥ 80% | 1 |
| M5 | Explanation quality | Share of rated explanations marked helpful | ≥ 70% at beta; 80% as GA ambition | 1 |
| M6 | Diagnostic usefulness | Usability participants can name a next study action from the weak-topic view | Majority of participants | 1 |
| M7 | Content readiness | Human-reviewed CSE Professional items live | ≥ 300 before alpha | 1 |
| M8 | Trust and safety | Confirmed cross-user data exposures; unresolved copyright takedowns; unresolved high-severity findings | 0 | 1–3 |
| M9 | AI cost | Cost per monthly active user (increment 2 features) | Within an approved cap, to be set with the provider decision | 2 |

Notes:

- Prior documents disagreed on explanation quality (70% vs 80%) and on the
  retention horizon (7-day vs 4-week). This set uses 70% for beta and a day-7
  retention measure. A 4-week return rate is added once beta data exists.
- Exam outcome (pass rate) is deliberately not a product metric: it cannot be
  attributed to Kabisado and would encourage overclaiming.

## 10. Assumptions

| ID | Assumption | Status |
| --- | --- | --- |
| A1 | CSE Professional is the highest-demand initial segment | Unverified |
| A2 | Users have an email address and a browser; many use mid-range Android phones | Unverified |
| A3 | Learners value diagnosis and explanations more than question volume | Unverified |
| A4 | Learners will upload personal reviewers when privacy is clear | Unverified |
| A5 | Original, human-reviewed items are sufficient for launch | Unverified |
| A6 | Grounded AI can produce usable items and explanations at acceptable cost | Unverified |
| A7 | A free tier is expected and willingness to pay is unknown | Unverified |

Validation methods are in [target-users.md](target-users.md).

## 11. Constraints

| ID | Constraint |
| --- | --- |
| C1 | Official CSC sources are authoritative; the CSC may amend the scope by supplemental announcement |
| C2 | No CSC affiliation, accreditation, endorsement, or use of CSC name and logo |
| C3 | Official exam items are not public domain; only original or licensed content |
| C4 | Personal data is handled under R.A. 10173 with a published privacy notice |
| C5 | AI provider, object storage, email, and hosting are not selected |
| C6 | Content operations capacity is unknown; 300+ reviewed items is a hard gate |
| C7 | Small team; no calendar dates committed until capacity is known |
| C8 | No production hosting committed; deployment stays provider-agnostic |

## 12. Dependencies and approval gates

| Dependency | Needed by | Status |
| --- | --- | --- |
| Approved product requirements (this PRD) | Everything | Draft |
| Approved exam scope (CSE reference) | Catalogue and content | Verified, awaiting approval |
| One MVP definition | Specs and tickets | Open |
| Architecture and ADRs | Feature specs | Proposed |
| Content sourcing and review plan (KAB-004) | Content seeding | Not started |
| Threat model and privacy review (KAB-005) | Public beta | Not started |
| Provider selection (KAB-003) | Upload and AI increments | Not started |

## 13. Open questions

1. Is the MVP increment 1 only, or increments 1 and 2?
2. Does Subprofessional ship with catalogue-only coverage at launch?
3. Who is the accountable content reviewer, and what is the correction and
   takedown process?
4. May a user practise their own unreviewed AI-generated items, clearly labelled?
5. Is explicit pause/resume in the MVP, or only resume-after-refresh?
6. Does an exam-version change duplicate topics, or reuse them with a version
   link?
7. Do practice sessions snapshot question text and options, or reference live
   rows?
8. Is the interface English-only at launch, with Filipino content where the exam
   requires it?
9. Is there a paid tier at launch, and does it gate AI usage?
10. What is the 2027 exam target if a learner is not taking the 14 March sitting?

## 14. Approval log

| Date | Change | Approved by |
| --- | --- | --- |
| 2026-11-06 | Draft created from existing product documents; exam scope verified | Pending |
