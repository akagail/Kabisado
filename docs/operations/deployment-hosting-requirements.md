# Deployment and Hosting Requirements

**Status:** Draft — requires Phase 3 approval
**Owner:** Engineering
**Last updated:** 2026-11-07

This document supplements [deployment.md](../deployment.md) and defines the
free-first, portable-by-design infrastructure progression, service upgrade
triggers, and migration paths for each component. Production host selection
(O4) remains open. Infrastructure decisions are staged, not committed.

## 1. Core Principle

Adopt **Free-First, Portable-by-Design Infrastructure**.

Initially use free tiers or low-cost services wherever practical, including mock
AI responses. Paid infrastructure may be introduced later when justified by
measured traffic, reliability, security, or operational needs. This is a budget
strategy, not permission to weaken security or production requirements.

This principle governs every component below. No production requirement is
weakened solely to accommodate a free tier.

## 2. InfraProgression Stages

### Stage 1 — MVP Development

| Component | Choice | Limits | Upgrade trigger |
| --- | --- | --- | --- |
| Django API | Local Docker Compose | SQLite fallback available; no network cost | First push to remote; uses hosted or cloud container later |
| Celery workers | Local Docker Compose | None immediate; signals parsed synchronously when no worker is running | First real async feature enables Celery (material extraction) |
| PostgreSQL | Local Docker + SQLite fallback | Local SQLite fallback for tests; docker compose postgres for dev | CI-driven, then local-only until first real deploy |
| Redis | Local Docker | Optional; Celery without broker is process-level | When async features land and worker isolation matters |
| Object storage | Local mock / MinIO | Dev only; no production | Phase 2 — private bucket behind presigned URLs |
| Email | Console backend (dev) or free sender | Console backend sends nothing; SMTP free tier with limits | Phase 2 — transactional email provider configured |
| AI | Fake adapter (dev only) | No real API calls; tests are deterministic | First real provider selected and adapter wired (O1) |
| Frontend | Local dev server | Vercel as free/low-cost deployment later | Push to any static hosting later |

**Stage 1 deliverable:** Every feature works locally. All external interactions
are mocked or interface-only. Credentials live only in local env vars. Portability
is preserved because Docker Compose defines all components in one stack.

### Stage 2 — Closed Alpha

| Component | Recommended provisional choice | Notes | Upgrade trigger |
| --- | --- | --- | --- |
| Django API | Managed container (Fly.io, Render, Railway) or DigitalOcean App Platform | Small workload; avoid AWS/GCP overhead initially | Measured p95 latency > 1 s or deployment uptime < 99% |
| Celery workers | Same managed container, same command | Worker lifecycle must be reliable at scale | Background task latency or retry storms require dedicated workers |
| PostgreSQL | Managed Postgres (Fly.io Plan, Railway DataStore, DigitalOcean droplets) | pgvector extension required later for AI embeddings | PITR required, or embedding retrieval latency exceeds acceptable |
| Redis | Managed Redis (all three options) | Session storage and Celery broker | Public availability and persistence required |
| Object storage | S3-compatible private bucket | Presigned URL pattern (ADR-0006) keeps architecture portable | Production-grade throughput or compliance-required residency |
| Email | Transactional provider with DPA | Sends at MVP volume (< 100 emails/month) | Volume growth or deliverability SLA becomes required |
| AI | First provider after O1 evaluation | Fake adapter not sufficient; provider contract required before wiring | Provider terms fail acceptance criteria; switch adapter |
| Error monitoring | OpenTelemetry + Grafana (free tier) or vendor's free allowance | No error budget before public launch | Business-critical alerts become required |

**Stage 2 deliverable:** Real data moves through real services. Portability is
preserved: the application talks to S3-compatible APIs, provides standard
PostgreSQL connections, and uses the AI adapter abstraction regardless of
provider. Each choice is documented with its limits.

### Stage 3 — Public Beta

| Component | Provisional upgrade path from Stage 2 | Upgrade triggers |
| --- | --- | --- |
| Django API / worker | Managed container still appropriate; consider ECS Fargate if horizontal scaling emerges | Scaling limit or multi-instance failover documented |
| PostgreSQL | Managed Postgres with PITR and backup restore drills mandated | (NFR-REL-03): restore drill failure; user deletion support in backups |
| Redis | Always-on managed; persistence required | (NFR-SEC-05): worker isolation no longer optional |
| Object storage | Private bucket; lifecycle rules mandatory; CORS restricted | Quota exceeded on free tier; upload patterns reveal abuse |
| Email | Provider with DPA; bounce handling verified; deliverability confirmed | Deliverability failure rate > 1%; reputation damage at scale |
| AI | Provider with contractual training prohibition and retention limits | Provider term violation or privacy review fails; provider term unfulfillable |
| Monitoring / alerting | Paid tier with alert routing and incident runbook | Critical alert without resolution time exceeds incident SLA |

**Stage 3 deliverable:** Production-grade reliability with documented recovery
procedures. Free-tier usage stops for everything that affects users. Everything
remaining is funded based on measured consumption.

### Stage 4 — Growth

Upgrade individual services according to measured traffic, storage, processing
requirements, reliability, and operational needs. Stages are not rigid
phases; a service moving from one stage to the next depends on its
characteristics, not calendar dates.

## 3. Provider Replacement Considerations

Each infrastructure component has a defined replacement path. Replacing a
provider does not require changing application code, unless the provider's
API shape breaks the abstraction.

### PostgreSQL

No app code changes. Connection string replaces `DATABASE_URL`. If the
target vendor differs from the region (e.g., PH → SG), verify pgvector
extension availability. For now, stage 1/2 both provision on the same
PostgreSQL version (Django LTS + Postgres 17).

Replacement path: Fly.io → Render → ECS Fargate, or DigitalOcean → Google Cloud
SQL, etc. Migrations remain portable because they are SQL scripts.

### Redis

No app code changes (Celery broker address). Connection string replaces
`REDIS_URL`. Ensure the new Redis supports authentication (`REDIS_PASSWORD`)
and private networking if applicable.

Replacement path: DigitalOcean Redis → Railway Redis → ElastiCache.

### Object Storage

Application code stays portable because the implementation follows ADR-0006:
presigned URLs against S3-compatible APIs. Changing storage means changing
the endpoint, credentials, and bucket configuration — no model changes.

Replacement path: Backblaze B2 → R2 → AWS S3 → any other S3-compatible
provider. Container image and settings change, application does not.

### Email Provider

Django email config is provider-independent. Configuration values replace
env vars; no code changes. Spam/bulk email handling is provider-specific and
is a product-management decision post-launch.

Replacement path: SES → Postmark → SendGrid, or Resend → any with a DPA.

### AI Provider

Provider switching is supported architecturally (ADR-0005) but requires an
evaluation: cost, quality against golden set, Philippines coverage, terms.
The adapter façade means zero model changes in business logic. Replace
provider by choosing a different adapter registration and re-running
evaluation before release.

Replacement path: first provider → alternative evaluated provider. Token
format compatibility must be validated during evaluation.

## 4. Upgrade Triggers

The following triggers should notify engineering of an upgrade path from
free or provisional to paid:

| Trigger | Notified by | Action |
| --- | --- | --- |
| Upload throughput exceeds free-tier quota | Storage monitoring | Provision paid tier; keep presigned URL pattern |
| Per-user generation quotas exhausted with expansion expected | Quota dashboards | Change provider per contract; enforce budget |
| Erroneous official exam item reproduced | Content review | Prohibit reproduction pattern in prompt policy |
| Acceptance criteria unmet in alpha | Retention/uptime checks | Upgrade infra or raise NFR |
| SSR response contains leak from shared cache | Security review (KAB-005) | Disable shared caching; fix rendering |

## 5. Unresolved Decisions Requiring Human Approval

| Decision | Current status | Required for | Approval needed |
| --- | --- | --- | --- |
| O1 AI provider + DPA | Pending; ADR-0005 conditions apply | Beta (KAB-107+108+) | Yes — provider selection, DPA, and budget commitment |
| O2 Object storage provider | Pending; defer per instruction | Beta (KAB-106+) | Yes — provider selection and cost commitment |
| O3 Transactional email provider | Requirements defined; provider not selected | Alpha (KAB-101 reset flow) | Selection remains post-Phase 3 until human approval |
| O4 Production backend host | Pending | Launch hardening (KAB-112+) | Yes — hosting commitment, cost, operational model |
| O7 Exam-version reuse | Draft | SPEC-0002 revision if second version is modelled | Before second version modelling |
| O8 Backup retention | Depends on O4 | Production (NFR-REL-03, AUTH-08) | After O4 |

## 6. Distinguish MVP Development Allowance from Public Launch

The staging sections above clarify where free-tier usage ends:

- **Development**: free / SQLite / console email / fake AI. No hard caps.
- **Closed alpha**: private object storage; transactional email; first AI provider.
  Free tiers are permitted but documented. Production security controls apply.
- **Public beta**: full paid infrastructure for reliability, backed by documented
  recovery. No free assumptions.
- **Growth**: upgrades track measured consumption.

Misuse of the definition: if a security control weakens for convenience, that
 violates the principle. Weaknesses trigger reversion to the prior-security
state, not free-tier substitution.

## 7. Important Restrictions

- Do not weaken authentication, authorization, privacy, encryption, or file
  validation to accommodate free tiers.
- Do not store real user data in services whose security, retention, or
  processing terms have not been evaluated.
- Do not assume free-tier services provide backups, PITR, persistent workers,
  private networking, or production-grade availability.
- Do not select or purchase a provider without human approval.
- Do not silently replace approved ADR decisions.
- Keep O1, O2, O3, and O4 provider decisions tracked as pending until
  explicitly approved.

## 8. Completion Criteria for Phase 3 Readiness

This document satisfies Phase 3 readiness when:

1. The four stages are defined with clear upgrade triggers for every
   infrastructure component.
2. Provider replacement paths are documented and validated by architectural
   abstractions (ADR-0005, ADR-0006) — not operational contingency.
3. Stage 2 choices are provisional and explicitly documented with free-tier
   limitations; free tiers are permitted at closed-alpha scope.
4. Unknown provider selections do not break application-layer abstraction.
5. O1–O4 remain in a tracking state pending explicit human approval.
6. A decision gate is defined for Phase 4 implementation: choose your
   Stage 2 provisioner, configure each component, and confirm upgrade triggers
   are documented before merging onto `main`.

A summary of changed files, tickets, and the gate is presented to the
reviewer for approval before Phase 4 begins.