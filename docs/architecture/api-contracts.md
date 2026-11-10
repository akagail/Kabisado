# API Contracts

**Status:** Finalized — approved against SPEC-0001–0005 and database design
**Owner:** Backend / Frontend
**Last updated:** 2026-11-07
**Approved by:** Repository owner
**Approved on:** 2026-11-07

Source of truth for HTTP endpoints, request/response schemas, authentication,
permissions, errors, and pagination for the MVP (increment 1) and beta deltas.

---

## Approved

Cross-referenced against:
- **SPEC-0001–0005**: all endpoints, auth, permission roles, error envelopes match spec scope.
- **Database design**: `accounts_user`, `accounts_profile`, `catalog_*`, `questions_*`, `practice_*`, `analytics_*` tables all referenced; ownership patterns align.

### Known clarifications (resolve during implementation, not block Phase 4)

| Endpoint | Clarification | Resolution |
| --- | --- | --- |
| GET `/exam-versions/{id}/subjects/` | No request schema needed; response shape (subject list) matches SPEC-0002 §8. | Implemented as spec requires. |
| POST `/practice-sessions/` | Request params union: `topic` (UUID), `subject` (UUID nullable), `exam_version` (UUID nullable). SPEC-0004 §8 omits `subject` and `exam_version`; code accepts all three but `subject`/`exam_version` may be null when `topic` is given. | Implementation resolves param validation; API contract validates all three fields are accepted. |
| POST `/practice-sessions/{id}/submit/` | Response shape: `{result: {score_correct, score_total, items:[...]}}`. SPEC-0004 §8 gives the same shape. Error `409` exists only for idempotent return (existing result); no other 409 on submit. | Clear. Documented in original spec. |
| GET `/practice-sessions/{id}/results/` | Returns `{result}` wrapping score + items with per-item correctness, explanation, provenance. Consistent with database design (`practice_attempt_answer` + `practice_session_item.snapshot`). | Consistent. |

## 1. Conventions

- Base path: `/api/v1/`
- JSON only; `snake_case` field names; TypeScript types mirror the OpenAPI contract.
- Session cookie authentication via the same-origin proxy (ADR-0004).
- CSRF: `X-CSRFToken` header on unsafe methods; token from `GET /auth/csrf/`.
- Error envelope (stable):

```json
{
  "error": {
    "code": "validation_error|unauthorized|forbidden|not_found|rate_limited|csrf_error|session_expired|server_error",
    "message": "Human-readable message.",
    "fields": {"email": ["Enter a valid email address."]}
  }
}
```

- Timestamps: ISO 8601 UTC.
- IDs: UUID strings (lowercase hyphenated).
- List endpoints: paginated; default page size 20, maximum 100; `page` and
  `page_size` query params; response includes `count`, `next`, `previous`.

## 2. Auth endpoints (SPEC-0001)

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| POST | `/auth/register/` | Public | Create account + session |
| POST | `/auth/login/` | Public | Start session |
| POST | `/auth/logout/` | Session | Invalidate session |
| POST | `/auth/password-reset/` | Public | Request reset email (generic 202) |
| POST | `/auth/password-reset/confirm/` | Public | Confirm reset token + set new password |
| GET | `/auth/csrf/` | Public | Get CSRF token |

### POST `/auth/register/`

Request:

```json
{ "email": "learner@example.com", "password": "StrongPass123!" }
```

Response `201`:

```json
{
  "user": { "id": "…", "email": "learner@example.com" },
  "profile": { "id": "…", "display_name": "", "target_exam": null, "preference": {} }
}
```

Errors: `400` validation, `429` rate limited, `409` duplicate (generic message).

### POST `/auth/login/`

Request: `{ "email": "…", "password": "…" }` → `200` same shape as register.

Errors: `400`, `401` generic invalid credentials, `429`.

### POST `/auth/logout/`

Request: none. Response `204`. Invalidates server-side session.

### POST `/auth/password-reset/`

Request: `{ "email": "…" }` → `202` always (no enumeration).

### POST `/auth/password-reset/confirm/`

Request: `{ "token": "…", "password": "…" }` → `200` user/profile on success.

Errors: `400`, `401` invalid/expired/used token, `429`.

### GET `/auth/csrf/`

Response `200`: `{ "csrfToken": "…" }`

**KAB-101 note:** until KAB-102 introduces `catalog.Exam`, `profile.target_exam`
is returned as the slug string (`"professional"` / `"subprofessional"`) or
`null`, not the object shown in §2.1.

### GET / `PATCH / `DELETE `/me/`, export endpoints

| Method | Path | Purpose |
| --- | --- |
| GET | `/me/` | Current user + profile |
| PATCH | `/me/` | Update display name, target exam, preference |
| DELETE | `/me/` | Delete account (body `{ "password": "…" }`) |
| POST | `/me/export/` | Request export (`pending`) |
| GET | `/me/export/{id}/` | Export status |

### 2.1 Request/response examples

Register `201` example: see SPEC-0001 §8.

`/me/` `200`:

```json
{
  "user": { "id": "…", "email": "learner@example.com" },
  "profile": {
    "id": "…",
    "display_name": "Ada",
    "target_exam": { "id": "…", "slug": "cse-professional", "name": "CSE Professional" },
    "preference": { "mode": "untimed", "size": 20 }
  }
}
```

## 3. Catalogue endpoints (SPEC-0002)

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/exams/` | Session | Exam families/exams |
| GET | `/exam-versions/{id}/subjects/` | Session | Subjects for version |
| GET | `/subjects/{id}/topics/` | Session | Topics with accuracy/attempts |
| GET | `/topics/{id}/` | Session | Topic detail + weak-topic status |

Responses use snake_case arrays; topic rows include:

```json
{
  "id": "…",
  "slug": "numerical-ability",
  "name": "Numerical Ability",
  "display_order": 2,
  "accuracy": 75.0,
  "attempts": 6,
  "weak_topic": false
}
```

`weak_topic` computed by the documented rule: `attempts ≥ 3 AND accuracy < 70`.

**KAB-102 implementation notes:** `/exams/` also returns `current_version`
(`{id, slug, label, source_url, published_at, passing_rate}` or `null`) per exam
so the client can call `/exam-versions/{id}/subjects/` without guessing. Until
practice responses exist (KAB-104), `accuracy` is `null`, `attempts` is `0`, and
`weak_topic` is `false`.

## 4. Question bank endpoints (SPEC-0003)

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| POST | `/questions/` | Staff | Create draft |
| POST | `/questions/{id}/submit-for-review/` | Staff | Submit for review |
| POST | `/questions/{id}/review/` | Staff | Approve or reject |
| POST | `/questions/{id}/retire/` | Staff | Retire item |
| GET | `/topics/{id}/questions/` | Session | Published items for topic (paginated) |
| POST | `/questions/{id}/flags/` | Session | Flag item |
| GET | `/admin/flags/` | Staff | Flag queue |

### Flag request

```json
{ "reason": "incorrect_answer", "note": "Distractor rationale unclear." }
```

Response `201`: flag record.

Errors: `400`, `401`, `403`, `404`, `409` duplicate open flag.

## 5. Practice endpoints (SPEC-0004)

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| POST | `/practice-sessions/` | Session | Start session (`mode`, `topic`, `size`) |
| GET | `/practice-sessions/{id}/` | Session | Session state, items, saved answers, expires_at |
| PUT | `/practice-sessions/{id}/answers/{position}/` | Session | Save/change answer |
| POST | `/practice-sessions/{id}/submit/` | Session | Submit; idempotent |
| GET | `/practice-sessions/{id}/results/` | Session | Score, correctness, explanations, provenance |
| GET | `/practice-sessions/` | Session | Paginated history |

### POST `/practice-sessions/` request

```json
{
  "topic": "…uuid…",
  "mode": "timed",
  "size": 20
}
```

Response `201`: `{ "id": "…", "mode": "timed", "status": "in_progress", "expires_at": "…" }`

### GET `/practice-sessions/{id}/` response

```json
{
  "id": "…",
  "status": "in_progress",
  "mode": "timed",
  "expires_at": "2026-12-01T12:00:00Z",
  "items": [
    {
      "position": 1,
      "question": {
        "id": "…",
        "stem": "What is 2+2?",
        "options": [
          { "id": "…", "text": "4", "is_correct": true }
        ]
      },
      "saved_answer": { "selected_option_id": "…", "is_correct": null }
    }
  ]
}
```

### PUT answers request

```json
{ "selected_option_id": "…" }
```

Response `204`. After deadline: `409` with `error.code = "session_expired"`.

### POST `/practice-sessions/{id}/submit/` response

```json
{
  "result": {
    "score_correct": 12,
    "score_total": 20,
    "score_percent": 60.0,
    "items": [
      {
        "position": 1,
        "question": { "…snapshot…" },
        "selected_option_id": "…",
        "is_correct": true,
        "explanation": "…",
        "provenance": "…"
      }
    ]
  }
}
```

Score is an estimate, labelled as such. Computed once, stored.

## 6. Analytics endpoints (SPEC-0005)

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/analytics/summary/` | Session | Accuracy by subject |
| GET | `/analytics/topics/` | Session | Accuracy + weak-topic by topic |

Response examples:

```json
{
  "subjects": [
    { "subject": { "id": "…", "slug": "numerical-ability", "name": "Numerical Ability" }, "accuracy": 75.0, "attempts": 6 }
  ]
}
```

```json
{
  "topics": [
    { "topic": { "id": "…", "slug": "percentages", "name": "Percentages" }, "accuracy": 60.0, "attempts": 3, "weak_topic": true }
  ]
}
```

## 7. Health endpoints (shared)

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/health/live/` | Public | Liveness probe |
| GET | `/health/ready/` | Public | Readiness probe |

## 8. Error catalogue

| Code | HTTP | Meaning |
| --- | --- | --- |
| `validation_error` | 400 | Request field validation failed; `fields` lists offending fields. |
| `unauthorized` | 401 | Missing/invalid session; redirect to login with `next`. |
| `forbidden` | 403 | Authenticated but not permitted (staff-only, or not owner). |
| `not_found` | 404 | Resource not found; no enumeration for auth resources. |
| `rate_limited` | 429 | Rate limit exceeded; `Retry-After` header present. |
| `csrf_error` | 403 | CSRF token missing/expired; client refetches and retries once. |
| `session_expired` | 409 | Timed practice session deadline passed. |
| `server_error` | 500 | Internal error; generic message to client, details only in logs. |

## 9. OpenAPI

- OpenAPI 3 schema generated from Django REST Framework (drf-spectacular) at
  `/api/v1/openapi.json`.
- Frontend shares the schema (or mirrors it) as the source of truth; hand-maintained
  duplicate contracts are discouraged (see documentation standards).
- Every endpoint above is covered by an API test per the testing strategy.

## 10. Approval status

**Finalized 2026-11-07** — approved against the five MVP specifications and the
database design. Changes after this point require an amendment section or a new
version; the OpenAPI schema is the machine-readable contract.
