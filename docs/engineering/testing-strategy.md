# Testing Strategy

**Status:** Proposed — requires approval
**Owner:** Engineering
**Last updated:** 2026-11-06

## 1. Principles

- Test behaviour, not implementation details.
- Every business rule and permission boundary has a test.
- Every bug fix includes a regression test.
- Tests must be deterministic; no live AI calls, no real network, no wall-clock
  dependence.
- Fast feedback first: unit/service tests on every save; E2E before merge for
  user-flow changes.
- Coverage is a signal, not a target to game.

## 2. Test pyramid

```text
        /\
       /e2e\        few, critical journeys (Playwright)
      /------\
     /  api   \     endpoint contracts, permissions (Pytest + DRF)
    /----------\
   / unit/service\  domain rules, scoring, validation (Pytest/Vitest)
  /--------------\
```

## 3. Backend

### What must be tested

- Services: success, validation failure, permission failure, state transition,
  idempotency.
- Models: constraints and invariants that the database enforces.
- API: status codes, response shape, pagination, auth, object-level access.
- Scoring: correct/incorrect, unanswered, timed expiry, duplicate submit.
- Weak-topic rule: boundaries (exactly 3 attempts, exactly 70%).
- Upload: type/size/checksum validation, ownership, deletion cascade.
- AI: adapter contract, output validation, prompt assembly, injection fixtures,
  quota enforcement, cost accounting. Use a fake adapter.
- Migrations: `makemigrations --check` in CI; migration tests for data backfills.

### Tools

- `pytest`, `pytest-django`, `factory_boy`, `freezegun` (or `time-machine`).
- `APIClient` for endpoint tests.
- `pytest-cov` for coverage reporting.
- `django_assert_num_queries` for N+1 checks.

### Conventions

```python
@pytest.mark.django_db
def test_submit_session_when_already_submitted_is_idempotent(...):
    ...
```

- One behaviour per test.
- Factories over fixtures.
- No network; stub storage and AI adapters.
- Use `pytest.mark.parametrize` for boundary tables.
- Keep the default suite under 60 seconds locally; mark slow tests.

### Coverage expectations

- Domain services and permissions: ≥ 90% line, 100% of decision branches that
  affect access or scoring.
- API modules: ≥ 80%.
- Overall: track, do not block on a single number.
- New code should not lower the project trend.

## 4. Frontend

### What must be tested

- Pure helpers: formatters, score display, time formatting, error mapping.
- Interactive components: form states, validation messages, disabled/pending,
  empty/error/unauthorized states, keyboard interaction.
- Hooks: countdown, autosave, retry.
- API client: error envelope mapping, CSRF header, unauthorized handling.
- Accessibility: labels, focus, roles for critical widgets.

### Tools

- Vitest + Testing Library + `@testing-library/jest-dom`.
- `jsdom` environment.
- Mock at the network boundary (MSW) when integration behaviour matters.
- No snapshot tests of large trees.

### Conventions

- Query by role/label, not by test ID, unless no accessible query exists.
- Assert what the user sees.
- One behaviour per test.
- Clean up timers and listeners.

## 5. End-to-end

Playwright, against a built app and a seeded test database.

Critical journeys:

1. Register → verify (if enabled) → login → logout.
2. Start untimed practice → answer → submit → see score and explanations.
3. Start timed practice → timer expires → auto-submit.
4. Upload a PDF → wait for processing → study flashcards.
5. Generate items → review → approve (staff).
6. Delete a material → derived content is gone.
7. Cross-user access attempt is denied.

Rules:

- Use stable, accessible selectors.
- Seed data through a test API or fixtures, not by clicking through setup.
- No arbitrary sleeps; wait for state.
- Run on Chromium in CI; add WebKit/Firefox before launch.
- One retry maximum; flaky tests are fixed or quarantined with a ticket.

## 6. AI testing

| Layer | Approach |
| --- | --- |
| Adapter contract | Fake adapter and provider-specific contract tests |
| Prompt assembly | Deterministic tests for delimiters and version selection |
| Output validation | Malformed, partial, duplicate-choice, multi-correct fixtures |
| Injection | Adversarial documents must not change system behaviour |
| Retrieval | User scoping, threshold, citation presence |
| Quality | Human-reviewed golden set; manual/scheduled runs, not CI |
| Cost | Token accounting and quota boundary tests |

Live model calls are never part of the required CI pipeline. Evaluation runs use
a separate budget and report.

## 7. Security testing

- Authorization matrix tests for every user-owned resource (IDOR).
- CSRF rejection tests.
- Upload validation tests (extension, MIME, magic bytes, size, checksum).
- Rate-limit tests.
- Dependency audit (`npm audit`, `pip-audit`) in CI.
- Secrets scan before release.
- Prompt-injection fixtures.
- No production data in test environments.

## 8. Performance testing

- Backend: query-count assertions on list endpoints; load test before launch.
- Frontend: Lighthouse budget check before launch; bundle-size review per PR.
- Practice start p95 < 1 s; non-AI API p95 < 400 ms.
- AI jobs: queue latency, not request latency.

## 9. Test data

- Factories generate minimal valid data.
- Seed scripts are idempotent and environment-guarded.
- Never copy production data into local or test environments.
- Use synthetic names, emails, and documents.
- Test uploads are small, non-sensitive files.

## 10. Flaky tests

- A flaky test is a bug.
- Fix the race, add a deterministic wait, or remove the external dependency.
- If quarantine is unavoidable, mark it, open a ticket, and report it in the PR.
- Do not retry indefinitely to hide instability.

## 11. CI mapping

| Check | Workflow |
| --- | --- |
| Ruff format/lint | `backend-ci` |
| Django check + migrations check | `backend-ci` |
| Pytest | `backend-ci` |
| ESLint + typecheck | `frontend-ci` |
| Vitest | `frontend-ci` |
| Production build | `frontend-ci` |
| Playwright | `e2e` |

See `docs/engineering/ci-cd.md`.

## 12. Definition of a good test

- Fails for the right reason.
- Names the behaviour.
- Runs in isolation.
- Does not depend on order or time.
- Uses the smallest setup that proves the point.
- Would catch a realistic regression.
