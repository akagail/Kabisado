# KAB-002: Approve Architecture, ADRs, and MVP Scope

**Status:** IN PROGRESS
**Type:** task
**Priority:** P0
**Epic:** E0 Foundation
**Owner:** Repository owner
**Created:** 2026-11-06
**Updated:** 2026-11-17
**Specification:** not required (decision ticket)
**Related ADRs:** ADR-0001 … ADR-0008
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

- [x] Review ADR index and each ADR. (2026-11-17)
- [x] Review product requirements and MVP scope. (2026-11-17)
- [x] Review architecture docs for contradictions. (2026-11-17; see §8.3)
- [ ] Record decisions.
- [ ] Update ADR statuses and docs.
- [ ] Unblock KAB-101+ tickets.

## 7. Testing checklist

- [ ] Documentation links resolve.
- [ ] No contradictory statements remain between roadmap, MVP scope, and
      requirements.
- [ ] Decision record is complete enough for a new agent to proceed.

## 8. Decision packet (prepared 2026-11-17)

Nothing in this packet is approved. Review the findings, mark a choice in
§8.4, and the amendments in §8.5 will be applied and dated.

### 8.1 Architecture decision records

| ADR | Current status | Finding | Recommended disposition |
| --- | --- | --- | --- |
| 0001 modular monolith | Approved | Matches the repo: one Django project, one Next.js app, modules under `backend/apps/`. | Approve as-is. |
| 0002 technology stack | Approved | Django row says 5.2 LTS and rejects 6.x feature releases; `backend/requirements.txt` pins `Django>=6.1.3,<6.2`. TypeScript row says "5.x/7.x as installed"; repo pins `^5.9.3`. See C1 and C5. | Keep the stack; supersede the version rows with ADR-0009. |
| 0003 REST/DRF | Approved | Matches `/api/v1/`, DRF, `drf-spectacular`, explicit pagination, and the error envelope in code. | Approve as-is. |
| 0004 session auth + proxy | Approved — with conditions | The 30-minute sliding inactivity condition is **not implemented**: settings use a 14-day cookie and no activity refresh. CSRF JSON endpoint and HttpOnly cookie match. See C2. | Keep approved; fix the condition in a follow-up ticket before alpha (recommended) or supersede the condition. |
| 0005 AI adapter + RAG | Approved in Principle | Conditions cannot be verified until a provider exists (KAB-003/KAB-107). No vendor SDK is imported outside `adapters/` today. | Keep "Approved in Principle"; do not mark Approved until KAB-107 meets the conditions. |
| 0006 presigned uploads | Approved — with conditions | No upload code yet (increment 2). Conditions are testable acceptance criteria for KAB-106. | Keep approved; carry the conditions into KAB-106. |
| 0007 attempt snapshot | Approved | Implemented in practice session items (KAB-104). | No action. |
| 0008 exam-version reuse | Draft | O7 is unresolved; the current schema already duplicates topics per version, which is the recommended default. Needed before a *second* exam version, not before the 2027 launch. | Recommend approve with duplication as the default; alternatively leave Draft and revisit at the next CSC announcement. |

### 8.2 Product documents

| Document | Current status | Finding | Recommended disposition |
| --- | --- | --- | --- |
| `mvp-scope.md` | Proposed — requires approval | F1–F11, increments, exclusions, and §10 decisions match the delivered KAB-101–105 work. The status was never advanced. | Approve as written; set status to Approved with date. |
| `product-requirements.md` | Draft — requires approval | Requirement IDs and priorities match MVP scope. §5 open questions 1–8 are stale; each is answered by MVP scope §10, `open-decisions.md`, or ADR-0004. | Approve; replace §5 with resolved pointers. |
| `roadmap.md` | Approved (delegated 2026-11-06) | Phase 0 says "architecture and MVP approved" (not yet true) and still lists Docker/remote CI as outstanding (both done). See C3, C6. | Correct Phase 0 wording and outstanding note after approval. |
| `open-decisions.md` | Active | Header says "Phase 2 decisions recorded, Phase 3 planning in progress"; O3/O5 are resolved, O1/O2/O4 are Category C gates, O7 needs ADR-0008. See C7. | Refresh header/status dates after approval. |
| `cse-exam-reference.md` | Reference — verified | Launch target is confirmed: **CSE Professional, 14 March 2027 CSE-PPT, Announcement No. 06 s. 2026**. Subprofessional is catalogue-only. | Confirm as the launch exam; no change. |

### 8.3 Contradictions to resolve

| # | Contradiction | Evidence | Recommended fix |
| --- | --- | --- | --- |
| C1 | ADR-0002 requires an LTS Django and rejects 6.x feature releases, but the backend pins Django 6.1. | `0002-technology-stack.md` lines 23, 38, 46; `backend/requirements.txt` line 1; `backend-architecture.md` line 10. | **Recommended:** keep Django 6.1 (tested, supported through the March 2027 launch) and write **ADR-0009** superseding the version rows. The ADR policy allows a feature release *with* an ADR. Alternative: downgrade to 5.2 LTS and retest. |
| C2 | ADR-0004's approved condition promises 30-minute sliding inactivity; settings have a 14-day cookie with `SESSION_SAVE_EVERY_REQUEST = False` and no inactivity middleware. | `0004-authentication.md` lines 55–59, 132–133; `backend/config/settings.py` lines 123–126. | **Recommended:** new ticket (e.g. KAB-116) to implement the inactivity refresh + test before alpha. Alternative: write an ADR superseding the condition. |
| C3 | MVP scope is still "Proposed", while the roadmap says architecture and MVP are approved. | `mvp-scope.md` line 3; `roadmap.md` lines 21–22. | Set MVP scope to Approved after sign-off; correct roadmap Phase 0. |
| C4 | Product requirements are "Draft" and §5 asks questions the MVP scope and open-decisions register already answer. | `product-requirements.md` lines 3, 205–214. | Approve; replace §5 with a resolved-questions table pointing at the answers. |
| C5 | ADR-0002 describes TypeScript as "5.x/7.x as installed"; the repo pins `^5.9.3` with a Dependabot major-version ignore. | `0002-technology-stack.md` line 21; `frontend/package.json` line 39; `.github/dependabot.yml`. | Fold into ADR-0009: "TypeScript 5.9.x pinned; majors gated by `typescript-eslint` support (KAB-113)." |
| C6 | Roadmap Phase 0 lists "Docker not installed" and "remote CI has not run" as outstanding. | `roadmap.md` lines 24–25. | Remove the stale note; both are done. |
| C7 | Open-decisions header still describes Phase 2/3. | `open-decisions.md` line 3. | Update to the current phase and date. |

### 8.4 Decisions requested (owner sign-off)

Check one option per line, or reply with the letters.

- [ ] **ADR-0001** — approve as-is.
- [ ] **ADR-0002** — approve stack intent; resolve C1/C5 via ADR-0009.
  - [ ] C1 option A: keep Django 6.1 + write ADR-0009 (recommended).
  - [ ] C1 option B: downgrade to Django 5.2 LTS.
- [ ] **ADR-0003** — approve as-is.
- [ ] **ADR-0004** — keep approved.
  - [ ] C2 option A: implement 30-minute inactivity in a follow-up ticket (recommended).
  - [ ] C2 option B: supersede the condition.
- [ ] **ADR-0005** — keep "Approved in Principle".
- [ ] **ADR-0006** — keep approved; conditions become KAB-106 acceptance criteria.
- [ ] **ADR-0008** — approve with duplication default (recommended).
  - [ ] or: leave Draft until the next CSC announcement.
- [ ] **MVP scope** — approve as written.
- [ ] **Product requirements** — approve; replace stale §5.
- [ ] **Launch exam** — confirm CSE Professional, 14 March 2027 CSE-PPT.
- [ ] **SPEC-0004 §8 deviation** — acknowledge the delivered flat practice shapes and pagination envelope (already shipped in KAB-114).

### 8.5 Amendments to apply after approval

1. `docs/architecture/decisions/0009-version-baseline.md` — new ADR superseding
   ADR-0002's version rows (Django 6.1, TypeScript 5.9.x, Node/Python pins);
   add to the ADR index.
2. `docs/architecture/decisions/README.md` — update ADR-0002 to "Superseded by
   ADR-0009" (or leave Approved and note the superseded rows, per ADR-0009).
3. `docs/product/mvp-scope.md` — status → Approved, last-updated date.
4. `docs/product/product-requirements.md` — status → Approved; §5 replaced.
5. `docs/product/roadmap.md` — Phase 0 wording and outstanding note corrected.
6. `docs/decisions/open-decisions.md` — header/date refreshed; O7 marked
   resolved if ADR-0008 is approved.
7. `docs/architecture/backend-architecture.md` — Django version aligned with
   ADR-0009.
8. Follow-up ticket for C2 (session inactivity) if option A is chosen.

### 8.6 Decision record

```text
Date: pending
Approver: pending
ADR-0001: pending
ADR-0002: pending (C1: pending, C5: pending)
ADR-0003: pending
ADR-0004: pending (C2: pending)
ADR-0005: pending
ADR-0006: pending
ADR-0008: pending
MVP scope: pending
Product requirements: pending
Launch exam: pending
SPEC-0004 §8 deviation: pending
```

## 9. Validation evidence

Prepared by an agent on 2026-11-17. No approval has been recorded. Checks were
limited to reading the documents and comparing them with the code; no
documentation links were re-verified yet.

## 10. Risks and notes

- Delaying this blocks all product work.
- Approving without reading the trade-offs shifts the risk to implementation.

## 11. References

- `docs/architecture/decisions/README.md`
- `docs/product/mvp-scope.md`
- `docs/product/product-requirements.md`
- `docs/decisions/open-decisions.md`
