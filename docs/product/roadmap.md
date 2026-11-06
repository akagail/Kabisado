# Roadmap

**Status:** Approved — delegated by repository owner, 2026-11-06
**Owner:** Product / Engineering
**Last updated:** 2026-11-06

No calendar dates are committed. The roadmap is ordered by dependency and risk.
Dates require team capacity, content readiness, and funding decisions.

## Phase 0 — Engineering foundation (complete)

**Goal:** make the repository safe and predictable to build in.

- Agent instructions, documentation standards, and ticket workflow.
- Product requirements and proposed MVP scope.
- Architecture, ADRs, database direction, AI architecture.
- CI for frontend and backend; Docker Compose local stack.
- Minimal Next.js and Django scaffolds with health checks.
- Security, testing, and deployment guidelines.

**Exit criteria:** initialization report reviewed; architecture and MVP approved;
CI green on the initial commit.

**Outstanding from Phase 0:** Docker Compose has not been run (Docker not
installed), and remote CI has not run because the repository is unpushed.

## Phase 1 — Core practice loop (private alpha)

**Epic E1 — Accounts and access**

- Registration, login, logout, password reset.
- Profile and target exam.
- Account deletion and export request.

**Epic E2 — CSE catalogue**

- Exam family / exam / version / subject / topic models.
- Seed CSE Professional and Subprofessional coverage.
- Admin catalogue management.

**Epic E3 — Question bank**

- MCQ, choices, explanation, source reference.
- Authoring and review workflow.
- Import tooling for reviewed content.
- Flagging and correction.

**Epic E4 — Practice and results**

- Practice set generation by topic.
- Untimed and timed sessions.
- Answer persistence, idempotent submit, auto-submit.
- Per-attempt content snapshot (ADR-0007).
- Results and explanations.

**Epic E5 — Progress analytics**

- Attempt and response history.
- Accuracy by subject/topic.
- Weak-topic rule and display.

**Content readiness (parallel, blocking):** 300+ reviewed CSE Professional items
across all four subjects, with a named accountable reviewer. Engineering can
finish before content does; the alpha cannot start.

**Exit criteria:** increment 1 exit criteria in
[mvp-scope.md](mvp-scope.md) are met.

## Phase 2 — Personal materials and AI study aids (public beta)

**Epic E6 — Material ingestion**

- Presigned upload, validation, private storage.
- PDF/DOCX text extraction.
- Processing status, retries, deletion.

**Epic E7 — AI platform**

- Provider adapter and fake test provider.
- Prompt registry and versioning.
- RAG retrieval over material chunks.
- Quotas, caching, cost accounting, spend caps.
- Prompt-injection defences and evaluation suite.

**Epic E8 — Generated study aids**

- Summaries and flashcards with source citations.
- MCQ generation and review queue.
- Provenance panel and flagging.
- Unverified private practice, excluded from weak-topic diagnosis (`AI-10`).

**Epic E9 — Flashcard study**

- Deck/list view, study mode, known/unknown.
- Basic review history (not spaced repetition).

**Exit criteria:** increment 2 exit criteria are met; privacy review complete.

## Phase 3 — Launch hardening

**Epic E10 — Trust and safety**

- Email verification, abuse controls, rate limits.
- Content moderation and takedown process.

**Epic E11 — Operations**

- Observability, alerting, backups, restore drill.
- Incident runbook, on-call expectation, support process.

**Epic E12 — Compliance and accessibility**

- Privacy policy, terms, data-processing disclosures.
- WCAG 2.2 AA audit and fixes.
- Account deletion/export verified end to end.

**Epic E13 — Release**

- Production hosting decision.
- Deployment pipeline with manual approval.
- Load test and launch checklist.

## Phase 4 — Post-MVP

Ordered by expected value, not commitment:

1. Identification and fill-in-the-blank exercises.
2. Spaced repetition and study scheduling.
3. Rule-based and then adaptive recommendations.
4. Full CSE mock exam simulation.
5. Subprofessional launch and Filipino localization.
6. External material discovery with licensing.
7. Additional exam families (PRC licensure, UPCAT, others).
8. Payments, plans, and institutional accounts.
9. Native/mobile and offline study.
10. Cohort and instructor tools.

## Cross-cutting workstreams

These run in parallel and are not "phases":

- **Content operations:** sourcing, authoring, review, correction, licensing.
- **Security and privacy:** threat modelling, dependency patching, access review.
- **Accessibility:** design reviews and audits.
- **Observability:** metrics, logs, traces, alerts.
- **Documentation:** specs, ADRs, runbooks, changelog.

## Dependencies

```text
Phase 0 ──► Phase 1 ──► Phase 2 ──► Phase 3
               │            │
               └── content ops ──┘
```

- Phase 2 requires object storage and an approved AI provider.
- Phase 3 requires a hosting decision and a privacy review.
- Content operations must start during Phase 1; it is the most likely schedule
  risk.
- Payments are deliberately after Phase 3 unless the business model requires
  otherwise.

## Prioritization rules

1. Security and data-loss prevention before new features.
2. Unblock the core learning loop before adding surface area.
3. Prefer work that reduces a named risk.
4. Do not start a phase while its predecessor's exit criteria are unmet, unless a
   documented exception is approved.

## Open decisions

Resolved on 2026-11-06 (see [prd.md](prd.md#14-decision-log)):

- Launch exam and version: CSE Professional content, 14 March 2027 CSE-PPT;
  Subprofessional catalogue only.
- Personal upload for public beta: yes, increment 2; not MVP.
- Free/paid model: free through the private alpha and beta; no payments.
- MVP scope: increment 1 only.

Still open:

- AI provider(s) and data-processing terms (`KAB-003`).
- Object storage and transactional email providers.
- Production backend host.
- Team capacity and target dates.
- Named content curator beyond the repository owner.
