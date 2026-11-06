# Test Plan: Feature

**Status:** Draft
**Owner:** Name/role
**Ticket:** KAB-NNN
**Specification:** SPEC-NNNN
**Last updated:** YYYY-MM-DD

## 1. Scope

What is being tested, and what is explicitly not?

## 2. Test strategy

| Layer | Tool | Coverage |
| --- | --- | --- |
| Unit | Pytest / Vitest | |
| API | Pytest + DRF | |
| Component | Vitest + Testing Library | |
| E2E | Playwright | |
| Security | manual + automated | |
| Accessibility | manual + axe | |

## 3. Test environment

- OS/browser/device.
- Database and seed data.
- Feature flags.
- External services: fakes or stubs.

## 4. Cases

| ID | Scenario | Steps | Expected | Automated |
| --- | --- | --- | --- | --- |
| T-01 | | | | Yes/No |

Include:

- happy path,
- validation failures,
- permission/ownership failures,
- boundary values,
- empty/loading/error states,
- retries/idempotency,
- accessibility,
- regression.

## 5. Test data

- Factories/seed.
- Files used.
- No production data.

## 6. Entry criteria

- Spec approved.
- Environment available.
- Build deployed.

## 7. Exit criteria

- All critical cases pass.
- No open high-severity defects.
- Coverage expectations met.
- Results recorded in the ticket.

## 8. Risks and limitations

- ...
