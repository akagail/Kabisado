# KAB-003: Select External Providers

**Status:** READY
**Type:** task
**Priority:** P0
**Epic:** E0 Foundation
**Owner:** Repository owner / Engineering
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (decision ticket)
**Related ADRs:** ADR-0002, ADR-0004, ADR-0005, ADR-0006
**GitHub issue:** none

## 1. Description

Select and record providers for backend hosting, PostgreSQL, Redis, object
storage, transactional email, and the first AI/embedding provider. No provider is
currently selected.

## 2. Business justification

Uploads, AI features, email verification, and production deployment are blocked
without these decisions. Choosing ad hoc creates lock-in and security gaps.

## 3. Scope

In:

- Backend container host and region.
- Managed PostgreSQL with pgvector and backups.
- Managed Redis.
- S3-compatible object storage.
- Transactional email.
- AI and embedding provider, including data-processing terms.
- Cost estimate per environment.
- Data residency and subprocessors.

Out:

- Signing contracts.
- Creating production accounts.
- Storing credentials in the repository.
- Activating deployment (KAB-112).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-002 | ticket | pending |
| KAB-005 | privacy review | pending |

## 5. Acceptance criteria

- [ ] A comparison table covers options, cost, region, and operational burden.
- [ ] Each selected provider has a recorded rationale.
- [ ] Data-processing/training terms are reviewed for AI and storage.
- [ ] Estimated monthly cost at MVP scale is documented.
- [ ] Secrets are stored outside the repository.
- [ ] An ADR or decision record captures the choices.
- [ ] Owner approves the selections and the budget ceiling.

## 6. Implementation checklist

- [ ] Gather requirements from architecture docs.
- [ ] Shortlist two or three options per category.
- [ ] Estimate cost and operational effort.
- [ ] Review security/privacy terms.
- [ ] Record the decision.
- [ ] Create non-production accounts only after approval.
- [ ] Document configuration in `docs/operations/environment-variables.md`.

## 7. Testing checklist

- [ ] A staging deployment can connect to each selected service.
- [ ] pgvector is available.
- [ ] Workers and scheduled jobs are supported.
- [ ] Signed upload/download works with the chosen bucket.
- [ ] Email delivery works to a test address.
- [ ] AI adapter contract passes against the selected provider in a manual run.

## 8. Validation evidence

```text
No providers selected yet.
```

## 9. Risks and notes

- Costs can grow with AI usage and egress; set caps.
- Regional latency to Philippine users matters.
- Avoid providers that train on user content without an opt-out.
- Prefer services with a standard exit path (S3 API, standard Postgres).

## 10. References

- `docs/operations/deployment.md` §3
- `docs/architecture/system-architecture.md` §12
- `docs/engineering/security-guidelines.md`
