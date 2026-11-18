# KAB-002: Approve Architecture, ADRs, and MVP Scope

**Status:** REVIEW
**Type:** task
**Priority:** P0
**Epic:** E0 Foundation
**Owner:** Repository owner
**Created:** 2026-11-06
**Updated:** 2026-11-17
**Specification:** not required (decision ticket)
**Related ADRs:** ADR-0001 … ADR-0008
**GitHub issue:** https://github.com/akagail/Kabisado/issues/26
**Pull request:** https://github.com/akagail/Kabisado/pull/59

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

- [x] Each ADR has an explicit status: Approved, Proposed with changes, or
      Rejected with rationale.
- [x] Auth model is approved or replaced with a documented alternative.
- [x] MVP increments and out-of-scope list are approved or amended.
- [x] Launch exam and level are confirmed.
- [x] Required amendments are applied to the docs.
- [x] Decisions are recorded in the ticket and dated.

## 6. Implementation checklist

- [x] Review ADR index and each ADR. (2026-11-17)
- [x] Review product requirements and MVP scope. (2026-11-17)
- [x] Review architecture docs for contradictions. (2026-11-17; see §8.3)
- [x] Record decisions.
- [x] Update ADR statuses and docs.
- [x] Unblock KAB-101+ tickets.

## 7. Testing checklist

- [x] Documentation links resolve.
- [x] No contradictory statements remain between roadmap, MVP scope, and
      requirements.
- [x] Decision record is complete enough for a new agent to proceed.

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
| C6 | Roadmap Phase 0 still lists "remote CI has not run" as outstanding. | `roadmap.md` lines 24–25. | Remove the remote-CI claim (CI runs on every PR); keep the Docker note, which is still true. |
| C7 | Open-decisions header still describes Phase 2/3. | `open-decisions.md` line 3. | Update to the current phase and date. |

### 8.4 Decisions requested (owner sign-off)

Approved by the repository owner on 2026-11-17. The recommended options were
selected.

- [x] **ADR-0001** — approve as-is.
- [x] **ADR-0002** — approve stack intent; resolve C1/C5 via ADR-0009.
  - [x] C1 option A: keep Django 6.1 + write ADR-0009.
  - [ ] C1 option B: downgrade to Django 5.2 LTS.
- [x] **ADR-0003** — approve as-is.
- [x] **ADR-0004** — keep approved.
  - [x] C2 option A: implement 30-minute inactivity in a follow-up ticket (KAB-116).
  - [ ] C2 option B: supersede the condition.
- [x] **ADR-0005** — keep "Approved in Principle".
- [x] **ADR-0006** — keep approved; conditions become KAB-106 acceptance criteria.
- [x] **ADR-0008** — approve with duplication default.
  - [ ] or: leave Draft until the next CSC announcement.
- [x] **MVP scope** — approve as written.
- [x] **Product requirements** — approve; replace stale §5.
- [x] **Launch exam** — confirm CSE Professional, 14 March 2027 CSE-PPT.
- [x] **SPEC-0004 §8 deviation** — acknowledge the delivered flat practice shapes and pagination envelope (already shipped in KAB-114).

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
Date: 2026-11-17
Approver: Repository owner
ADR-0001: Approved
ADR-0002: Approved; version rows superseded by ADR-0009
ADR-0003: Approved
ADR-0004: Approved; 30-minute inactivity condition deferred to KAB-116
ADR-0005: Approved in Principle (unchanged)
ADR-0006: Approved; conditions carried into KAB-106
ADR-0008: Approved (duplication default)
ADR-0009: Approved (Django 6.1, TypeScript 5.9.x)
MVP scope: Approved
Product requirements: Approved
Launch exam: CSE Professional, 14 March 2027 CSE-PPT
SPEC-0004 §8 deviation: Acknowledged
```

## 9. Validation evidence

Approved by the repository owner on 2026-11-17. Amendments applied in the same
change:

- New ADR-0009 (version baseline) and ADR index update.
- ADR-0002 note (version rows superseded); ADR-0008 marked Approved.
- `backend-architecture.md` Django version aligned.
- `mvp-scope.md` and `product-requirements.md` statuses set to Approved; stale
  open questions replaced with resolutions.
- `roadmap.md` Phase 0 wording corrected (Docker still outstanding).
- `open-decisions.md` header refreshed; O7 marked resolved.
- `SPEC-0004` §8 deviation confirmed.
- KAB-116 created for the session-inactivity condition (#60).

Documentation links were checked with a local relative-link scan; no broken
targets were found in the changed files.

Remaining for the reviewer: the descriptive architecture documents
(`system-architecture.md`, `backend-architecture.md`, `frontend-architecture.md`,
`ai-architecture.md`, `file-upload-architecture.md`, `mvp-data-and-api.md`) still
carry "Proposed" statuses. They were outside this packet's decision list; decide
whether to mark them Approved or keep them as implementation guides.

## 10. Risks and notes

- Delaying this blocks all product work.
- Approving without reading the trade-offs shifts the risk to implementation.

## 11. References

- `docs/architecture/decisions/README.md`
- `docs/architecture/decisions/0009-version-baseline.md`
- `docs/product/mvp-scope.md`
- `docs/product/product-requirements.md`
- `docs/decisions/open-decisions.md`
- `tickets/ready/KAB-116-session-inactivity.md`
