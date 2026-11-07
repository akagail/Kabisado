# Phase 4 Clearance Model

**Status:** Approved — 2026-11-07
**Owner:** Engineering / Product  
**Approved by:** Repository owner
**Last updated:** 2026-11-07  
**Companion:** [deployment-hosting-requirements.md](../operations/deployment-hosting-requirements.md), [open-decisions.md](../decisions/open-decisions.md), [SPEC-0001..0005](../specifications/)

This document defines the **Staged Approval and Free-First Development** approach for Phase 4 implementation. It replaces the single-gate "approve everything before implementation" model with a three-category progression that allows local development to begin as soon as foundational specifications are approved, while keeping production provider decisions as explicit prerequisites for their respective features.

---

## 1. Foundational Prerequisites (Category A)

These must be reviewed and approved by the repository owner before any application code is written. They are sequential: SPECs are reviewed before the database design; the database design is finalized before API contracts; the API contracts are validated before threat model and data map complete.

| # | Document | Current status | What it covers | Required before any code |
| --- | --- | --- | --- | --- |
| 1 | **SPEC-0001–0005** | **Approved** (2026-11-07) | Five MVP feature specifications (problem, goals, criteria, API, security) | Approved as the initial MVP baseline. |
| 2 | **Database design** (`database-design.md`) | **Approved** (2026-11-07) | ERD, fields, constraints, indexes, ownership rules, migration plan | Two additive gaps documented: `questions_question.author_id` and `provenance`. |
| 3 | **API contracts** (`api-contracts.md`) | **Finalized** (2026-11-07) | Endpoints, request/response, auth, permissions, error handling, pagination | Cross-referenced against approved specs and database design. |
| 4 | **Initial threat model + data map** | **Initial pass complete** (2026-11-07) | Trust boundaries, STRIDE threats per boundary, data inventory, Philippine Data Privacy Act considerations, account deletion flow | `docs/engineering/threat-model.md`, `docs/operations/data-map.md`. Full sign-off before public beta. |

**Sequential dependency:** SPECs → database design → API contracts → threat model/data map. Missing one blocks the next.

**What can proceed while Category A items remain incomplete:**
- All documentation cleanup (Phase 3) — already complete.
- Open-decisions tracking — ongoing, no change needed.
- Multi-agent implementation plan is ready for execution once Category A clears.

**Category A status: cleared 2026-11-07** (see §6). Phase 4 local
implementation may proceed; Category B runs in parallel and Category C gates
fire only per feature.

---

## 2. Parallel Planning Requirements (Category B)

These should be completed alongside unrelated implementation work. They do not block local development. They accumulate toward their relevant release gates without stopping implementation.

| Item | Owner | When it closes | Release gate this feeds |
| --- | --- | --- | --- |
| **Content sourcing plan** (`docs/product/content-sourcing-plan.md`) | Product / Content | Before implementing content ingestion or AI-generated question pipeline | KAB-004 checklist; 300-item alpha gate |
| **Provider evaluations** (free-tier options, limitations, pricing, upgrade triggers, migration paths) | Engineering / Procurement | Ongoing; per-item resolved when provider selected | O1/O2 readiness |
| **Production hosting evaluation** (Stage 2 provisional choices, cost estimates) | Engineering | During Stage 2 provisioning | KAB-112 launch hardening |
| **Deployment preparation** (CI/CD environments, smoke tests, rollback rehearsals) | Engineering | Along the way; gates at production activation | KAB-112 checklist |

**Free-first principle for evaluations:** Document findings without making purchases. Provider selection requires separate explicit approval.

---

## 3. Feature-Specific and Release Gates (Category C)

These are category-B requirements that apply to a specific workflow. If they are unresolved, the relevant functionality cannot be implemented or released — not because local dev is blocked, but because deploying that feature to real users is blocked.

| Gate | Feature affected | Resolution gate | Blocking if unresolved |
| --- | --- | --- | --- |
| **O1 AI provider + DPA** | Material summarization, MCQ generation, flashcards (Beta) | Provider selection, DPA, budget commitment | Cannot process real user documents through an LLM |
| **O2 Object storage** | Material uploads (Beta) | S3-compatible provider, cost commitment | Cannot enable hosted user-file uploads |
| **Real transactional email** | Password reset, registration verification | Provider selected and configured behind abstraction | Cannot send real emails to alpha users (console backend only for local dev) |
| **Production backend hosting** | Production deployment | Hosting commitment, cost, operational model | Cannot deploy to production |
| **Security/backup/recovery controls** | Accepting real user data | Threat model, backup retention, restore drill | Cannot accept real users securely |

---

## 4. Free-First Development Policy

All Phase 4 implementation follows these principles:

1. **Prefer open-source software and free services.** Use `docker-compose` for local development infrastructure wherever practical.
2. **Avoid paid dependencies during initial development.** No real AI provider calls, no hosted object storage, no transactional email until explicitly needed.
3. **Keep integrations replaceable.** Provider-independent abstractions (ADR-0005 for AI, ADR-0006 for storage) are the contract, not the implementation.
4. **Use environment variables for provider-specific configuration.** Never hardcode credentials.
5. **Do not compromise security, privacy, backups, or data integrity just to remain free.** Weaknesses trigger reversion to the prior-security state, not free-tier substitution.
6. **Document unavoidable future costs before they become commitments.** Every paid service has an upgrade trigger documented in `deployment-hosting-requirements.md`.
7. **Obtain explicit approval before selecting or purchasing paid services.** Provider selections under O1, O2, and O4 require separate human approval, recorded in the open-decisions register.

---

## 5. Revised Phase 4 Readiness Summary

| Category | Criteria | Status | Blocked by |
| --- | --- | --- | --- |
| **A — Foundational** | All four items reviewed and approved | **Satisfied 2026-11-07** — SPECs approved, DB design approved (2 additive gaps), API contracts finalized, threat model + data map initial pass complete | Nothing for MVP local development; full security sign-off before public beta |
| **B — Parallel** | Content sourcing plan + provider evaluations documented | **Running in parallel** with implementation | None — does not block code |
| **C — Release gates** | O1, O2, real email, production hosting selected for respective features | **Deferred** under free-first policy | Separate approvals per item when the feature/release needs them |

**Practical exit criterion:** Local Docker development works end-to-end for all MVP features. None of the Category-C gates fire because Category-B parallel planning has been sufficiently advanced. The first feature implementation begins on the designated branch (`feat/KAB-NNN-title`) from `main`.

**Phase 4 status: CLEARED for local MVP implementation (2026-11-07).**

---

## 6. Review Record

| Step | Document | Outcome | Date |
| --- | --- | --- | --- |
| 1 | **SPEC-0001–0005** | **Approved** as the initial MVP baseline. No critical blockers identified. | 2026-11-07 |
| 2 | **Database design** | **Approved** as implementation baseline. Two additive gaps documented (`questions_question.author_id`, `provenance`). | 2026-11-07 |
| 3 | **API contracts** | **Finalized** against specs and DB design. Known clarifications recorded in the document. | 2026-11-07 |
| 4 | **Threat model + data map** | **Initial pass complete** (`threat-model.md`, `data-map.md`); full sign-off before public beta. | 2026-11-07 |

Next reviews are Category C release gates, triggered per feature (O1 for AI,
O2 for hosted uploads, real email before alpha, O4 before production).

---

## 7. What Hasn't Changed

- All approved ADRs (ADR-0001 through 0006 statuses: 0004 & 0006 now Approved, 0008 still Draft).
- Phase 3 documentation cleanup complete (central docs index, trimmed product docs, archived plans, rewritten specs).
- Free-first infrastructure stages (4 stages with upgrade triggers) documented in `deployment-hosting-requirements.md`.
- Multi-agent implementation plan ready for execution.

**What has changed:** The clearance model is now staged rather than monolithic. Implementation may begin after Category A approval, with parallel planning (Category B) running concurrently, and Category-C release gates firing only when their respective features need real infrastructure.
