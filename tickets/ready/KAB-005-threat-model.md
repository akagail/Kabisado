# KAB-005: Threat Model and Privacy Review

**Status:** READY
**Type:** security
**Priority:** P0
**Epic:** E0 Foundation
**Owner:** Engineering / Security
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (security analysis)
**Related ADRs:** ADR-0004, ADR-0005, ADR-0006
**GitHub issue:** https://github.com/akagail/Kabisado/issues/29

## 1. Description

Produce a concrete threat model and privacy data map for the proposed MVP,
covering authentication, uploads, AI processing, analytics, admin access, and
account deletion.

## 2. Business justification

The MVP handles credentials, personal documents, and study history. Security and
privacy controls must be designed before implementation, not retrofitted.

## 3. Scope

In:

- Assets, actors, trust boundaries, and data flows.
- STRIDE-style threats for each boundary.
- Abuse cases: IDOR, CSRF, credential stuffing, malicious uploads, prompt
  injection, quota evasion, cost exhaustion.
- Data inventory: what is collected, why, where stored, retention, subprocessors.
- Philippine Data Privacy Act considerations (R.A. 10173).
- Account deletion/export flow.
- AI provider data terms.
- Residual risks and accepted risks.

Out:

- Implementing controls.
- Legal advice.
- Penetration testing.
- Vendor selection (KAB-003).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-002 | architecture decision | pending |
| KAB-003 | provider terms | pending |

## 5. Acceptance criteria

- [x] `docs/engineering/threat-model.md` exists.
- [x] `docs/operations/data-map.md` exists.
- [x] Every trust boundary has threats and mitigations.
- [x] Every personal data field has purpose, retention, and access rules.
- [x] Account deletion and export are mapped end to end.
- [x] AI data flow documented; provider terms pending selection (O1).
- [x] Residual risks are listed with an owner and acceptance status.
- [ ] Security sign-off recorded before public beta.

## 6. Implementation checklist

- [x] Draw the data-flow diagram.
- [x] Enumerate assets and actors.
- [x] Run STRIDE per boundary.
- [x] Map data fields to purpose and retention.
- [x] Review auth/CSRF/session design.
- [x] Review upload and AI flows (designed paths; provider TBD).
- [x] Define deletion/export sequence.
- [x] Record accepted risks.

## 7. Testing checklist

- [ ] Authorization matrix drafted for every resource.
- [ ] CSRF and session tests planned.
- [ ] Upload validation tests planned.
- [ ] Prompt-injection fixtures planned.
- [ ] Deletion test planned across DB, storage, and derived content.

## 8. Validation evidence

```text
Initial threat model and data map completed 2026-11-07.
docs/engineering/threat-model.md — trust boundaries TB1–TB7, STRIDE per
boundary, abuse cases, residual risks.
docs/operations/data-map.md — field inventory, data flows, subprocessor
status, deletion and export sequences, R.A. 10173 considerations.
Remaining: authorization matrix and test fixtures are written alongside each
feature; full security sign-off requires real provider terms (O1/O2/O3) and
the backup/restore drill before public beta.
```

**Status note:** Initial review complete for Phase 4 local development. Ticket
stays open until the pre-public-beta sign-off criterion is met.

## 9. Risks and notes

- This document is engineering guidance, not legal advice.
- AI subprocessors may change; review on every provider change.
- Retention periods require owner approval.

## 10. References

- `docs/engineering/security-guidelines.md`
- `docs/architecture/system-architecture.md`
- `docs/architecture/ai-architecture.md`
