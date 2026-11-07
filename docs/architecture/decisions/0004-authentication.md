# ADR-0004: Authentication via Session Cookie and Same-Origin Proxy

**Status:** Approved — with conditions
**Date:** 2026-11-07
**Approved:** 2026-11-07
**Deciders:** Engineering, Security
**Supersedes:** none

## Context

The frontend runs on Vercel and the API runs on a separately hosted Django
service. We need authentication that:

- does not expose tokens to JavaScript,
- works with server-side rendering,
- avoids third-party cookie restrictions,
- supports CSRF protection,
- does not require a heavy identity provider at MVP.

## Decision

Use **Django session authentication** with the browser talking to the API
through a **same-origin `/api` proxy** provided by Next.js.

- Browser requests go to `https://app.example.com/api/v1/...`.
- Next.js proxies to the Django API (rewrite or route handler).
- The session cookie is set on the app's own origin:
  `HttpOnly`, `Secure` outside local, `SameSite=Lax`, `Path=/`.
- CSRF protection is enabled. The client fetches a token from
  `/api/v1/auth/csrf/` and sends `X-CSRFToken` on unsafe requests.
- The CSRF token is delivered through a secure JSON endpoint
  (`GET /api/v1/auth/csrf/`) that returns `{ "csrfToken": "..." }`; the
  `csrftoken` cookie may remain `HttpOnly` because the token can be delivered
  via the response body and set through a header-safe JSON response. The
  cookie is retained only as a convenience for server-rendered forms.
- Server components call the backend directly and forward the incoming cookie.
- Logout flushes the session server-side.

Authorization remains in Django services; the proxy is not a security boundary.

## Security design details

### CSRF handling

- `CsrfViewMiddleware` is enabled for all unsafe methods (`POST`, `PUT`, `PATCH`,
  `DELETE`).
- The client reads the token from `GET /api/v1/auth/csrf/` and sends it as the
  `X-CSRFToken` header on unsafe requests. The `Referer` check applies to HTTPS
  and is not bypassed for the JSON endpoint.
- CSRF failures return HTTP 403 with `error.code = "csrf_error"; the client
  refetches the token and retries once.

### Session expiration and inactivity policy

- `SESSION_COOKIE_AGE` is set to **14 days** (default) with a sliding inactivity
  timeout (configurable, default **30 minutes of inactivity**).
- On each authenticated request that is not a read of long-lived data, the
  session activity timestamp is refreshed; absolute expiry is enforced by the
  session store.
- Logout (`POST /api/v1/auth/logout/`) flushes the session server-side and clears
  the cookie; subsequent requests with a stale session receive 401.

### Secure proxy header forwarding and cookie handling

- The Next.js proxy forwards `Cookie`, `X-CSRFToken`, and `Content-Type` headers
  to the backend, and forwards `Set-Cookie` responses back to the browser.
- The proxy must not terminate TLS itself; TLS terminates at the edge host.
- Cookies are set on the app's own origin (first-party), never via a redirect to
  the backend origin.

### SSR response caching (user-data leak prevention)

- Authenticated responses must not be served from shared caches (no `public`
  caching directives). Use `private`, `no-store`, or no cache headers for
  responses that include user-specific data.
- Server-rendered authenticated pages must not use a shared ISR/ISR-like cache
  key that ignores the session; use dynamic rendering for user-scoped content.

### Tests

- CSRF rejection test (missing/invalid token returns 403).
- Session invalidation test (logout clears session server-side).
- Cross-user object access test (IDOR: user cannot read another user's data).
- Rate-limit tests on login/password-reset (429 with `Retry-After`).

## Alternatives considered

| Option | Trade-off |
| --- | --- |
| JWT in `localStorage` | XSS can exfiltrate tokens; rejected |
| JWT access in memory + refresh in cookie | More moving parts; refresh rotation and CSRF still needed |
| Cookies across origins (`SameSite=None`) | Third-party cookie blocking makes it unreliable |
| Managed identity provider (Auth0/Clerk) | Cost and lock-in before product validation |
| NextAuth on the frontend | Splits identity between Next.js and Django; Django admin still needs auth |

## Consequences

Positive:

- No token handling in browser JavaScript.
- CSRF protection uses a mature Django mechanism.
- Works with SSR and Django admin.
- No per-request token refresh logic.

Negative:

- The proxy adds a network hop and a component that must forward cookies and
  headers correctly.
- Vercel rewrite limits (body size, timeout) apply to API JSON; large uploads
  bypass the proxy.
- If the frontend and API are later served from different origins without a
  proxy, this decision must be revisited.
- Session storage must be shared/DB-backed if the API scales horizontally.

## Security requirements

- `SESSION_COOKIE_SECURE=True` in production.
- `SESSION_COOKIE_HTTPONLY=True`.
- `CSRF_COOKIE_HTTPONLY=False` (the client must read it) or serve the token via
  a JSON endpoint.
- Rotate the session key on login.
- Rate-limit login and password reset.
- Do not expose the backend origin to the browser.
- Test CSRF rejection and cross-user access (IDOR).

## Approval

Approved on 2026-11-07 with conditions:

- CSRF delivered through a secure JSON endpoint while the CSRF cookie remains
  HttpOnly.
- Session expiration and inactivity policy documented (14-day max age,
  30-minute sliding inactivity default).
- Secure proxy header forwarding and cookie handling documented.
- SSR responses excluded from shared caching for user-specific data.
- Tests for CSRF rejection, session invalidation, and cross-user object access
  included in the test plan.
