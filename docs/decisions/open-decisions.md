# Open Decisions Register

**Status:** Active — Phase 2 decisions recorded, Phase 3 planning in progress
**Owner:** Product / Engineering
**Last updated:** 2026-11-07

This register tracks every unresolved decision from Phase 2 that affects
architecture, product scope, or implementation readiness. No decision here is
final until explicitly approved.

Classification legend:

- **Blocking** — implementation cannot start or complete without this decision.
- **Deferrable** — implementation can proceed with a reasonable default; decision
  can be made later without rework.
- **Requires ADR** — the decision changes system structure, data model, or
  external contracts; an Architecture Decision Record must be written and
  approved before implementation.

---

## O1 — AI provider and data-processing terms

**Status:** Unresolved
**Classification:** Blocking (for Beta / Increment 2)
**Affected:** KAB-107 (AI platform), KAB-108 (AI study aids), SPEC-0007/0008,
`ai-architecture.md`, `ai-capabilities.md` §10, NFR-SEC-08, NFR-COST-01..03

### Technical and product implications

- The entire AI beta (material summarization, question generation, explanations,
  flashcards) depends on a provider that contractually:
  1. Prohibits training on user content.
  2. Limits retention of prompts and completions.
  3. Allows the data-processing agreement required by R.A. 10173.
- Without this, no user document can be sent to an LLM; the beta cannot ship.
- Provider choice determines API shape, latency, cost model, available models,
  and whether a local/open-weight fallback is feasible.
- The AI adapter (AI-01, AI-02) is provider-independent, but the first concrete
  implementation and the evaluation suite (AI-12) need a real endpoint.

### Recommended approach

Shortlist 2–3 providers that meet the contractual requirements, obtain their
DPAs, run a small evaluation (cost, latency, Filipino/English quality,
structured-output reliability), and present a comparison for approval. Do not
implement the adapter against a provider before the DPA is signed.

### Alternatives considered

| Option | Pros | Cons |
| --- | --- | --- |
| Major cloud provider (OpenAI, Anthropic, Google) | Mature APIs, SLAs, DPAs available | Cost at scale; data leaves PH jurisdiction unless regional endpoints exist |
| Self-hosted open-weight model (Llama, Qwen, etc.) | Full data control, no per-token cost | GPU infra cost; model quality gap for Filipino; ops burden |
| Hybrid: cloud for drafts, self-hosted for sensitive | Balances cost and privacy | Two stacks to maintain; still needs DPA for cloud tier |

### Consequences of delay

Beta (Increments 2, tickets KAB-106–109) cannot start. MVP (Increment 1) is
unaffected.

### Required approval

**Yes.** Provider selection, DPA acceptance, and cost commitment require explicit
human approval before any integration work.

---

## O2 — Object storage provider

**Status:** Unresolved
**Classification:** Blocking (for Beta / Increment 2)
**Affected:** KAB-106 (material upload), SPEC-0006, `ai-architecture.md` §7,
NFR-SEC-03, NFR-SEC-05, NFR-COST-03

### Technical and product implications

- Presigned direct-to-storage uploads (ADR-0006) need an S3-compatible endpoint.
- Private storage, lifecycle rules for abandoned uploads, and signed download
  URLs are required.
- Provider choice affects SDK, IAM model, regional latency, and cost.
- Must be selected before SPEC-0006 is written so the API contract matches the
  provider's capabilities (e.g., multipart upload limits, encryption defaults).

### Recommended approach

Evaluate 2–3 S3-compatible providers (AWS S3, Cloudflare R2, Wasabi, Backblaze
B2, self-hosted MinIO) against: regional presence in PH/SG, cost for
<100 GB/month, IAM granularity for presigned URLs, lifecycle policy support,
and DPA availability. Choose one; write the adapter; implement the upload flow.

### Alternatives considered

| Option | Pros | Cons |
| --- | --- | --- |
| Cloudflare R2 | No egress fees, S3 API, PH edge | Newer service; DPA terms to verify |
| AWS S3 | Mature, regional (AP-SE-1), full IAM | Egress fees; cost at scale |
| Self-hosted MinIO | Full control, no vendor lock-in | Operational burden; no managed durability SLA |

### Consequences of delay

Material upload (KAB-106) and everything downstream (AI processing, flashcards)
cannot start. MVP unaffected.

### Required approval

**Yes.** Provider selection and cost commitment require approval.

---

## O3 — Transactional email provider

**Status:** Requirements defined; provider not selected
**Classification:** Blocking (for MVP / Increment 1)
**Affected:** KAB-101 (accounts), SPEC-0001, AUTH-04, NFR-SEC-03

### Technical and product implications

- Password reset (AUTH-04, MUST for MVP) cannot work without email delivery.
- The provider needs: API or SMTP, delivery reliability, bounce/complaint
  handling, and a DPA.
- Local development uses the console backend; production needs a real provider
  before the first alpha user registers.

### Requirements (provider-independent)

1. **API or SMTP** — a simple, documented interface for sending password reset
   links.
2. **DPA and privacy** — contractual prohibition on training on user content;
   retention limits for sent message metadata.
3. **PH/SG deliverability** — good deliverability to common Philippine ISPs
   (Globe, Smart, Gmail).
4. **Bounce/complaint handling** — webhooks or polling to detect delivery
   failures; no sender reputation damage.
5. **Rate limiting** — respects the app's rate-limit policy (auth endpoints
   must not trigger provider throttling).
6. **Cost** — per-email pricing that fits the alpha budget (expected < 100
   emails/month at MVP volume).
7. **Testing** — a local/test mode that does not send real email (console
   backend or a sandbox API).

### Recommended approach

Pick a transactional provider (Postmark, SendGrid, Mailgun, Resend, AWS SES) that
offers a DPA, good PH deliverability, and a simple API. Configure it behind the
existing Django email backend abstraction so the code does not change. Do this
early — it is a small, low-risk decision that unblocks AUTH-04.

### Alternatives considered

| Option | Pros | Cons |
| --- | --- | --- |
| Postmark | High deliverability, simple API, DPA | Cost per email |
| AWS SES | Very cheap, scales, DPA | Lower deliverability without warm-up; setup complexity |
| Resend | Developer-friendly, DPA | Newer; volume limits on free tier |

### Consequences of delay

MVP cannot accept real users; password reset fails. This is the smallest
blocking decision — decide it first.

### Required approval

**Clarified — approval required only for a real provider before alpha.**

Local development uses Django's console email backend (`EMAIL_BACKEND` =
`django.core.mail.backends.locmem.EmailBackend`), so AUTH-04 (password reset)
works locally without any external provider. A real transactional email
provider must be selected, configured behind the existing Django email backend
abstraction, and tested before enabling email-dependent functionality for
alpha users. This unblocks the MVP login/reset flow at closed alpha; no
provider selection is needed for MVP development or public beta preview.

The decision is effectively resolved (console backend + pre-alpha provider), but
the provider itself remains a Phase 4 implementation gate.

---

## O4 — Production backend host

**Status:** Unresolved
**Classification:** Blocking (for Launch Hardening / Increment 3)
**Affected:** KAB-112 (deployment pipeline), `deployment.md`, `ci-cd.md`,
NFR-REL-03, NFR-SEC-01, O8 (backup retention)

### Technical and product implications

- Determines: container orchestration (ECS, Fly.io, Railway, Render, Kubernetes,
  VM), managed Postgres/Redis availability, secrets management, TLS termination,
  scaling model, and cost.
- Hosting decision drives the deployment pipeline, backup strategy, incident
  runbook, and the launch-hardening exit criteria.
- Cannot finalize `deployment.md`, run the restore drill (NFR-REL-03), or
  configure production secrets until this is chosen.

### Recommended approach

Define the non-functional requirements first (budget, ops capacity, compliance,
PH data residency if required), then evaluate 2–3 platforms. Do not over-engineer
— the architecture is a modular monolith; a single container service with managed
Postgres and Redis is sufficient for launch.

### Alternatives considered

| Option | Pros | Cons |
| --- | --- | --- |
| Fly.io / Railway / Render | Simple, managed DB/Redis, global | Vendor lock-in; cost at scale |
| AWS ECS Fargate + RDS + ElastiCache | Full control, PH region, enterprise | Higher ops complexity; more moving parts |
| VM (DigitalOcean, Linode, Vultr) + Docker Compose | Cheap, simple, full control | Manual scaling; self-managed DB backups/upgrades |

### Consequences of delay

Launch hardening (KAB-112) and public availability cannot complete. Alpha and
beta can run on any staging environment.

### Required approval

**Yes.** Hosting commitment, cost, and operational model require approval.

---

## O5 — Named content curator and content-review responsibility

**Status:** Repository owner is accountable until a curator is appointed
**Classification:** Blocking (for MVP alpha gate)
**Affected:** KAB-004 (content plan), KAB-103 (question bank), KAB-108 (AI
review), SPEC-0003, `ai-capabilities.md` §17, D3

### Technical and product implications

- The 300-item content gate (D3) requires a human who:
  1. Authors or reviews every question before publication.
  2. Ensures explanations are accurate and cite the correct source.
  3. Applies the provenance rule (external citation or authoring record).
  4. Retires bad items and investigates flags.
- AI-generated items need the same reviewer (or a second one) before entering
  shared pools.
- Without a named person, the alpha gate is a checkbox with no owner.

### Recommended approach

The repository owner acts as the initial curator. Before alpha, either confirm
this is sustainable or appoint a part-time curator with a defined SLA (e.g., 20
items/week reviewed). Document the workflow in SPEC-0003: draft → review (not by
author) → publish → audit.

### Alternatives considered

| Option | Pros | Cons |
| --- | --- | --- |
| Repository owner curates | No hiring; immediate start | Bottleneck; conflict of interest (author = reviewer) |
| Hire/contract a curator | Dedicated capacity; separation of duties | Cost; onboarding time |
| Community review with staff oversight | Scales; engagement | Quality variance; moderation overhead; not for MVP |

### Consequences of delay

Alpha cannot start; the 300-item gate is not credible without a reviewer.

### Required approval

**Yes.** Naming the curator and accepting the workload (or budget for a contractor)
requires approval.

---

## O6 — Team capacity and target dates

**Status:** Unresolved
**Classification:** Deferrable (for planning only; does not block code)
**Affected:** All tickets, `roadmap.md`, sprint planning, hiring

### Technical and product implications

- No calendar dates are committed in the roadmap. Capacity determines whether
  phases run sequentially or with overlap, and whether beta can start before
  alpha exit criteria are fully met.
- Affects hiring, contractor budgets, and stakeholder expectations.

### Recommended approach

Keep the roadmap dependency-ordered without dates. When O1–O5 are resolved,
estimate the remaining tickets with the actual team, then propose a target
timeline for approval. Do not invent dates before capacity is known.

### Consequences of delay

None for code; only for external communication and resource planning.

### Required approval

**Yes, but later.** Timeline approval comes after provider and curator decisions.

---

## O7 — Exam-version reuse policy

**Status:** Unresolved
**Classification:** Requires ADR (before next CSC announcement is modelled)
**Affected:** `database-design.md` (ExamVersion → Subject → Topic),
`cse-exam-reference.md`, SPEC-0002, KAB-102, content seeding

### Technical and product implications

- The current design: `ExamVersion` has its own `Subject` and `Topic` rows.
  A new bulletin creates a new version and duplicates the topic tree.
- Alternative: topics are shared across versions with a many-to-many mapping
  (`ExamVersionTopic`) that stores version-specific metadata (display order,
  item count, weight).
- The decision affects:
  - Content seeding effort (duplicate vs map).
  - Historical analytics (a learner's progress on "Word analogy" in the 2027
    version vs a 2028 version).
  - Catalogue UI (show version selector or merge?).
  - Question linking (questions link to topics; if topics are shared, a
    question appears in all versions that include that topic).

### Recommended approach

**Default: duplicate per version.** The CSC can add, remove, or reword topics
between bulletins. Duplicating avoids silent content changes when a new version
is added. A cross-version mapping table can be added later for reporting
("this topic existed in versions X and Y").

### Alternatives considered

| Option | Pros | Cons |
| --- | --- | --- |
| Duplicate topics per version (current) | Simple; historical isolation; no silent changes | Seeding effort repeats; cross-version reporting needs extra work |
| Shared topics with version mappings | DRY; easy cross-version progress | A topic edit affects all versions; CSC changes are not always compatible |
| Hybrid: core topics shared, version-specific overlays | Balance | Complexity; still needs a clear rule for what is "core" |

### Consequences of delay

Content seeding for the 2027 version can proceed with duplication (current
schema). The ADR is needed before a second version is modelled.

### Required approval

**Yes.** This is an architectural data-model decision; write ADR-0008 and approve
before SPEC-0002 is finalized for multi-version support.

---

## O8 — Backup retention for deleted accounts

**Status:** Unresolved
**Classification:** Deferrable (depends on O4 hosting decision)
**Affected:** `deployment.md`, NFR-REL-03, KAB-112, AUTH-08, D12

### Technical and product implications

- Deleted accounts de-identify practice records but backups may retain
  identifiable data until the backup expires.
- The retention promise to users ("your data is deleted") must match the backup
  policy.
- Hosting provider (O4) determines backup tooling, retention knobs, and restore
  granularity.

### Recommended approach

Define the policy after O4: e.g., "backups retained 30 days; point-in-time
recovery excludes deleted accounts after 7 days." Document in the privacy notice
and `deployment.md`.

### Consequences of delay

None for MVP/alpha; required before public launch hardening.

### Required approval

**Yes, but with O4.** Policy approval follows the hosting decision.

---

## O9 — Filipino-language generation scope

**Status:** Decided for beta: English output only; Filipino source passages are
quoted, not paraphrased
**Classification:** Deferrable (can be expanded later)
**Affected:** `ai-capabilities.md` §17, SPEC-0007/0008, KAB-107/108

### Technical and product implications

- Current decision (D9): AI output in English; Filipino appears only in quoted
  source passages and in Verbal Ability topic content.
- Expanding to Filipino generation requires: a model that handles Filipino well,
  evaluation data in Filipino, and prompt tuning.
- Not blocking beta; can be a post-beta feature.

### Recommended approach

Keep the beta English-output scope. If user research shows Filipino explanations
are a strong adoption driver, add a Filipino generation track with its own
evaluation gate.

### Consequences of delay

None for beta launch; only affects learners who prefer Filipino explanations.

### Required approval

**Only if scope expands.** Current decision is approved.

---

## O10 — Kabisado's value proposition for learners not taking the March 14, 2027 examination

**Status:** Unresolved
**Classification:** Deferrable (product positioning; does not block implementation)
**Affected:** `product-overview.md`, `roadmap.md` Phase 4, marketing, future
exam support

### Technical and product implications

- The 2027 CSE-PPT is a single date. Learners preparing for later sittings, or
  for other exams (PRC, UPCAT, etc.), need a reason to use Kabisado now.
- Product architecture already supports multiple exams (ExamFamily → Exam →
  Version), but content and messaging are CSE-2027-centric.
- Affects: onboarding messaging, catalogue visibility, progress retention across
  exam cycles, and the roadmap for additional exam families.

### Recommended approach

Design for **continuous preparation**: the catalogue shows the current official
version; past versions remain accessible for reference; progress is tied to
topics, not a single exam date. When the next CSC announcement arrives, it
becomes a new `ExamVersion` and the product continues. Messaging: "study the
current official coverage; your progress carries forward."

### Alternatives considered

| Option | Pros | Cons |
| --- | --- | --- |
| Single-exam focus (2027 only) | Simple MVP message | Dead product after March 2027; wastes architecture |
| Continuous preparation (recommended) | Aligns with architecture; retains users | Requires clear communication that coverage may change |
| Multi-exam from launch | Broader appeal | Content ops multiply; dilutes CSE focus |

### Consequences of delay

None for MVP/alpha; affects retention after the 2027 exam and the Phase 4
roadmap.

### Required approval

**Only for messaging and roadmap priority.** Architecture already supports it.

---

## Summary: Decisions Requiring Your Approval Before Implementation

| Decision | Classification | Must be resolved before | Recommended next action |
| --- | --- | --- | --- |
| **O3 Transactional email** | Blocking (MVP) | KAB-101 / SPEC-0001 | Provider-independent config first; selection deferred to Phase 4 |
| **O5 Content curator** | Blocking (MVP alpha) | KAB-004 / KAB-103 / SPEC-0003 | Confirm owner-as-curator or appoint contractor |
| **O1 AI provider + DPA** | Blocking (Beta) | KAB-107 / SPEC-0007 | Shortlist, obtain DPAs, evaluate, present comparison |
| **O2 Object storage** | Blocking (Beta) | KAB-106 / SPEC-0006 | Evaluate S3-compatible options, pick one |
| **O7 Exam-version reuse** | Requires ADR | Second version modelling / SPEC-0002 v2 | Write ADR-0008 with duplication as default |
| **O4 Production host** | Blocking (Launch) | KAB-112 / `deployment.md` | Define NFRs, evaluate 2–3 platforms, pick one |

Free-first infrastructure tracking is documented in [deployment-hosting-requirements.md](../operations/deployment-hosting-requirements.md): four stages with upgrade triggers, provider replacement paths, and unresolved decisions table.

The remaining decisions (O6, O8, O9, O10) can be deferred without blocking code.
O9 is already decided for beta scope.

---

## Synchronization

This register is the source of truth for open decisions. When a decision is
approved:

1. Update the row's status and add the approval date.
2. Update the affected specification, ADR, or ticket.
3. If an ADR is created, add it to `docs/architecture/decisions/README.md`.
4. If a GitHub Issue exists for the affected ticket, update its description or
   add a comment with the decision link.

Do not create duplicate GitHub Issues for decisions already tracked here.