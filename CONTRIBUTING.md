# Contributing to Kabisado

Kabisado is documentation-first and ticket-driven. Read
[`AGENTS.md`](AGENTS.md) before changing code, even if you are human.

## 1. Before you start

- Check the backlog: [`tickets/backlog/`](tickets/backlog/).
- Significant features need an approved specification in
  [`docs/specifications/`](docs/specifications/).
- Architecture changes need an ADR in
  [`docs/architecture/decisions/`](docs/architecture/decisions/).
- If your idea has no ticket, open one using the template.

## 2. Set up

Follow [`docs/operations/local-development.md`](docs/operations/local-development.md).
Short version:

```bash
# Backend
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements-dev.txt
python manage.py migrate
pytest

# Frontend
cd frontend
npm ci
npm run dev
```

Copy `.env.example` to `.env` in the relevant app and fill in local values.
Never commit `.env`.

## 3. Pick up a ticket

1. Move the ticket from `tickets/ready/` to `tickets/in-progress/`.
2. Create a branch from `main`:
   `git switch -c feat/KAB-012-short-description`.
3. Read the ticket's specification and related ADRs.
4. Post a short implementation plan in the ticket if the change is non-trivial.

## 4. Make the change

- Stay within the ticket scope. New work becomes a new ticket.
- Add tests with the implementation.
- Add migrations for model changes.
- Update docs when behaviour or architecture changes.
- Keep commits small and conventional:
  `feat(auth): add login endpoint`, `docs(adr): accept modular monolith`.

## 5. Validate

```bash
# Backend
cd backend
ruff format --check .
ruff check .
python manage.py check
python manage.py makemigrations --check --dry-run
pytest

# Frontend
cd frontend
npm run lint
npm run typecheck
npm test -- --run
npm run build
```

For user-flow changes, also run `npx playwright test`. If a check cannot run,
say so in the PR; do not claim it passed.

## 6. Open a pull request

Use the PR template. Include:

- Ticket link and the specification it implements.
- What changed and why.
- Test evidence (commands and results).
- Security and data risks.
- Screenshots for UI changes.
- Follow-up tickets for deliberately deferred work.

A PR is mergeable when reviewed, CI is green, and acceptance criteria are met.

## 7. Review standards

Reviewers check correctness first, then scope, security, tests, and
maintainability. Style comments should point to the documented standard, not
personal preference. Blocking comments must be resolved or explicitly deferred
with a ticket.

## 8. Reporting bugs and vulnerabilities

- Functional bugs: use the bug issue form or a bug ticket.
- Security issues: do not open a public issue. Contact the maintainer privately.

## 9. Conduct

Be direct, technical, and respectful. Critique the work, not the person. Do not
publish other people's personal data, copyrighted material, or credentials.
