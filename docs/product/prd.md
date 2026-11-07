# Product Requirements Document

**Status:** Approved — product decisions delegated by the repository owner, 2026-11-06
**Owner:** Product
**Last updated:** 2026-11-06
**Companion documents:** [product-overview.md](product-overview.md),
[target-users.md](target-users.md), [product-requirements.md](product-requirements.md),
[mvp-scope.md](mvp-scope.md), [user-flows.md](user-flows.md),
[ai-capabilities.md](ai-capabilities.md),
[cse-exam-reference.md](cse-exam-reference.md)

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

**Proposed — Checkpoint 3, awaiting approval.** The MVP is increment 1: the CSE
Professional core practice loop, released as a private alpha. Personal materials,
AI study aids, and flashcards form a fast-follow public beta; launch hardening
precedes public availability.

| Release | Scope |
| --- | --- |
| MVP | F1–F11: accounts, profile, catalogue, question bank, untimed and timed practice, results, analytics, weak topics, flagging, account deletion |
| Fast-follow beta | Upload and extraction, AI platform, AI summaries and generated items, flashcards |
| Launch hardening | Verification, abuse controls, observability, backups, legal pages, accessibility audit, load test |

The feature list, per-feature acceptance criteria, release map, and exclusions are
in [mvp-scope.md](mvp-scope.md). Journeys, error states, and edge cases are in
[user-flows.md](user-flows.md). No implementation scope is approved until that
document is approved.

## 7. Functional scope

Functional requirements and stable IDs live in
[product-requirements.md](product-requirements.md):

| Area | Prefix | Release |
| --- | --- | --- |
| Authentication and profile | `AUTH` | MVP (email verification in hardening) |
| Examination catalogue | `CAT` | MVP |
| Materials and extraction | `MAT` | Fast-follow beta |
| AI study aids | `AI` | Fast-follow beta |
| Question bank and review | `QST` | MVP (flashcards in beta) |
| Practice sessions | `PRA` | MVP |
| Analytics | `ANL` | MVP (score trend if schedule allows) |
| Recommendations | `REC` | Post-MVP |
| Content discovery | `DIS` | Post-MVP (the no-unlicensed-ingestion rule applies now) |
| Administration | `ADM` | MVP (generation queues in beta) |

Conflicts resolved at Checkpoint 3:

- `QST-02` requires a source reference for every question. Provenance is defined
  as an external citation **or** an authoring record (author, coverage area,
  review date).
- `PRA-07` pause/resume is not in the MVP. Refresh-based resume (`PRA-03`) is the
  MVP behaviour; explicit pause is post-MVP.

Still open: none at product level. The `AI-05` review boundary is resolved in
[ai-capabilities.md](ai-capabilities.md): users may practise their own unreviewed
items privately and labelled, and such attempts are excluded from weak-topic
diagnosis.


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

Resolved by the decision log are not repeated here. Remaining:

1. Who becomes the content curator beyond the repository owner, and when?
2. How is content reused when a second exam version is seeded (duplicate topics
   or link versions)? Needs an ADR before the next CSC announcement is modelled.
3. What does Kabisado promise a learner who is not sitting the 14 March 2027
   exam? Replacement exams are not yet announced.
4. Are institutional or school partnerships pursued after the beta?
5. What team capacity and target dates can be committed without overpromising?

## 14. Decision log

Product decisions were delegated to the agent by the repository owner on
2026-11-06. Architecture decisions and provider selections remain separate gates.

| ID | Decision | Outcome | Date |
| --- | --- | --- | --- |
| D1 | MVP definition | Increment 1, core practice loop, private alpha | 2026-11-06 |
| D2 | Subprofessional at launch | Catalogue and Clerical Ability modelled; practice content deferred | 2026-11-06 |
| D3 | Content gate | 300+ reviewed Professional items; repository owner is accountable reviewer until a curator is appointed; authors never review their own items | 2026-11-06 |
| D4 | Pause/resume | Post-MVP; refresh-based resume only | 2026-11-06 |
| D5 | Attempt history | Snapshot item content at attempt start (ADR-0007) | 2026-11-06 |
| D6 | AI review boundary | Two tiers: unverified private (owner only, excluded from diagnosis) and reviewed shared | 2026-11-06 |
| D7 | AI quality gates | Accept proposed thresholds: 100% citations resolve, ≥95% validation, ≥90% factual, ≥80% helpful, 100% injection, 0 exposure | 2026-11-06 |
| D8 | AI quota (provisional) | 20 generation jobs per user per day, 200 per month; global cap set with provider pricing | 2026-11-06 |
| D9 | Language | English UI; Filipino source and topic content; English AI output in beta | 2026-11-06 |
| D10 | Pricing | Free through alpha and beta; no payments | 2026-11-06 |
| D11 | Practice UX | Flag from results only; no onboarding diagnostic; retakes allowed | 2026-11-06 |
| D12 | Data export | Manual fulfilment at alpha, stated as within 7 days | 2026-11-06 |
| D13 | Export format | JSON archive plus CSV, documented format | 2026-11-06 |
| D14 | Catalogue access | Authenticated only; no public catalogue in the MVP | 2026-11-06 |
| D15 | History view | Pagination only; no filters in the MVP | 2026-11-06 |

| Date | Change | Approved by |
| --- | --- | --- |
| 2026-11-06 | Draft created from existing product documents; exam scope verified | Repository owner (proceeded) |
| 2026-11-06 | Checkpoint 3 MVP proposed; Checkpoint 4 flows; Checkpoint 5 AI policy | Repository owner (proceeded) |
| 2026-11-06 | D1–D12 decided; PRD, MVP scope, flows, and AI policy approved | Repository owner (delegated) |
