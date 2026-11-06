# Epics and Backlog Map

**Status:** Proposed
**Owner:** Product / Engineering
**Last updated:** 2026-11-06

An epic is a grouping of related tickets, not a ticket itself. The dependency
graph below is the recommended order; it is not a commitment to dates.

## Phase 0 — Foundation

| Epic | Outcome | Tickets |
| --- | --- | --- |
| E0 Foundation | Repository, docs, CI, local stack, decisions | KAB-001 … KAB-005 |

## Phase 1 — Core practice loop

| Epic | Outcome | Tickets |
| --- | --- | --- |
| E1 Accounts | Users can register, log in, manage their account | KAB-101 |
| E2 CSE catalogue | Exam/subject/topic taxonomy seeded for CSE | KAB-102 |
| E3 Question bank | Reviewed MCQs with explanations and provenance | KAB-103 |
| E4 Practice | Timed/untimed sessions, persistence, scoring, results | KAB-104 |
| E5 Analytics | Accuracy by topic, history, weak-topic rule | KAB-105 |

## Phase 2 — Personal materials and AI

| Epic | Outcome | Tickets |
| --- | --- | --- |
| E6 Materials | Private PDF/DOCX upload, extraction, deletion | KAB-106 |
| E7 AI platform | Provider adapter, prompts, RAG, quotas, evaluation | KAB-107 |
| E8 Study aids | Summaries, flashcards, generated questions, review queue | KAB-108 |
| E9 Flashcards | Study mode and known/unknown tracking | KAB-109 |

## Phase 3 — Launch hardening

| Epic | Outcome | Tickets |
| --- | --- | --- |
| E10 Trust and safety | Verification, abuse controls, moderation | Split from KAB-101/KAB-108 as needed |
| E11 Operations | Logging, metrics, alerts, backups, runbook | KAB-110 |
| E12 Compliance and accessibility | Privacy, WCAG 2.2 AA, performance | KAB-111 |
| E13 Release | Hosting, CD, smoke tests, launch checklist | KAB-112 |

## Dependency graph

```text
KAB-001 Foundation
   ├──► KAB-002 Approve architecture + MVP
   │       ├──► KAB-101 Accounts
   │       │       └──► KAB-104 Practice ──► KAB-105 Analytics
   │       ├──► KAB-102 Catalogue ──► KAB-103 Questions ──► KAB-104
   │       ├──► KAB-106 Materials ──► KAB-107 AI platform ──► KAB-108 Study aids ──► KAB-109 Flashcards
   │       └──► KAB-111 Accessibility/performance
   ├──► KAB-003 Provider selection ──► KAB-106 (storage), KAB-107 (AI), KAB-112 (hosting)
   ├──► KAB-004 Content sourcing ──► KAB-102, KAB-103
   └──► KAB-005 Threat model/privacy ──► KAB-101, KAB-106, KAB-107
KAB-110 Observability ──► KAB-112 Release
KAB-112 Release ──► production launch
```

## Backlog rules

- Only the next 2–3 tickets per workstream should be `READY`.
- Everything else stays in `BACKLOG` until its dependencies and specification are
  settled.
- Feature tickets stay in `BACKLOG` until a specification is approved.
- Decisions requiring human approval are explicitly marked.
- Do not create speculative tickets for post-MVP features; add them when the
  roadmap phase starts.
