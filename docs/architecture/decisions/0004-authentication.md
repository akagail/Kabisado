# ADR-0004: Authentication via Session Cookie and Same-Origin Proxy

**Status:** Proposed — requires security review
**Date:** 2026-11-06
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
- Server components call the backend directly and forward the incoming cookie.
- Logout flushes the session server-side.

Authorization remains in Django services; the proxy is not a security boundary.

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

Requires human approval and a security review before implementation.
