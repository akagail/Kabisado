# KAB-101: Accounts and Authentication

**Status:** REVIEW
**Type:** feature
**Priority:** P1
**Epic:** E1 Accounts
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-07
**Specification:** SPEC-0001 (approved 2026-11-07)
**Related ADRs:** ADR-0004
**GitHub issue:** https://github.com/akagail/Kabisado/issues/14
**Pull request:** https://github.com/akagail/Kabisado/pull/33

## 1. Description

Implement registration, login, logout, password reset, profile management, and
account deletion using Django session authentication through the same-origin
proxy.

## 2. Business justification

Every user-owned feature depends on identity, session handling, and an account
lifecycle. It is the first product increment.

## 3. Scope

In:

- Email/password registration and login.
- Logout and session rotation.
- Password reset by email.
- `GET /me/` and profile update (display name, target exam, timezone,
  study preference).
- Account deletion (immediate hard delete, cascade).
- Data export request and status.
- CSRF endpoint and client handling.
- Login/reset rate limits.
- Login and registration UI states.
- Django admin access for staff.

Out:

- Social login/SSO.
- MFA.
- Email verification.
- Payments and entitlements.
- Custom user avatars.
- Export file generation (manual at alpha).
- `catalog.Exam` model and `target_exam` FK (KAB-102).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| SPEC-0001 | approval | Approved 2026-11-07 |
| ADR-0004 | architecture | Approved 2026-11-07 |
| KAB-003 email provider | external | Not needed locally; console backend |

## 5. Acceptance criteria

- [x] A user can register, log in, log out, and reset a password.
- [x] Passwords use a modern hasher and validators (12-char minimum, common,
      numeric, similarity, optional HIBP).
- [x] Session cookie is `HttpOnly`, `Secure` outside DEBUG, `SameSite=Lax`.
- [x] CSRF is enforced on unsafe requests, including anonymous ones.
- [x] Login and reset do not reveal whether an email exists.
- [x] A user can view/update their profile.
- [x] A user can request deletion; owned data is deleted.
- [x] Cross-user profile/export access is denied.
- [x] Rate limits return 429 with `Retry-After`.
- [x] API tests cover success, validation, unauthenticated, unauthorized, and
      CSRF cases.

## 6. Implementation checklist

- [x] Write and approve the specification.
- [x] Write the technical design (ADR-0004).
- [x] Implement user/profile models and migrations.
- [x] Implement services and endpoints.
- [x] Implement the API client CSRF handling.
- [x] Build the auth screens and states.
- [x] Add admin and audit logging.
- [x] Add rate limiting.
- [x] Update docs and OpenAPI.

## 7. Testing checklist

- [x] Service tests for registration, reset, deletion.
- [x] API tests for all endpoints and error cases.
- [x] Frontend tests for forms and error states.
- [x] E2E: register → login → logout.
- [x] Security: IDOR, CSRF, enumeration, rate limit.
- [x] Accessibility: labels, focus, keyboard (labelled inputs, `aria-invalid`,
      `aria-describedby`, `role="alert"`/`status`).

## 8. Validation evidence

Backend (`cd backend`, `.venv` Python 3.13 / Django 5.2.19 / DRF 3.18.3):

```text
ruff format --check .          All checks passed
ruff check .                   All checks passed
manage.py check                System check identified no issues
makemigrations --check          No changes detected
pytest                         32 passed
spectacular --validate         no errors or warnings
```

Frontend (`cd frontend`, Node 26.13.0):

```text
npm run lint                   0 errors
npm run typecheck              passed
npm test -- --run              10 passed (5 files)
npm run build                  passed; 9 routes built
npx playwright test            2 passed (home, auth flow)
```

Live proxy verification against the running Django API (not mocked):

```text
GET  /api/v1/auth/csrf/                200 (no redirect)
POST /api/v1/auth/register/            201
GET  /api/v1/me/                       200
POST /api/v1/auth/logout/              204
GET  /api/v1/me/                       401
Playwright live register -> onboarding -> profile -> sign out   passed
```

## 9. Deviations

Recorded in `docs/specifications/SPEC-0001-accounts-and-profile.md` §19:

1. `target_exam` is a validated `CharField` until `catalog.Exam` lands in
   KAB-102.
2. `display_name` lives on `accounts_user` per the approved database design,
   exposed in the API as `profile.display_name`.
3. HIBP breached-password validation is env-gated
   (`ENABLE_BREACHED_PASSWORD_CHECK`, off locally/CI).
4. Account deletion is immediate; no grace period (would require a queue).
5. Export requests are records only; `download_url` is null at alpha.
6. Password reset invalidates sessions by scanning `django_session` rows.

## 10. Risks and notes

- Email delivery is a dependency; only the console/locmem backends are
  configured. A transactional provider is still required before alpha.
- Rate-limit counters use `LocMemCache`, so limits are per process. A shared
  cache is required when more than one API process runs.
- `ENABLE_BREACHED_PASSWORD_CHECK=true` must be set before public alpha.
- Deletion cascade for materials/AI content will be exercised when those
  modules exist.
- Do not add social login before the core flow is stable.

## 11. Review fixes (2026-11-07)

Found while testing registration manually through the real proxy (mocked tests
did not cover it):

1. **Trailing-slash redirect loop.** Next 16 normalized `/api/v1/.../` to
   `/api/v1/...` before the rewrite, Django's `APPEND_SLASH` redirected back,
   and every API call looped. Fixed in `frontend/next.config.ts` with
   `skipTrailingSlashRedirect: true` and a trailing slash in the rewrite
   destination. Guarded by `src/tests/proxy-config.test.ts`.
2. **CSRF origin rejected by the proxy.** The browser sends
   `Origin: http://localhost:3000`, while Django sees its own host, so CSRF
   failed unless the env var was set. `CSRF_TRUSTED_ORIGINS` now defaults to
   `FRONTEND_URL` even outside DEBUG; it still rejects any other origin.
3. **Local database not migrated** (environment only): `manage.py migrate` is
   required before registration works.

## 12. References

- `docs/specifications/SPEC-0001-accounts-and-profile.md`
- `docs/architecture/api-contracts.md` §Auth
- `docs/architecture/backend-architecture.md` §7
- `docs/architecture/decisions/0004-authentication.md`
- `docs/architecture/database-design.md` §3, §10
- `docs/operations/environment-variables.md`
- `docs/product/mvp-scope.md` increment 1
- `docs/engineering/phase-4-clearance-model.md` — Category A gate dependency
