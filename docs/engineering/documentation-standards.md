# Documentation Standards

**Status:** Approved for foundation use
**Owner:** Engineering
**Last updated:** 2026-11-06

## 1. Why

Documentation is how a human or agent enters the project without prior context.
It must be accurate, current, and traceable. A stale document is worse than no
document because it misleads.

## 2. Document types

| Type | Location | Purpose |
| --- | --- | --- |
| Product overview | `docs/product/` | Vision, users, scope, roadmap |
| Requirements | `docs/product/product-requirements.md` | Stable requirement IDs |
| Architecture | `docs/architecture/` | System design and boundaries |
| ADR | `docs/architecture/decisions/` | One significant decision |
| Specification | `docs/specifications/` | Approved feature behaviour |
| Plan | `docs/plans/` | Phased execution and reports |
| Engineering standard | `docs/engineering/` | How we build and review |
| Operations | `docs/operations/` | Setup, env vars, deployment |
| Ticket | `tickets/` | Unit of work and acceptance |
| Template | `docs/templates/` | Reusable document skeletons |

## 3. Required header

Every substantive document starts with:

```markdown
# Title

**Status:** Draft | Proposed | Approved | Superseded
**Owner:** Team or role
**Last updated:** YYYY-MM-DD
```

Specifications add: `Ticket`, `Related ADRs`, `Approved by`, `Approved on`.

## 4. Status lifecycle

```text
Draft → Proposed → Approved → Superseded
```

- **Draft:** incomplete, not for implementation.
- **Proposed:** ready for review, decisions are recommendations.
- **Approved:** a human has accepted it; implementation may proceed.
- **Superseded:** replaced by a linked document; keep for history.

An agent may move Draft → Proposed. Only a human approves.

## 5. Naming

- Files: `kebab-case.md`.
- ADRs: `NNNN-short-title.md`.
- Specs: `SPEC-NNNN-short-title.md`.
- Tickets: `KAB-NNN-short-title.md`.
- Plans: descriptive, no dates in the filename.
- Use lowercase unless the name is an acronym.

## 6. Writing style

- Lead with the decision or the point.
- Use short paragraphs and tables.
- Prefer concrete nouns and verbs.
- Define acronyms on first use.
- State assumptions explicitly:

```markdown
**Assumption:** Users have a stable email address.
**Recommendation:** Start with CSE Professional only.
**Needs approval:** Production hosting provider.
```

- Do not present a guess as a fact.
- Do not invent metrics, dates, citations, or validation results.
- Link to sources; do not paste long copyrighted excerpts.
- Use relative links for repository files and absolute URLs for external sources.

## 7. Structure

Recommended order:

1. Status header.
2. Purpose / scope.
3. Context or problem.
4. Decision or requirements.
5. Alternatives / trade-offs.
6. Consequences / risks.
7. Open questions.
8. References.

Not every document needs every section; do not add empty headings.

## 8. Diagrams

- Use Mermaid in fenced blocks.
- Keep diagrams small and labelled.
- A diagram must match the prose; update both together.
- Do not use diagrams for information a short table conveys better.

## 9. Requirements and decisions

- Requirement IDs are stable and never renumbered.
- Use `MUST`, `SHOULD`, `COULD` consistently.
- ADRs record one decision, its alternatives, and consequences.
- Do not edit an approved ADR's decision; write a superseding ADR.

## 10. Specifications

A feature specification must cover:

- Problem and goal.
- User flows (happy path and alternates).
- Permissions and roles.
- Data requirements and validation.
- Edge cases and error states.
- API/UI contract.
- Acceptance criteria (testable).
- Out of scope.
- Risks and dependencies.
- Rollout and observability.

Use `docs/templates/feature-specification.md`.

## 11. Tickets

- One ticket per independently reviewable change.
- Acceptance criteria are observable and testable.
- Out-of-scope is explicit.
- Link the specification, ADRs, and related tickets.
- Update the checklist as work progresses.
- Do not mark complete with unmet criteria.

See `tickets/README.md`.

## 12. Code-adjacent docs

- `README.md` for orientation and quick start.
- `AGENTS.md` for agent rules.
- Module-level `README.md` only when the module needs more than a paragraph.
- Docstrings for public services and non-obvious modules.
- Inline comments for why, constraints, and shortcuts.

## 13. Review

- A document is reviewed like code: accuracy, scope, links, and clarity.
- The owner is responsible for keeping it current.
- Reviewers check that assumptions are labelled and decisions are not implied.
- Broken relative links block merge.
- Do not approve a spec with untestable acceptance criteria.

## 14. Maintenance

- Update the `Last updated` date on substantive edits.
- If a document is no longer true, fix it or mark it `Superseded` in the same PR.
- Remove empty placeholders; do not create a document "for later".
- Quarterly review of architecture and operations docs is recommended.
- The initialization report records what was created and what remains open.

## 15. Templates

- `docs/templates/adr.md`
- `docs/templates/feature-specification.md`
- `docs/templates/technical-design.md`
- `docs/templates/product-requirements.md`
- `docs/templates/implementation-plan.md`
- `docs/templates/test-plan.md`
- `tickets/TEMPLATE.md`
- `.github/PULL_REQUEST_TEMPLATE.md`

Copy a template; do not edit the template to fit one document.
