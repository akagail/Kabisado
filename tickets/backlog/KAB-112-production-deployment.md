# KAB-112: Production Deployment Pipeline

**Status:** BACKLOG
**Type:** task
**Priority:** P1
**Epic:** E13 Release
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (operations)
**Related ADRs:** ADR-0002, ADR-0004
**GitHub issue:** none

## 1. Description

Implement staging and production deployment for the API, worker, and frontend,
with manual approval, migrations, smoke tests, and rollback.

## 2. Business justification

The product cannot launch without a repeatable, safe release process. This ticket
activates the deployment design once hosting is approved.

## 3. Scope

In:

- Container registry and immutable image tags.
- Staging environment and deployment.
- Production environment with manual approval.
- Frontend Vercel project and environment variables.
- Migration release step.
- Smoke tests.
- Rollback procedure.
- Release notes and tagging.

Out:

- Provider selection (KAB-003).
- Autoscaling beyond a basic policy.
- Multi-region.
- Blue/green (start with rolling + rollback).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-003 | provider selection | pending |
| KAB-110 | observability | pending |
| KAB-005 | privacy/security review | pending |

## 5. Acceptance criteria

- [ ] A merged commit produces an immutable API image.
- [ ] Staging deploys and passes smoke tests.
- [ ] Production requires explicit approval.
- [ ] Migrations run once per release and are logged.
- [ ] Health/readiness checks gate the rollout.
- [ ] Rollback to the previous image is documented and rehearsed.
- [ ] Secrets are stored in the platform, not in git.
- [ ] A release tag and notes are created.
- [ ] The launch checklist in `docs/operations/deployment.md` is complete.

## 6. Implementation checklist

- [ ] Configure the registry.
- [ ] Add build/push workflow.
- [ ] Configure staging and production environments.
- [ ] Add migration release step.
- [ ] Add smoke tests.
- [ ] Document rollback.
- [ ] Run a staging rehearsal.
- [ ] Obtain production approval.

## 7. Testing checklist

- [ ] Staging deploy from a clean commit.
- [ ] Migration failure drill.
- [ ] Rollback drill.
- [ ] Health check failure drill.
- [ ] Secret rotation check.
- [ ] Smoke journey: auth → practice → results.

## 8. Validation evidence

```text
Not started. Production deployment is intentionally inactive.
```

## 9. Risks and notes

- Do not activate production before hosting, credentials, privacy, and approval
  gates are complete.
- A failed migration can cause data loss; back up first.
- Keep the previous image deployable.

## 10. References

- `docs/operations/deployment.md`
- `docs/engineering/ci-cd.md` §9–11
