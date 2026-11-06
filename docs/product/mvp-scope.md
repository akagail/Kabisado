# MVP Scope

**Status:** Proposed — requires approval
**Owner:** Product
**Last updated:** 2026-11-06

## 1. MVP goal

Prove that CSE Professional learners will repeatedly use a loop of **practice →
explanation → weak-topic diagnosis**, and that AI-assisted study aids built from
their own reviewers are trustworthy enough to pay for or recommend.

The MVP is delivered in three increments. Each increment is independently
testable. Public beta requires increments 1 and 2; general availability requires
increment 3.

## 2. Increment 1 — Core practice loop (private alpha)

**Outcome:** a learner can practise CSE Professional questions, see explanations,
and understand their weakest topics.

In scope:

- Email/password registration, login, logout, password reset.
- Profile: display name, target exam, study preference.
- CSE Professional and Subprofessional catalogue with subjects and topics.
- Seeded, human-reviewed multiple-choice questions with explanations and source
  references. No official CSC items are reproduced.
- Untimed practice by subject/topic.
- Timed practice with auto-submit.
- Per-attempt answer persistence and idempotent submission.
- Results: score, correct answers, explanations.
- Analytics: accuracy by subject and topic, recent history, weak-topic rule.
- Admin: catalogue and question management, content flag review.
- Account deletion and data export request.

Exit criteria:

- A new user can register, practise 20 questions, and see a topic breakdown.
- All acceptance tests for increment 1 pass.
- No critical or high security findings in review.
- 300+ reviewed CSE Professional items across the coverage areas.
- At least 10 usability sessions completed with target users.

## 3. Increment 2 — Personal materials and AI study aids (public beta)

**Outcome:** a learner can turn their own reviewer into flashcards and practice
items, with provenance and review.

In scope:

- PDF upload (DOCX optional) with validation and private storage.
- Asynchronous text extraction; visible status and retry.
- Source-linked AI summaries and flashcard generation.
- AI-generated multiple-choice items with a review queue; unreviewed items are
  private to the generating user or hidden from shared pools.
- Flashcards: create, study, mark known/unknown.
- Material deletion removes derived content.
- Per-user and global AI quotas and spend caps.
- AI provider adapter with at least one implementation and a fake provider for
  tests.
- Provenance panel: source passage, model, prompt version, generation time.
- Content flagging for AI output.

Exit criteria:

- A user uploads a 20-page PDF and receives usable flashcards within the
  processing SLA.
- Every generated item links to a source passage.
- Prompt-injection test suite passes.
- AI cost per active user is measured and within the approved cap.
- Privacy review of the selected AI provider is complete.

## 4. Increment 3 — Launch hardening

**Outcome:** the product is safe, observable, and operable for public use.

In scope:

- Email verification and abuse controls.
- Rate limits on auth, upload, and AI endpoints.
- Structured logging, error tracking, and alerting.
- Backups and a tested restore procedure.
- Privacy policy, terms, and data-processing disclosures.
- Accessibility audit (WCAG 2.2 AA) and fixes for core flows.
- Load test of the practice flow.
- Incident runbook and support process.
- Production deployment approval.

## 5. Explicitly out of scope

- Identification and fill-in-the-blank exercises.
- Full CSE mock exam simulation with section timing.
- Personalized study plans and scheduling.
- Spaced repetition (FSRS or SM-2).
- Weak-topic recommendations beyond a rule-based list.
- External material discovery and ingestion.
- Payments, subscriptions, entitlements, and invoices.
- Social features, leaderboards, public profiles, and sharing.
- Native mobile apps.
- Offline/PWA mode.
- Multi-tenant institutions.
- Exams other than CSE.
- OCR for scanned documents.
- Filipino-language UI and explanations.
- Proctoring or high-stakes certification.

Any addition requires a scope-change approval with impact on schedule, cost, and
risk.

## 6. Dependencies

| Dependency | Needed by | Status |
| --- | --- | --- |
| Approved product requirements | Increment 1 | Draft |
| Approved architecture and ADRs | Increment 1 | Proposed |
| CSE content sourcing and review plan | Increment 1 | Not started |
| Auth and account spec | Increment 1 | Not started |
| Practice and analytics spec | Increment 1 | Not started |
| Object storage provider | Increment 2 | Not selected |
| AI provider and data-processing terms | Increment 2 | Not selected |
| Transactional email provider | Increment 3 | Not selected |
| Production hosting | Increment 3 | Not selected |

## 7. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| AI-generated questions are wrong | Trust loss | Review queue, source links, flagging, no unreviewed shared pool |
| Copyright complaint | Legal and reputational | Original items, recorded licences, takedown process |
| Content seeding takes longer than engineering | Launch delay | Start content ops in parallel; track as a first-class workstream |
| AI cost exceeds budget | Unsustainable | Quotas, caching, spend caps, cheaper models for drafts |
| Users do not trust AI explanations | Low adoption | Human review, citations, transparent labelling |
| Scope creep into recommendations/scheduling | Delay | Explicit out-of-scope list; new tickets require approval |
| Solo/small team capacity | Burnout and quality loss | Small increments, automated checks, no speculative features |

## 8. Success criteria for the MVP

The canonical metric set is in [prd.md](prd.md#9-success-metrics). Targets remain
hypotheses until approved.

## 9. Decisions required

1. Approve or amend the three increments.
2. Confirm CSE Professional as the launch exam; Subprofessional as fast follow.
3. Confirm whether increment 2 is required for public beta.
4. Approve the out-of-scope list.
5. Approve the content-sourcing model and reviewer ownership.
