# Data Map

**Status:** Initial — approved for Phase 4 implementation
**Owner:** Engineering / Security
**Last updated:** 2026-11-07
**Ticket:** KAB-005
**Companion:** [threat-model.md](../engineering/threat-model.md), [database-design.md](../architecture/database-design.md)

Personal data inventory for the MVP and designed beta deltas. Purpose,
retention, and access rules per field. R.A. 10173 (Philippine Data Privacy Act)
applies.

## 1. Data inventory

### Accounts

| Field | Classification | Purpose | Retention | Access |
| --- | --- | --- | --- | --- |
| `accounts_user.email` | PII (identifier) | Login, password reset, account notices | Account lifetime; purged on delete | Owner; staff for support (audited) |
| `accounts_user.password` (hash) | Secret | Authentication | Account lifetime | None (never displayed) |
| `accounts_user.display_name` | PII (low) | UI personalization | Account lifetime | Owner; staff for moderation |
| `accounts_user.email_verified_at` | Metadata | Verification state | Account lifetime | Owner; staff |
| `accounts_user.last_login_at` | Behavioral | Security/UX | Account lifetime | Owner; staff |
| `accounts_profile.target_exam_id` | Preference | Content scoping | Account lifetime | Owner |
| `accounts_profile.study_preference` | Preference | Default practice settings | Account lifetime | Owner |
| `accounts_profile.timezone` | Preference | Display | Account lifetime | Owner |

### Authentication material

| Item | Classification | Purpose | Retention | Access |
| --- | --- | --- | --- | --- |
| Session record | Secret | Active session | Until expiry/logout (14d max, 30m sliding) | Server only |
| CSRF token | Secret (low) | Request forgery protection | Session lifetime | Browser (body/header) |
| Password reset token | Secret | Reset flow | Single use, short expiry | Server only (hashed) |
| Password reset links | Secret | Reset flow | Not logged | Email recipient only |

### Learning data

| Field | Classification | Purpose | Retention | Access |
| --- | --- | --- | --- | --- |
| `practice_practice_session.*` | Personal (behavioral) | Practice history, scoring | Account lifetime; cascade on delete | Owner only |
| `practice_session_item.snapshot_*` | Personal (derived from content) | Immutable attempt record | Account lifetime | Owner only |
| `practice_attempt_answer.*` | Personal (behavioral) | Results, analytics | Account lifetime; cascade on delete | Owner only; no staff read |
| `analytics_topic_stat.*` | Personal (aggregated) | Weak-topic diagnosis | Account lifetime; cascade on delete | Owner only |
| `questions_content_flag.reporter_id` | PII (link only) | Abuse handling | Retained; set NULL on account delete | Staff (moderation) |

### Content and audit

| Field | Classification | Purpose | Retention | Access |
| --- | --- | --- | --- | --- |
| `questions_question.*` | Product content | Question bank | Retired, not deleted | Staff write; learners read published |
| `core_audit_event.*` | Security log (may contain actor id) | Accountability | 12 months; `actor_id` set NULL on delete | Staff; append-only |
| `core_export_request.*` | PII (link only) | Data-portability requests | Request retained; file deleted after 7 days | Owner; staff for fulfilment |

### Beta deltas (not active in MVP)

| Field | Classification | Purpose | Retention | Access |
| --- | --- | --- | --- | --- |
| `materials_material.*` | User document (potentially sensitive PII) | Study material source | Until user deletes or account deletion | Owner only; presigned URLs |
| `materials_material_chunk.text` | Derived user document | Retrieval for AI aids | With parent material | Owner only; AI pipeline |
| `materials_material_chunk.embedding` | Derived vector | Retrieval | With parent material | System only |
| `ai_generation.*` | Metadata (may include prompt hashes) | Cost, audit, provenance | 12 months; user link anonymized | Staff for cost/audit; no raw content in logs |
| `questions_flashcard.*` | Derived content | Study aids | With source/parent | Owner (private) until reviewed |

## 2. Data flows

```text
Browser ──(TLS)──> Next.js ──(same-origin proxy)──> Django ──> PostgreSQL
                                                    │
                                                    ├──> Email provider (reset links) [O3]
                                                    ├──> Object storage (presigned) [O2, beta]
                                                    └──> AI provider (beta) [O1]
```

- Practice data never leaves Django/Postgres in the MVP.
- Uploaded material leaves our boundary only via the AI provider, and only after
  O1 (DPA, no-training terms) is approved.
- Email addresses leave via the email provider only for transactional mail.

## 3. Subprocessors (status)

| Subprocessor | Data received | Status |
| --- | --- | --- |
| Email provider | Email address, reset link | **Not selected** (O3) |
| Object storage | Uploaded files | **Not selected** (O2) |
| AI provider | Document text, prompts | **Not selected** (O1) |
| Hosting | All application data at rest | **Not selected** (O4) |

No real user data is sent to a subprocessor whose terms have not been reviewed.

## 4. Account deletion sequence

1. User confirms with password.
2. Delete `accounts_user` + `accounts_profile`.
3. Cascade: practice sessions, session items, attempt answers, analytics rows,
   export requests, beta materials/chunks/flashcards owned by the user.
4. De-identify: `content_flag.reporter_id` → NULL (note cleared),
   `audit_event.actor_id` → NULL (action retained),
   `ai_generation.user_id` → NULL.
5. Object storage: delete owned objects (beta).
6. Backups: purged per provider retention (O8), disclosed in privacy notice.

## 5. Account export sequence

1. User requests export; one `pending` request at a time.
2. At alpha, fulfilled manually within 7 days (target).
3. Archive: profile, practice sessions, results, flags, interactions.
4. Download link is short-lived; file deleted after 7 days; request record retained.

## 6. Privacy considerations (R.A. 10173)

- Lawful basis: contract/consent at registration; privacy notice linked on
  registration and profile.
- Data minimization: only fields the product needs are collected.
- Access and correction: profile edit; export on request.
- Erasure: account deletion with cascading purge.
- Retention: documented per table; 12 months for audit/AI metadata, 30 days for
  backups.
- Breach response: maintainer notified privately; no public disclosure of
  vulnerabilities.
- Cross-border transfer: only after subprocessor terms reviewed (O1–O4).

## 7. Open items

| Item | Blocked by | Required before |
| --- | --- | --- |
| Subprocessor DPAs | O1, O2, O3, O4 | Sending real user data |
| Backup retention policy vs. deletion promise | O4/O8 | Public launch |
| AI provider training/retention terms | O1 | Beta AI features on real documents |
