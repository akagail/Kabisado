# KAB-101: Accounts and Authentication

**Status:** BACKLOG
**Type:** feature
**Priority:** P1
**Epic:** E1 Accounts
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** SPEC-0001 (draft, awaiting approval)
**Related ADRs:** ADR-0004
**GitHub issue:** https://github.com/akagail/Kabisado/issues/14

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
- `GET /auth/me/` and profile update (display name, target exam, timezone).
- Account deletion (grace period and cascade).
- Data export request.
- CSRF endpoint and client handling.
- Login/reset rate limits.
- Login and registration UI states.
- Django admin access for staff.

Out:

- Social login/SSO.
- MFA.
- Email verification (unless approved for this ticket).
- Payments and entitlements.
- Custom user avatars.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-002 | approval | pending |
| KAB-005 | security review | pending |
| KAB-003 | email provider | pending |

## 5. Acceptance criteria

- [ ] A user can register, log in, log out, and reset a password.
- [ ] Passwords use a modern hasher and validators.
- [ ] Session cookie is `HttpOnly`, `Secure`, `SameSite=Lax`.
- [ ] CSRF is enforced on unsafe requests.
- [ ] Login and reset do not reveal whether an email exists.
- [ ] A user can view/update their profile.
- [ ] A user can request deletion; owned data is deleted or anonymized.
- [ ] Cross-user profile access is denied.
- [ ] Rate limits return 429 with `Retry-After`.
- [ ] API tests cover success, validation, unauthenticated, unauthorized, and
      CSRF cases.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement user/profile models and migrations.
- [ ] Implement services and endpoints.
- [ ] Implement the API client CSRF handling.
- [ ] Build the auth screens and states.
- [ ] Add admin and audit logging.
- [ ] Add rate limiting.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Service tests for registration, reset, deletion.
- [ ] API tests for all endpoints and error cases.
- [ ] Frontend tests for forms and error states.
- [ ] E2E: register → login → logout.
- [ ] Security: IDOR, CSRF, enumeration, rate limit.
- [ ] Accessibility: labels, focus, keyboard.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Email delivery is a dependency; a console backend is acceptable only locally.
- Deletion must cover storage and derived AI content.
- Do not add social login before the core flow is stable.

## 10. References

- `docs/specifications/SPEC-0001-accounts-and-profile.md`
- `docs/architecture/api-contracts.md` §Auth
- `docs/architecture/backend-architecture.md` §7
- `docs/architecture/decisions/0004-authentication.md`
- `docs/product/mvp-scope.md` increment 1
- `docs/engineering/phase-4-clearance-model.md` — Category A gate dependency
