# Coding Standards

**Status:** Approved for foundation use
**Owner:** Engineering
**Last updated:** 2026-11-06

These rules apply to all code. When a rule is wrong for a specific case, document
the exception in the PR.

## 1. General

- Optimize for the next reader, not for cleverness.
- Keep functions small and single-purpose.
- Prefer explicit names over comments.
- Comment the **why**, not the **what**. One line is usually enough.
- Do not leave commented-out code, dead branches, or unused imports.
- Do not add abstractions for a single use.
- Handle errors at the boundary; do not swallow them.
- Keep secrets and environment-specific values out of code.

## 2. Python / Django

### Formatting and linting

- Ruff formats and lints. Line length 100. Target Python 3.13.
- Rules: `E`, `F`, `I`, `B`, `UP`, `DJ`, `S` (security) with documented ignores.
- No `# noqa` without a reason on the same line.
- Type hints on public functions, service boundaries, and non-trivial helpers.
- `from __future__ import annotations` is not needed on 3.13.

### Imports

Order: standard library, third-party, first-party, local. Use absolute imports
for apps (`from apps.practice.services import ...`); relative imports only within
a package for tightly coupled modules.

### Naming

| Thing | Convention | Example |
| --- | --- | --- |
| Module/package | `snake_case` | `practice/` |
| Class | `PascalCase` | `PracticeSession` |
| Function/variable | `snake_case` | `submit_session` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_UPLOAD_BYTES` |
| Boolean | `is_` / `has_` / `can_` | `is_approved` |
| QuerySet method | noun phrase | `approved_questions()` |
| Service | verb + noun | `create_practice_session()` |

### Models

- Explicit `related_name` on foreign keys.
- Explicit `on_delete`.
- `__str__` for admin readability.
- Constraints in `Meta.constraints` when the database can enforce them.
- Keep business workflows out of `save()`; use services.
- Avoid signals for domain logic; they hide control flow. Use them only for
  cross-cutting audit/cache invalidation with a comment.

### Services and views

- Views: authenticate, authorize, validate via serializer, call one service,
  return a response.
- Services: accept keyword-only primitives/IDs, open a transaction when multiple
  writes must be atomic, enforce permissions, return a domain object.
- Do not pass `request` into a service.
- Raise typed domain exceptions; map them to HTTP responses in one place.
- Use `select_related` / `prefetch_related` for known access patterns.
- Avoid N+1 queries; test query counts for list endpoints.

### Errors and logging

- Never use bare `except:`.
- Catch the narrowest exception; re-raise with context if needed.
- Use `logger.exception` inside an exception handler; `logger.info` otherwise.
- Do not log secrets, tokens, document text, or full request bodies.
- User-facing messages are neutral; internal details go to logs.

### Transactions

- Use `transaction.atomic()` around multi-row invariants.
- Do not hold a transaction open across network calls (AI, storage, email).
- Use `select_for_update()` for contended state transitions (e.g. submit).

### Tests

- Pytest style: plain functions, fixtures, `pytest.mark.django_db`.
- Name: `test_<expected>_when_<condition>`.
- One behaviour per test.
- Use factories, not large JSON fixtures.
- Assert behaviour and response shape, not implementation internals.

## 3. TypeScript / React

### Formatting and linting

- TypeScript `strict: true`.
- ESLint with Next.js core-web-vitals and TypeScript rules.
- Prettier is not configured; ESLint and editor defaults are authoritative.
- No `any` without a comment explaining why. Prefer `unknown` + narrowing.
- No non-null assertion (`!`) unless the invariant is local and obvious.

### Naming

| Thing | Convention | Example |
| --- | --- | --- |
| File | `kebab-case` | `practice-session.tsx` |
| Component | `PascalCase` | `PracticeSession` |
| Hook | `use` + `PascalCase` | `useCountdown` |
| Type/interface | `PascalCase` | `PracticeSession` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_ITEMS` |
| Boolean | `is` / `has` / `can` | `isSubmitting` |

### Components

- Server component by default; add `"use client"` only when needed.
- One component per file, named after the file.
- Props are typed and read-only.
- No business logic in components.
- Extract repeated markup into a component after the second duplication, not the
  first.
- Keep `components/ui` (shadcn) close to upstream; document modifications.

### Data and state

- One API client module owns base URL, headers, CSRF, and error mapping.
- Do not fetch in a component that could be a server component.
- Keep filters/pagination in the URL.
- No global state library until measured.
- Mutations handle pending, success, and error states.
- Cancel or ignore stale requests where the UI can change quickly.

### Styling

- Tailwind utilities with semantic tokens.
- No inline hex colours.
- Use `cn()` for conditional classes.
- Mobile-first; test at 360 px.
- Respect `prefers-reduced-motion`.

### Accessibility

- Every input has a label.
- Every icon-only button has an accessible name.
- Do not remove focus outlines without a visible replacement.
- Dialogs trap focus and restore it on close.
- Announce async results where appropriate.
- Test with keyboard.

## 4. API and data contracts

- API fields are `snake_case`; convert at the client boundary, not ad hoc.
- IDs are UUID strings.
- Timestamps are ISO 8601 UTC.
- Enums are stable strings; do not use display labels as values.
- Nullable means "unknown/not set", not "empty string".
- Every list response is paginated.
- Error responses follow the documented envelope.

## 5. Comments and documentation

- Docstrings on public services and non-obvious modules.
- Comments explain constraints, trade-offs, or workarounds.
- Mark deliberate shortcuts:

```python
# shortcut: synchronous scoring is fine under 200 items; move to Celery if sets grow.
```

- Update the relevant doc when behaviour or architecture changes.
- Do not duplicate documentation in code and Markdown; link instead.

## 6. Review checklist

- [ ] Scope matches the ticket.
- [ ] Names are clear and consistent.
- [ ] Errors are handled, not swallowed.
- [ ] Authorization checks exist for every object access.
- [ ] Queries avoid N+1 and unbounded scans.
- [ ] Tests cover success, failure, and permission cases.
- [ ] No secrets, PII, or document content in logs.
- [ ] Documentation updated.
- [ ] No unrelated refactor.
