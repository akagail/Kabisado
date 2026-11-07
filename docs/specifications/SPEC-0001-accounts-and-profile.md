# SPEC-0001: Accounts and Profile

**Status:** Draft
**Owner:** Backend / Frontend
**Ticket:** KAB-101
**Related ADRs:** ADR-0003, ADR-0004
**Approved by:** —
**Approved on:** —
**Last updated:** 2026-11-07

## 1. Problem

Users need a secure, privacy-respecting way to create an account, authenticate,
manage their profile, and delete their data. This is the foundation for all
user-owned features in the MVP.

## 2. Goals

- Register with email and password; log in and out.
- Reset a forgotten password via email.
- View and edit display name, target exam (Professional/Subprofessional), and
  study preference.
- Delete account and request data export.
- Session authentication via HttpOnly cookie through same-origin proxy.
- CSRF protection on all unsafe requests.
- Rate limits on auth endpoints.

## 3. Non-goals

- Social login / SSO (AUTH-07, COULD).
- Multi-factor authentication.
- Email verification at MVP (AUTH-06, SHOULD — deferred to hardening).
- Payments, subscriptions, or entitlements.
- Custom avatars or public profiles.

## 4. Users and permissions

| Role | Can do | Cannot do |
| --- | --- | --- |
| Anonymous | Register, log in, request password reset | Access any authenticated route |
| Learner | Manage own profile, change password, request deletion/export, view own data | Access other users' data, staff endpoints |
| Staff | Django admin access, suspend accounts | Publish content on behalf of users, view practice answers |
| Admin | Everything staff can do, plus manage staff | — |

## 5. User flows

### 5.1 Happy path — Register → Login → Profile

1. Anonymous user visits `/register`, submits email and password.
2. Server validates: email format, uniqueness (generic error), password strength,
   breached-password check.
3. User created, session cookie set (`HttpOnly`, `Secure`, `SameSite=Lax`),
   redirected to `/onboarding` to choose target exam.
4. User selects exam, lands on catalogue home.
5. Later visits `/login`, submits credentials, session restored.
6. Visits `/profile`, sees display name, target exam, preference; edits and saves.

### 5.2 Happy path — Password reset

1. User clicks "Forgot password" on login page, enters email.
2. Server responds with same generic message regardless of email existence.
3. If email exists, a single-use reset token is generated, emailed via provider,
   and stored hashed with expiry.
4. User clicks link, lands on `/reset-password/{token}`, enters new password
   (validated same as registration).
5. Token consumed, session created, existing sessions invalidated, redirected to
   catalogue.

### 5.3 Happy path — Account deletion

1. User visits `/profile/delete`, reads warning, re-enters password.
2. Server validates password, deletes profile and user-owned rows, anonymizes
   flags (user FK set to NULL, note cleared), logs audit event.
3. Session destroyed, redirected to home with confirmation.

### 5.4 Happy path — Data export

1. User visits `/profile/export`, clicks "Request export".
2. Export request recorded with `pending` status.
3. Fulfilled manually at alpha (within 7 days); user notified when ready.
4. User downloads JSON + CSV archive containing profile, attempts, results, flags.

### 5.5 Alternate and error paths

| Condition | Behaviour |
| --- | --- |
| Registration: email already registered | Generic "check your details" message; no enumeration |
| Registration: weak or breached password | Inline field errors with specific guidance |
| Login: invalid credentials | Generic error; rate-limited (5/min IP, 10/hour email) |
| Login: too many attempts | 429 with `Retry-After`; form state preserved |
| Reset: token expired or used | "Link expired or already used. Request a new one." |
| Reset: unknown email | Same generic success message; no email sent |
| Profile edit: target exam change | Catalogue reloads; history preserved |
| Deletion: wrong password | Generic error; rate-limited; no deletion |
| Export: already pending | "Export already requested. Check back later." |
| Session expired mid-request | 401 with `WWW-Authenticate`; client redirects to login with `next` |

## 6. Behaviour

- **Session:** Django `SessionMiddleware` + `AuthenticationMiddleware`. Cookie:
  `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SECURE=True` (prod),
  `SESSION_COOKIE_SAMESITE='Lax'`, `SESSION_COOKIE_AGE=1209600` (14 days).
- **CSRF:** `CsrfViewMiddleware` enabled. Client fetches token from
  `GET /api/v1/auth/csrf/` and sends `X-CSRFToken` header on `POST/PUT/PATCH/DELETE`.
- **Password hashing:** `PBKDF2PasswordHasher` (Django default) with minimum
  12 characters, `django-password-validators` for common passwords, and
  `django-breached-password` (or equivalent) against HaveIBeenPwned k-anonymity.
- **Rate limits:** `django-ratelimit` or custom middleware on `/auth/login/`,
  `/auth/password-reset/`, `/auth/password-reset/confirm/`, `/auth/register/`.
- **Logout:** `POST /api/v1/auth/logout/` flushes session server-side, clears
  cookie, returns 204.
- **Same-origin proxy:** Next.js rewrites `/api/v1/*` to Django backend,
  forwards `Cookie` and `X-CSRFToken` headers, returns `Set-Cookie` to browser.

## 7. Data requirements

| Field | Type | Required | Validation | Notes |
| --- | --- | --- | --- | --- |
| User.email | EmailField | Yes | Unique, normalized lower-case, RFC 5322 | Identifier |
| User.password | CharField | Yes | PBKDF2, min 12 chars, not breached | Never logged |
| User.is_active | Boolean | Yes | Default True | False = suspended |
| User.is_staff | Boolean | Yes | Default False | Admin access |
| User.created_at | DateTime | Auto | UTC | — |
| User.updated_at | DateTime | Auto | UTC | — |
| Profile.user | OneToOne | Yes | Cascade on user delete | — |
| Profile.display_name | CharField | Yes | 1–80 chars | Shown in UI |
| Profile.target_exam | ForeignKey | Yes | Exam (Professional/Subprofessional) | Scopes content |
| Profile.preference | JSONField | No | Schema: `mode` (untimed/timed), `size` | Defaults used for practice |
| ExportRequest.user | ForeignKey | Yes | — | Status: pending/ready/expired |
| ExportRequest.status | CharField | Yes | Choices | — |
| ExportRequest.requested_at | DateTime | Auto | — | — |
| ExportRequest.completed_at | DateTime | Nullable | — | — |
| AuditEvent.actor | ForeignKey | Yes | SET_NULL on user delete | — |
| AuditEvent.action | CharField | Yes | Choices: login, logout, register, reset, profile_update, delete, export | — |
| AuditEvent.object_type | CharField | Yes | — | — |
| AuditEvent.object_id | UUIDField | Nullable | — | — |
| AuditEvent.summary | TextField | Yes | Human-readable | — |
| AuditEvent.created_at | DateTime | Auto | UTC | — |

**Retention and deletion:**

- User deletion: `User` and `Profile` hard-deleted; `PracticeSession`,
  `SessionItem`, `AttemptAnswer` hard-deleted; `ContentFlag.user` set to NULL,
  `note` cleared; `ExportRequest` deleted; `AuditEvent.actor` set to NULL,
  `summary` retains action only.
- Export data: fulfilled exports available for 7 days, then file deleted;
  `ExportRequest` retained for audit.
- Backups: follow hosting provider policy (O8); point-in-time recovery excludes
  deleted accounts after 7 days.

## 8. API contract

| Method | Path | Auth | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| POST | `/api/v1/auth/register/` | No | `{email, password}` | `{user: {id, email}, profile: {...}}` | 400 validation, 409 email exists (generic), 429 |
| POST | `/api/v1/auth/login/` | No | `{email, password}` | `{user: {id, email}, profile: {...}}` | 400, 401 (generic), 429 |
| POST | `/api/v1/auth/logout/` | Session | — | 204 | 401 |
| POST | `/api/v1/auth/password-reset/` | No | `{email}` | 202 (always) | 400, 429 |
| POST | `/api/v1/auth/password-reset/confirm/` | No | `{token, password}` | 200 `{user, profile}` | 400, 401 token invalid/used/expired, 429 |
| GET | `/api/v1/auth/csrf/` | No | — | `{csrfToken}` | — |
| GET | `/api/v1/me/` | Session | — | `{user: {id, email}, profile: {...}}` | 401 |
| PATCH | `/api/v1/me/` | Session | `{display_name?, target_exam?, preference?}` | `{profile}` | 400, 401, 403 |
| DELETE | `/api/v1/me/` | Session | `{password}` | 204 | 400, 401, 403 |
| POST | `/api/v1/me/export/` | Session | — | `{export_id, status: pending}` | 401, 409 pending exists |
| GET | `/api/v1/me/export/{id}/` | Session | — | `{status, download_url?}` | 401, 404 |

**Error envelope (all endpoints):**

```json
{
  "error": {
    "code": "validation_error|unauthorized|forbidden|not_found|rate_limited|server_error",
    "message": "Human-readable message",
    "fields": {"field": ["message"]}
  }
}
```

## 9. UI requirements

**Screens and states:**

- `/register` — form with email, password, confirm; loading, inline field errors,
  submit disabled while loading; success → `/onboarding`.
- `/login` — email, password, "Forgot password?" link; loading, generic error,
  redirect `next` param.
- `/onboarding` — radio: Professional / Subprofessional; continue → catalogue.
- `/reset-password` — email form; same generic success.
- `/reset-password/{token}` — new password, confirm; loading, token errors.
- `/profile` — display name, target exam (radio), preference (mode, size); save
  toast; delete account button (modal confirmation with password re-entry).
- `/profile/export` — request button (disabled if pending), status text,
  download link when ready.

**Accessibility:** Labels for all inputs, visible focus, ARIA live regions for
toasts/errors, keyboard operable, colour not sole indicator.

**Mobile:** 360px viewport, touch targets ≥44px, no horizontal scroll.

## 10. Edge cases

| Case | Expected behaviour |
| --- | --- |
| Register while already logged in | Redirect to catalogue with info toast |
| Login with inactive account | Generic error; no enumeration |
| Reset token used in another tab | Second use shows "already used" |
| Profile edit concurrent in two tabs | Last write wins; stale tab shows refresh prompt |
| Export requested, user deleted before fulfil | Export request cancelled; no file generated |
| CSRF token missing/expired | 403 with `csrf_error` code; client refetches token and retries once |
| Password reset email fails to send | Logged server-side; user sees generic success; retry on next request |
| Multiple rapid logout calls | All return 204; session already destroyed |

## 11. Error states

| Condition | User-facing message | HTTP/status |
| --- | --- | --- |
| Validation error | "Please correct the highlighted fields." | 400 |
| Invalid credentials | "Invalid email or password." | 401 |
| Account inactive | "This account is inactive." | 401 |
| Rate limited | "Too many attempts. Please wait X seconds." | 429 + `Retry-After` |
| CSRF failure | "Session expired. Please try again." | 403 |
| Unauthorized | "Please sign in to continue." | 401 |
| Forbidden | "You don't have permission to do that." | 403 |
| Not found | "Not found." | 404 |
| Server error | "Something went wrong. Please try again." | 500 |

## 12. Analytics and observability

**Events (no PII):**

- `auth_register_success` — `{method: email}`
- `auth_login_success` — `{method: email}`
- `auth_logout`
- `auth_password_reset_requested`
- `auth_password_reset_completed`
- `profile_updated` — `{fields: [...]}` 
- `account_deleted`
- `export_requested`
- `export_completed`

**Metrics:** registration conversion, login success rate, reset completion rate,
export fulfilment time (alpha: manual, target ≤7 days).

**Alerts:** auth 5xx rate > 1%, rate-limit saturation, email delivery failures.

## 13. Security and privacy

- **Authorization:** Every authenticated endpoint checks `request.user.is_authenticated`
  and ownership (`request.user == object.user` or `request.user.is_staff`).
- **CSRF:** Enforced on all unsafe methods; token fetched from dedicated endpoint.
- **Rate limits:** IP-based for anonymous, user-based for authenticated.
- **Secrets:** `SECRET_KEY`, email credentials, database URL in env vars only.
- **Logs:** No passwords, tokens, reset links, or full emails in logs.
- **Session:** Rotated on login; invalidated on logout, password change, deletion.
- **R.A. 10173:** Data export and deletion on request; privacy notice linked
  on registration and profile.

## 14. Acceptance criteria

- [ ] User can register with email and strong password; duplicate email rejected
      with generic message.
- [ ] User can log in and out; session cookie is HttpOnly, Secure, SameSite=Lax.
- [ ] User can reset password via email; token is single-use, expires, invalidates
      existing sessions.
- [ ] User can view and edit display name, target exam, and preference.
- [ ] User can delete account with password confirmation; data deleted or
      anonymized per retention rules.
- [ ] User can request export; receives JSON+CSV within 7 days (alpha manual).
- [ ] CSRF enforced on all unsafe requests; token fetch works.
- [ ] Rate limits return 429 with `Retry-After`; no enumeration on login/reset.
- [ ] All endpoints covered by API tests: success, validation, 401, 403, 404,
      429, CSRF.
- [ ] Frontend forms show loading, empty, error, unauthorized states.
- [ ] Accessibility: labels, focus, keyboard, ARIA live for toasts.
- [ ] OpenAPI schema generated and matches implementation.

## 15. Out of scope

- Social login, SSO, MFA.
- Email verification (hardening).
- Avatar upload, public profiles.
- Payments, subscriptions, entitlements.
- Automatic export fulfilment (alpha manual).
- Backup retention policy (depends on hosting, O8).

## 16. Dependencies and risks

| Item | Type | Status |
| --- | --- | --- |
| ADR-0004 (session auth) | Architecture | **Proposed — needs security design review** |
| Transactional email provider (O3) | External | Requirements defined; provider not selected |
| ADR-0002 (stack) | Architecture | Approved |
| SPEC-0002 (catalogue) | Spec | Draft (for target_exam FK) |

**Risks:**

- Email delivery failure blocks password reset; console backend only for local.
- CSRF proxy misconfiguration breaks auth; test thoroughly in staging.
- Deletion cascade must cover future AI/materials tables; use `on_delete` signals.

## 17. Rollout

- Feature flag: none (core MVP).
- Migration: `accounts` app models + `Profile`, `ExportRequest`, `AuditEvent`.
- Backfill: none.
- Rollback: revert migration; session cookie name unchanged.

## 18. Open questions

1. Exact password validator config (min length, breached list source)?
2. Session age: 14 days or shorter for alpha?
3. Export format: JSON + CSV confirmed; any other formats needed?
4. Should staff be able to trigger export on behalf of user (support)?