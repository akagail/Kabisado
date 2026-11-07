# Threat Model

**Status:** Initial — approved for Phase 4 implementation
**Owner:** Engineering / Security
**Last updated:** 2026-11-07
**Ticket:** KAB-005
**Companion:** [data-map.md](../operations/data-map.md), [security-guidelines.md](security-guidelines.md), [SPEC-0001..0005](../specifications/)

This is engineering guidance, not legal advice. It covers the MVP (increment 1)
and the beta deltas that are already designed. Revisit when a provider is
selected or a new data flow is added.

## 1. Scope and assets

| Asset | Why it matters | Where it lives |
| --- | --- | --- |
| Credentials (password hashes, reset tokens) | Account takeover | Django DB, never logged |
| Session cookies / CSRF tokens | Session hijack, CSRF | Browser, Django session store |
| Practice attempt history | Private study record (personal data) | Postgres |
| Question bank + explanations | Product integrity | Postgres |
| User email address | Identity, PII | Postgres (`citext`) |
| Uploaded materials (beta) | Potentially sensitive personal documents | Private object storage |
| AI prompts/completions (beta) | May contain user document text | Adapter → provider |
| Flags and audit events | Trust, moderation, abuse evidence | Postgres |

## 2. Actors and trust boundaries

Actors: anonymous visitor, learner, staff/curator, admin, platform operator,
external AI provider (beta), object storage provider (beta), email provider.

Boundaries:

| # | Boundary | Crosses |
| --- | --- | --- |
| TB1 | Browser → Next.js (TLS) | Untrusted client input |
| TB2 | Next.js `/api` proxy → Django | Session cookie, CSRF header |
| TB3 | Django → PostgreSQL | Trusted network, least-privilege DB user |
| TB4 | Django/Celery → object storage | Presigned URLs, private bucket (beta) |
| TB5 | Django/Celery → AI provider | User-derived text leaves our boundary (beta) |
| TB6 | Django → email provider | Reset links, PII |
| TB7 | Operator → Django admin | Privileged access |

The proxy is **not** a security boundary; all authorization is enforced in
Django services (ADR-0004).

## 3. STRIDE per boundary

### TB1 — Browser → Next.js

| Threat | Detail | Mitigation |
| --- | --- | --- |
| Spoofing | Forged session cookie | `HttpOnly`, `Secure`, `SameSite=Lax`; server-side session store |
| Tampering | Modified request bodies | Server-side validation via DRF serializers; never trust client IDs |
| Repudiation | User denies action | `core_audit_event` for auth/content actions |
| Information disclosure | XSS steals DOM data | React escaping, no `dangerouslySetInnerHTML`, CSP |
| DoS | Auth endpoint flooding | Rate limits on login/register/reset (429 + `Retry-After`) |
| Elevation | Client-side role checks bypassed | Roles enforced server-side only |

### TB2 — Proxy → Django

| Threat | Detail | Mitigation |
| --- | --- | --- |
| CSRF | Cookie sent cross-site | `CsrfViewMiddleware`; token from `GET /auth/csrf/`, `X-CSRFToken` on unsafe methods; 403 `csrf_error` |
| Session fixation | Attacker-set session | Session rotated on login; flush on logout/password change |
| Header spoofing | Client-supplied identity headers | Never trust `X-User-Id`-style headers; identity only from session |
| Cache leak | Shared cache serves user data | `private`/`no-store` on authenticated responses; dynamic rendering for user content |

### TB3 — Django → PostgreSQL

| Threat | Detail | Mitigation |
| --- | --- | --- |
| Injection | String-built SQL | ORM/parameterized queries only |
| IDOR via query | Missing owner filter | Every queryset filtered by `request.user`; object-level checks in services |
| Credential exposure | DB URL in logs | Secrets via env only; no connection strings logged |

### TB4 — Object storage (beta)

| Threat | Detail | Mitigation |
| --- | --- | --- |
| Unauthorized object read | Guessing keys | Non-guessable keys; private bucket; short-lived presigned GET; ownership re-checked before signing (ADR-0006) |
| Malicious upload | Malware, zip bombs, spoofed MIME | Validate extension + MIME + magic bytes + size; scan or hold for review before parsing |
| Orphan/replay | Reused presigned URL | Expiring URLs; completion checksum validation; idempotent completion; orphan cleanup job |
| Cross-user access | Completing another user's upload | Ownership verification on completion and download URL generation |

### TB5 — AI provider (beta)

| Threat | Detail | Mitigation |
| --- | --- | --- |
| Prompt injection | Document text instructs the model | Delimit untrusted text, instruction hierarchy, output validation, no tool execution from document content |
| Data leakage | Provider trains/retains content | O1 gate: DPA + no-training terms required before real user data is sent |
| Cost exhaustion | Quota evasion | Per-user quotas, cost accounting in `ai_generation`, rate limits |
| Wrong/hallucinated output | Silent inaccuracy | Citation-required retrieval gate, output schema validation, human review queue before shared publication |

### TB6 — Email provider

| Threat | Detail | Mitigation |
| --- | --- | --- |
| Account enumeration | Reset reveals existence | Always generic 202; same message regardless of existence |
| Token theft/replay | Reset link intercepted | Single-use hashed tokens with expiry; sessions invalidated on reset |
| Spoofing | Spoofed sender | Provider SPF/DKIM/DMARC; provider selection gate (O3) |

### TB7 — Admin

| Threat | Detail | Mitigation |
| --- | --- | --- |
| Privilege misuse | Staff reads practice answers | Admin scope limited to moderation; access audited |
| Account takeover | Weak admin credentials | Strong password policy; staff accounts restricted; consider MFA at hardening |

## 4. Abuse cases

| Abuse | Control |
| --- | --- |
| IDOR (read another user's session/results/profile) | Object-level ownership checks in every service; tests per SPEC |
| CSRF on state-changing endpoint | Enforced token + Referer check; tested |
| Credential stuffing | Rate limits + breached-password check on registration |
| Quota evasion across accounts (beta) | Per-user and per-IP limits; cost ledger |
| Upload abuse (size/type) | Pre-signing and post-upload validation |
| Content scraping of question bank | Auth-only access; rate limits; no bulk export endpoint |
| Self-review of content | Service-level rule: reviewer ≠ author |

## 5. Residual risks (accepted for MVP)

| Risk | Owner | Status | Note |
| --- | --- | --- | --- |
| No MFA at MVP | Engineering | Accepted | Revisit at hardening |
| No malware scanning until provider/storage chosen | Engineering | Accepted for local dev | Required before beta uploads (O2 gate) |
| Account deletion vs. backups | Engineering | Open | Depends on O4/O8; disclosed in privacy notice |
| No email verification at MVP | Product | Accepted | Deferred (AUTH-06) |
| Manual export fulfillment at alpha (≤7 days) | Product | Accepted | Documented in SPEC-0001 |

## 6. Security sign-off

Initial review complete 2026-11-07 for Phase 4 local development. Full sign-off
before public beta requires: real provider terms (O1/O2/O3), backup/restore
verification, and the restore drill (NFR-REL-03).
