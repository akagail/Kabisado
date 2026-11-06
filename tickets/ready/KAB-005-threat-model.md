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

- [ ] `docs/engineering/threat-model.md` exists.
- [ ] `docs/operations/data-map.md` exists.
- [ ] Every trust boundary has threats and mitigations.
- [ ] Every personal data field has purpose, retention, and access rules.
- [ ] Account deletion and export are mapped end to end.
- [ ] AI data flow and provider terms are documented.
- [ ] Residual risks are listed with an owner and acceptance status.
- [ ] Security sign-off recorded before public beta.

## 6. Implementation checklist

- [ ] Draw the data-flow diagram.
- [ ] Enumerate assets and actors.
- [ ] Run STRIDE per boundary.
- [ ] Map data fields to purpose and retention.
- [ ] Review auth/CSRF/session design.
- [ ] Review upload and AI flows.
- [ ] Define deletion/export sequence.
- [ ] Record accepted risks.

## 7. Testing checklist

- [ ] Authorization matrix drafted for every resource.
- [ ] CSRF and session tests planned.
- [ ] Upload validation tests planned.
- [ ] Prompt-injection fixtures planned.
- [ ] Deletion test planned across DB, storage, and derived content.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- This document is engineering guidance, not legal advice.
- AI subprocessors may change; review on every provider change.
- Retention periods require owner approval.

## 10. References

- `docs/engineering/security-guidelines.md`
- `docs/architecture/system-architecture.md`
- `docs/architecture/ai-architecture.md`
