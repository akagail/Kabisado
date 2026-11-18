# KAB-003: Select External Providers

**Status:** IN PROGRESS
**Type:** task
**Priority:** P0
**Epic:** E0 Foundation
**Owner:** Repository owner / Engineering
**Created:** 2026-11-06
**Updated:** 2026-11-18
**Specification:** not required (decision ticket)
**Related ADRs:** ADR-0002, ADR-0004, ADR-0005, ADR-0006
**GitHub issue:** https://github.com/akagail/Kabisado/issues/27
**Pull request:** https://github.com/akagail/Kabisado/pull/61

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
| KAB-002 | ticket | Completed 2026-11-17 (ADR-0002/0009 approved) |
| KAB-005 | privacy review | Pending — consumes this packet's DPA notes |

## 5. Acceptance criteria

- [x] A comparison table covers options, cost, region, and operational burden.
- [ ] Each selected provider has a recorded rationale.
- [ ] Data-processing/training terms are reviewed for AI and storage.
- [x] Estimated monthly cost at MVP scale is documented.
- [x] Secrets are stored outside the repository.
- [ ] An ADR or decision record captures the choices.
- [ ] Owner approves the selections and the budget ceiling.

Rationale is drafted per component (§8.8); it is not a selection until approved.
Public terms were read, but no DPA has been reviewed or accepted.

## 6. Implementation checklist

- [x] Gather requirements from architecture docs.
- [x] Shortlist two or three options per category.
- [x] Estimate cost and operational effort.
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

## 8. Decision packet

Prepared 2026-11-18. Prices were read from the providers' public pricing pages on
that date and are quoted in USD, excluding tax. They are anchors for a budget
ceiling, not quotations; re-check at signup.

### 8.1 Requirements this must satisfy

| Requirement | Source | Consequence for selection |
| --- | --- | --- |
| Modular monolith: one API container + one worker container | ADR-0001, `system-architecture.md` | No Kubernetes, no multi-service mesh |
| Managed PostgreSQL 17 with pgvector | ADR-0002/0009, `ai-architecture.md` §9 | Extension must be installable on the managed plan |
| Redis for Celery broker when async work lands | ADR-0002, `system-architecture.md` | Can be deferred until KAB-106 extraction |
| Private S3-compatible bucket + presigned URLs | ADR-0006 | Any S3 API works; no provider SDK in business logic |
| Transactional email with DPA before alpha users | AUTH-04, O3 | Console backend locally; real provider before first real user |
| LLM + embeddings under one DPA that forbids training on user content | ADR-0005, O1, NFR-SEC-08 | Free tiers that train on content are disqualified |
| Singapore-region latency for PH users | NFR-PERF, O4 | Prefer SG region over US |
| Exit path without code changes | `deployment-hosting-requirements.md` §3 | Standard Postgres, Redis URL, S3 API, SMTP/API email |

### 8.2 Backend host, PostgreSQL, Redis

| Option | Region | Cost anchor (monthly) | pgvector | Ops burden | Notes |
| --- | --- | --- | --- | --- | --- |
| **Render** (recommended) | Singapore | Hobby workspace $0; web Starter $7; Postgres Basic $6; Key Value Starter $10 | Yes (documented extension) | Low: git-push deploys, managed DB, cron jobs | One vendor for API, worker, DB, Redis; private networking |
| Railway | Singapore | Hobby $5 incl. $5 usage; ~$10/GB RAM-month, ~$20/vCPU-month | Yes | Low | Usage-based; cost is harder to cap than fixed plans |
| DigitalOcean App Platform + Managed DB | SGP1 | App from $5; Managed Postgres from $15; no managed Redis (uses Valkey) | Yes | Low–medium | DB is the priciest at the smallest useful size |
| AWS ECS Fargate + RDS + ElastiCache | ap-southeast-1 | Well above $100 at minimum viable size | Yes | High | Overkill for a monolith; revisit only if residency/compliance demands it |

**Recommendation:** Render, Singapore region — API and worker as two services,
managed Postgres, managed Key Value. It is the only shortlisted option that
publishes a fixed price per component, which makes the ceiling enforceable.

**Deferral:** Redis is not needed until Celery is wired (first async feature is
material extraction, KAB-106). Alpha can run on Postgres-backed Django sessions
with no broker, saving $10/month. Add Key Value when the worker lands.

### 8.3 Object storage

| Option | Cost anchor | Egress | Region | Notes |
| --- | --- | --- | --- | --- |
| **Cloudflare R2** (recommended) | 10 GB free; $0.015/GB-month after | $0 | Global; jurisdiction controls are EU/FedRAMP, no APAC residency guarantee | S3 API; presigned URLs work; cheapest at MVP volume |
| AWS S3 | ~$0.023/GB-month + requests | Billed | ap-southeast-1 | Mature IAM; egress cost and more setup |
| Backblaze B2 | $6/TB-month | Free up to 3× stored | US/EU | Cheapest at scale; no APAC region |
| Self-hosted MinIO | Instance cost only | Instance cost | Wherever hosted | No managed durability; ops burden; rejected for alpha |

**Recommendation:** Cloudflare R2 private bucket. MVP stores well under 10 GB, so
the storage line is $0 at alpha. The presigned-URL contract (ADR-0006) means
switching to S3 later is configuration only.

**Open point for KAB-005:** R2 offers no Philippine or Singapore data-residency
commitment. If the privacy review requires in-country storage, AWS S3
ap-southeast-1 becomes the choice and the storage cost rises to roughly
$1–2/month at MVP volume. This is a residency decision, not a cost decision.

### 8.4 Transactional email

| Option | Free tier | Paid anchor | Notes |
| --- | --- | --- | --- |
| **Resend** (recommended for alpha) | 3,000/month, 100/day | Pro $20 for 50k | Simple API, good DX; 100/day cap is ample for password resets |
| Postmark | 100/month (testing only) | Basic $15 for 10k | Best-in-class deliverability; the safer choice once real users depend on reset mail |
| AWS SES | None meaningful | $0.10 per 1,000 | Cheapest at volume; needs warm-up and more setup |

**Recommendation:** Resend free tier through closed alpha (volume is under 100
emails/month), moving to Postmark Basic ($15) before public beta when reset-mail
deliverability becomes a support risk. Both sit behind Django's email backend, so
the switch is configuration.

### 8.5 AI and embedding provider

| Option | Price per MTok (input / output) | Training on paid content | Notes |
| --- | --- | --- | --- |
| **Google Gemini paid tier** (recommended) | Flash-Lite 3.5 $0.30 / $2.50; Flash 3.8 $0.75 / $3.75 | No on paid tier | LLM **and** embeddings under one DPA and one bill; paid prices rise January 2027 |
| Anthropic Claude | Haiku 5.5 $0.10 / $0.50; Sonnet 5.5 $2 / $10 | No (commercial terms) | Strong instruction-following and structured output; embeddings must come from a second vendor |
| OpenAI | gpt-6-luna $0.10 / $0.50; gpt-6.1-terra $1 / $5 | No (API terms) | Comparable; adds a third vendor if Gemini already chosen |

**Recommendation:** Gemini **paid** tier as the first provider — one vendor for
generation and embeddings, one DPA, one quota. The free tier is disqualified: its
terms allow content to be used to improve Google's products, which fails O1 and
NFR-SEC-08. Anthropic Haiku stays as the evaluation fallback through the adapter.

**Explicitly not chosen:** any provider's free tier for user documents, and
self-hosted open-weight models (GPU cost and ops burden exceed the beta budget).

**Cost is dominated by usage, not list price.** A typical summary or question set
is a few thousand tokens; 1,000 generations/month at Flash-Lite prices is well
under $5. The ceiling below caps it rather than predicting it.

### 8.6 Estimated monthly cost

| Line | Closed alpha | Public beta |
| --- | --- | --- |
| Render web service | $7 | $7 |
| Render worker | $7 (only once Celery lands) | $7 |
| Render Postgres | $6 | $6–20 |
| Render Key Value | $0 (deferred) | $10 |
| Cloudflare R2 | $0 | ~$1 |
| Email | $0 (Resend free) | $15–20 |
| AI + embeddings | ≤$20 cap | ≤$60 cap |
| **Total** | **~$20–40** | **~$106–125** |

Frontend stays on Vercel's free tier (ADR-0002); it is not part of this budget.

### 8.7 Data processing and residency

| Provider | DPA / terms status | Residency |
| --- | --- | --- |
| Render | Standard DPA available on paid workspace — **verify and accept before real user data** | Singapore region selectable |
| Cloudflare R2 | DPA available — **verify** | No APAC residency guarantee |
| Resend / Postmark | DPA available — **verify** | US processing |
| Google Gemini | Paid-tier terms exclude training on content; DPA available — **verify** | Global; no PH residency |

None of these DPAs has been accepted. Acceptance is an owner action at signup, and
KAB-005 reviews the resulting data flow. R.A. 10173 obligations and the
subprocessor list belong in `docs/operations/data-map.md`; the register's O1/O2/O4
entries are updated only after approval.

### 8.8 Recommended bundle (for approval)

| Component | Selection |
| --- | --- |
| Backend host + worker | Render, Singapore |
| PostgreSQL + pgvector | Render managed Postgres |
| Redis | Render Key Value — **deferred until Celery lands** |
| Object storage | Cloudflare R2 private bucket |
| Email | Resend free → Postmark Basic before public beta |
| AI + embeddings | Google Gemini paid tier; Anthropic Haiku as evaluation fallback |
| Frontend | Vercel free tier (already in ADR-0002) |

**Proposed budget ceiling:** $50/month during closed alpha, $150/month during
public beta, with a hard AI spend cap of $20 and $60 respectively. Any line that
exceeds its ceiling needs a new approval, not a silent overage.

**Approval needed:** the bundle above, the two ceilings, and acceptance of the
DPAs at signup. Reply with changes per line; nothing is selected until then.

## 9. Validation evidence

```text
2026-11-18  Pricing read from public pages: render.com/pricing,
            railway.com/pricing, digitalocean.com/pricing,
            developers.cloudflare.com/r2/pricing, postmarkapp.com/pricing,
            resend.com/pricing, aws.amazon.com/ses/pricing,
            ai.google.dev/gemini-api/docs/pricing, openai.com/api/pricing,
            platform.claude.com/docs/en/about-claude/pricing.
2026-11-18  Render pgvector support confirmed in Render's Postgres
            extensions documentation.
2026-11-18  No accounts created, no credentials stored, no code changed.
```

Not executed: DPA review (contract acceptance is an owner action), and any
connectivity test against the services (no accounts exist yet).

## 10. Risks and notes

- AI usage and egress are the two lines that can run away; both get hard caps.
- R2 has no APAC residency guarantee; KAB-005 may force AWS S3 ap-southeast-1.
- Render Key Value costs $10/month for a component that is idle until Celery
  lands; deferring it is deliberate.
- Gemini paid prices rise in January 2027; the ceiling, not the unit price, is
  what gets approved.
- Fixed-price plans (Render) were preferred over usage-based (Railway) because a
  ceiling is only enforceable when the unit prices are known.
- Switching any provider stays configuration-only: standard Postgres, Redis URL,
  S3 API, Django email backend, AI adapter (ADR-0005/0006).

## 11. References

- `docs/operations/deployment.md` §3
- `docs/operations/deployment-hosting-requirements.md` §2–§5
- `docs/decisions/open-decisions.md` O1, O2, O3, O4
- `docs/architecture/system-architecture.md` §12
- `docs/engineering/security-guidelines.md`
- `docs/architecture/decisions/0005-ai-provider-abstraction.md`
- `docs/architecture/decisions/0006-file-uploads.md`
