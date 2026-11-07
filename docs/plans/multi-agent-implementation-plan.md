# Multi-Agent Implementation Plan

**Status:** Draft — for Phase 3 approval  
**Owner:** Engineering  
**Last updated:** 2026-11-07  

## 1. Purpose

This plan defines how implementation agents will execute the MVP (Increment 1)
feature specifications in parallel while maintaining code quality, architectural
integrity, and clear ownership boundaries.

## 2. Branch Conventions

| Feature | Branch | Base |
| --- | --- | --- |
| KAB-101 Accounts & Profile | `feat/KAB-101-accounts-auth` | main |
| KAB-102 CSE Catalogue | `feat/KAB-102-cse-catalogue` | main |
| KAB-103 Question Bank | `feat/KAB-103-question-bank` | main |
| KAB-104 Practice & Results | `feat/KAB-104-practice-sessions` | main |
| KAB-105 Progress Analytics | `feat/KAB-105-progress-analytics` | main |

- **No direct pushes to main.**
- Each branch targets one ticket and its spec.
- Rebase against `main` before PR.
- PR title: `feat(auth): implement registration, login, logout, profile` (Conventional Commits).
- Link the ticket in the PR description.

## 3. Agent Ownership and Parallelism

| Agent | Primary Tickets | Secondary / Reviews | Sequencing |
| --- | --- | --- | --- |
| **Agent A (Backend Core)** | KAB-101 (accounts), KAB-102 (catalogue) | Review KAB-103, KAB-104 | Start first; provides models/services |
| **Agent B (Backend Domain)** | KAB-103 (questions), KAB-104 (practice), KAB-105 (analytics) | Review KAB-101, KAB-102 | Starts after KAB-102 models ready |
| **Agent C (Frontend Core)** | KAB-101 (auth UI), KAB-102 (catalogue UI) | Review KAB-104, KAB-105 UI | Starts with Agent A |
| **Agent D (Frontend Domain)** | KAB-104 (practice UI), KAB-105 (analytics UI) | Review KAB-103 UI | Starts after KAB-104 backend ready |

**Rules:**
- Backend agents own models, services, selectors, serializers, views, URLs, admin, tests.
- Frontend agents own routes, components, hooks, API client, styling, tests.
- Cross-ticket dependencies are resolved via **shared base models** (User, ExamVersion, Topic) merged early.
- No agent modifies another agent's module without a review from the owning agent.
- Use the service/selector layer for cross-module calls.

## 4. Shared Infrastructure (Merged First)

Before feature branches, these are merged to `main` via a **foundation PR**:

1. Django project scaffold (config, core app, health endpoints, OpenAPI).
2. Next.js scaffold (App Router, API proxy, auth client, shadcn UI).
3. Shared base models: `TimeStampedModel`, `UUIDModel`, `AuditEvent`.
4. Database migrations for accounts, catalogue, question, practice, analytics.
5. CI pipelines (backend-ci, frontend-ci, e2e).
6. Docker Compose for local PostgreSQL + backend + frontend.

**Order of merges:**
1. Foundation PR (scaffolds, CI, Docker) → `main`
2. KAB-101 (accounts) + KAB-102 (catalogue) in parallel → `main` (sequential or same-day)
3. KAB-103 (questions) after KAB-102
4. KAB-104 (practice) after KAB-101 + KAB-103
5. KAB-105 (analytics) after KAB-104

## 5. Cross-Cutting Concerns

| Concern | Owner | Notes |
| --- | --- | --- |
| Session auth + CSRF | Agent A | ADR-0004 (pending security review) |
| API client + error mapping | Agent C | Single module `src/lib/api/client.ts` |
| Type generation / OpenAPI sync | Agent A + C | `drf-spectacular` → TypeScript types |
| Migration discipline | All | One migration per logical change; CI check |
| Security review | Agent A + C | Every PR includes security checklist |
| Accessibility | Agent C + D | WCAG 2.2 AA on core flows |

## 6. Definition of Ready for a Ticket

A ticket moves to `tickets/in-progress/` only when:
- [ ] Specification is **Approved** (not Draft).
- [ ] ADR dependencies are **Approved** (e.g., ADR-0004 for KAB-101).
- [ ] Technical design is written and reviewed (1-pager in the ticket or linked).
- [ ] All models/migrations needed by downstream tickets are available on `main`.
- [ ] Branch created and CI passes on empty branch.

## 7. Definition of Done for a Ticket

A ticket moves to `tickets/review/` only when:
- [ ] All acceptance criteria from the spec are implemented and verified.
- [ ] Backend: services + selectors + API + admin + tests pass.
- [ ] Frontend: routes + components + API client + tests pass.
- [ ] OpenAPI schema matches implementation.
- [ ] Security checklist passed (IDOR, CSRF, rate limit, validation).
- [ ] Accessibility checklist passed (labels, focus, keyboard, ARIA live).
- [ ] Documentation updated (API docs, migration notes, CHANGELOG if needed).
- [ ] PR reviewed by at least one other agent (cross-review).
- [ ] No lint, typecheck, or test failures.
- [ ] Self-review completed in PR description.

## 8. Risk Mitigation

| Risk | Mitigation |
| --- | --- |
| ADR-0004 not approved before KAB-101 starts | KAB-101 stays in BACKLOG; foundation work only until approval |
| KAB-103 question bank depends on KAB-102 catalogue | KAB-102 merged first; shared Topic model available |
| KAB-104 practice needs ADR-0007 snapshot implementation | ADR-0007 is Approved; model includes snapshot fields |
| Frontend API types drift from backend | Generate types from OpenAPI in CI; fail on drift |
| Duplicate validation logic | Backend is authoritative; frontend mirrors for UX only |
| Long-running feature branches | Rebase daily; merge to main within 5 working days of start |
| Security issues found late | Security review in every PR; threat model in KAB-005 before alpha |

## 9. Testing Strategy per Agent

| Agent | Unit | Integration | E2E |
| --- | --- | --- | --- |
| A | Services, models, auth | Auth API, catalogue API | Register → login → logout |
| B | Services, selectors, scoring | Questions, practice, analytics API | Start → answer → submit → results |
| C | API client, hooks, auth forms | Auth screens, catalogue screens | Register → login → catalogue |
| D | Practice components, analytics components | Practice flow, analytics flow | Full practice loop with results |

## 10. Communication and Sync

- **Daily standup (async):** Each agent posts: done, next, blockers.
- **Weekly sync (video):** Cross-agent review of integration points.
- **PR review SLA:** 4 hours during working hours.
- **Conflict resolution:** Engineering lead decides; documented in ADR if architectural.

## 11. Timeline (Dependencies Only, No Dates)

```
Week 1-2: Foundation PR → main
Week 3:   KAB-101 + KAB-102 (parallel, sequential merge)
Week 4:   KAB-103 (depends on KAB-102)
Week 5-6: KAB-104 (depends on KAB-101, KAB-103)
Week 7:   KAB-105 (depends on KAB-104)
Week 8:   Integration testing, E2E, accessibility audit, alpha readiness
```

> **Note:** Actual calendar dates require O3 (email provider), O4 (hosting), O5 (curator), and O6 (capacity) decisions. This plan is dependency-ordered.

## 12. Approval Gates

Before Phase 4 begins, the following must be **Approved**:

1. All 5 MVP specifications (SPEC-0001 through SPEC-0005).
2. ADR-0004 (session auth security design).
3. ADR-0006 (presigned upload security controls).
4. O3 (email provider selected and configured).
5. O5 (content curator named and workload accepted).
6. This multi-agent implementation plan.
7. Phase 3 technical package presented to repository owner.

## 13. References

- `docs/specifications/SPEC-0001-accounts-and-profile.md`
- `docs/specifications/SPEC-0002-cse-catalogue.md`
- `docs/specifications/SPEC-0003-question-bank-and-review.md`
- `docs/specifications/SPEC-0004-practice-and-results.md`
- `docs/specifications/SPEC-0005-progress-analytics-and-weak-topics.md`
- `docs/architecture/api-contracts.md`
- `docs/architecture/database-design.md`
- `docs/architecture/decisions/README.md` (ADR statuses)
- `docs/decisions/open-decisions.md` (O1–O10)
- `tickets/backlog/KAB-101-accounts-authentication.md` through `KAB-105-progress-analytics.md`