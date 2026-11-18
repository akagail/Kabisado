# KAB-116: Enforce Session Inactivity Timeout

**Status:** READY
**Type:** security
**Priority:** P1
**Epic:** E1 Accounts
**Owner:** unassigned
**Created:** 2026-11-17
**Updated:** 2026-11-17
**Specification:** ADR-0004 (approved condition)
**Related ADRs:** ADR-0004
**GitHub issue:** https://github.com/akagail/Kabisado/issues/60

## 1. Description

ADR-0004's approval condition promises a 30-minute sliding inactivity timeout on
top of the 14-day absolute session age. The current settings use
`SESSION_COOKIE_AGE = 14 days` and `SESSION_SAVE_EVERY_REQUEST = False`, with no
inactivity middleware, so an idle authenticated session stays valid for up to
14 days.

## 2. Business justification

A shared or lost device keeps a session alive far longer than the security
condition allows. This is a P1 authentication gap to close before the private
alpha.

## 3. Scope

In:

- Record the last authenticated activity on the session.
- Expire the session after `SESSION_INACTIVITY_SECONDS` (default 1800).
- Refresh activity on authenticated requests, throttled to avoid a write per
  request.
- Keep the 14-day absolute expiry as the upper bound.
- Tests for refresh, expiry, logout, and anonymous requests.

Out:

- "Stay signed in" / remember-me.
- MFA.
- Changing the 14-day absolute age.
- Frontend changes (401 handling already exists).
- An idle-warning modal.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| ADR-0004 | architecture | Approved 2026-11-07 (condition open) |
| KAB-101 | ticket | Completed 2026-11-08 |

## 5. Acceptance criteria

- [ ] An authenticated request refreshes the inactivity timestamp.
- [ ] A request after the timeout returns 401 and flushes the session.
- [ ] Requests inside the window do not expire the session.
- [ ] The 14-day absolute expiry still applies.
- [ ] The timeout is configurable via `SESSION_INACTIVITY_SECONDS`; default 1800.
- [ ] Tests cover refresh, expiry, anonymous, and logout paths.
- [ ] The ADR-0004 condition is recorded as satisfied.

## 6. Implementation checklist

- [ ] Add the inactivity middleware or session helper.
- [ ] Add the setting and `.env.example` entry.
- [ ] Update `docs/operations/environment-variables.md`.
- [ ] Update `docs/engineering/security-guidelines.md` if the policy changes.
- [ ] Add the regression tests.
- [ ] Run the backend checks from `AGENTS.md` §13.

## 7. Testing checklist

- [ ] Unit tests for the timeout decision.
- [ ] API test: a request after idle time returns 401.
- [ ] API test: activity refresh keeps the session alive.
- [ ] CSRF and auth regression tests.
- [ ] Manual check with a short timeout value.

## 8. Validation evidence

Record commands and results. Do not paste secrets or production data.

```text
(pending)
```

## 9. Risks and notes

- Writing the timestamp on every request adds database writes; throttle updates
  to at most once per minute.
- The timestamp must live in the shared session store, not process memory, if
  the API scales horizontally.
- A 30-minute timeout can log out a learner mid-study; confirm the 401 handling
  experience before alpha.

## 10. References

- Specification: ADR-0004 §"Session expiration and inactivity policy"
- ADR: `docs/architecture/decisions/0004-authentication.md`
- Design: SPEC-0001 (accounts)
- Related tickets: KAB-101
