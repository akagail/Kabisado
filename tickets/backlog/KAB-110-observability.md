# KAB-110: Observability Baseline

**Status:** BACKLOG
**Type:** task
**Priority:** P1
**Epic:** E11 Operations
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (operations)
**Related ADRs:** none
**GitHub issue:** none

## 1. Description

Add structured logging, request/job correlation IDs, health checks, core metrics,
error tracking, and alert definitions.

## 2. Business justification

Without visibility, failures in uploads, AI jobs, and auth are discovered by
users. Launch readiness requires operating the system, not only testing it.

## 3. Scope

In:

- JSON logs with request/job IDs.
- Pseudonymous user IDs; no sensitive payloads.
- Liveness/readiness endpoints (already scaffolded; extend for Redis when used).
- Metrics: request latency, 5xx rate, queue depth, job failures, AI tokens/cost,
  upload failures.
- Error tracking integration (provider pending).
- Alert rules and thresholds.
- Dashboard or documented queries.
- Runbook for common failures.

Out:

- Full distributed tracing (add when needed).
- On-call rotation.
- SIEM.
- Log retention beyond policy.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-003 | monitoring provider | pending |
| KAB-112 | deployment target | pending |

## 5. Acceptance criteria

- [ ] Logs are structured and correlatable across API and worker.
- [ ] No secrets, tokens, prompts, or document text appear in logs.
- [ ] Health endpoints reflect database/cache readiness.
- [ ] Metrics are emitted for the listed signals.
- [ ] Alerts exist for 5xx, queue backlog, failed jobs, and AI spend.
- [ ] A runbook covers the top failure modes.
- [ ] A synthetic failure is visible in logs and alerts.

## 6. Implementation checklist

- [ ] Define the log schema.
- [ ] Add correlation middleware and job context.
- [ ] Add metrics instrumentation.
- [ ] Add error tracking.
- [ ] Define alerts.
- [ ] Write the runbook.
- [ ] Test with a forced failure.

## 7. Testing checklist

- [ ] Log redaction test.
- [ ] Health check test.
- [ ] Metric emission test.
- [ ] Alert delivery test.
- [ ] Runbook walkthrough.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Logging user content is a privacy incident; test redaction.
- Do not alert on every transient error; tune thresholds.
- Keep costs bounded; sample high-volume logs if needed.

## 10. References

- `docs/operations/deployment.md` §10
- `docs/engineering/security-guidelines.md` §10
