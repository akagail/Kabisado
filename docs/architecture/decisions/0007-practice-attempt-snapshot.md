# ADR-0007: Snapshot question content when a practice attempt starts

**Status:** Approved
**Date:** 2026-11-06
**Approved:** 2026-11-07
**Deciders:** Product, Backend, Repository Owner
**Supersedes:** none
**Related:** [KAB-104](../../../tickets/backlog/KAB-104-practice-sessions.md),
SPEC-0004 (planned), [database-design.md](../database-design.md)

**Approval condition:** Implementation must preserve historical question content, answers, scoring, and relevant examination context so future edits cannot alter previous results.

## Context

Practice attempts must produce a result that stays true over time. Content changes
after a session: curators fix typos, correct a wrong key, rewrite an explanation,
or retire an item. The proposed schema stores only `question_id` and the selected
option on each session item, so editing or retiring a question would silently
change historical results and analytics.

The MVP also has to answer a user question honestly: "why did I get this wrong?"
If the item changed since the attempt, a live reference shows an explanation that
does not match what the learner saw.

## Decision

When a practice session starts, copy the item content into the session:

- stem, options and their order, correct option, explanation, and provenance
  (source reference, authoring record, difficulty) are stored on the session item;
- the selected answer is stored against the session item's option, not the live
  option row;
- results, history, and analytics read only session data;
- the live question remains linked for authoring and reporting, and editing or
  retiring it never rewrites an existing session.

Scope: all practice modes in the MVP and beta. The snapshot is per attempt, not
per user, and is never reused across attempts.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
| --- | --- | --- | --- |
| Live reference to question rows | Smallest schema, no duplication | History changes when content changes; retired items break results; explanations can mismatch what the learner saw | Fails the "results are immutable" rule |
| Snapshot only when an item is retired | Small storage growth | Requires migration logic at retire time; mid-session edits still leak; complex to reason about | Complexity is higher than copying at start |
| Immutable question versions (copy-on-write) | Clean authoring history | Heavy for MVP; every edit forks a row; more joins and admin work | Correct but disproportionate now |

## Consequences

Positive:

- Results and analytics are reproducible and explainable.
- Retiring or correcting content is safe; no backfill needed.
- Attempts show exactly what the learner answered and read.

Negative:

- Storage grows with attempts; a 20-item session duplicates item text.
- A corrected key does not retroactively fix an old result.
- Reporting "which version of the item was used" requires reading the snapshot.

Mitigations:

- Store only the fields needed for display and scoring; do not copy unused
  metadata.
- Keep the live question link for content-quality reporting.
- A correction flow can annotate a historical item as "content corrected later"
  without changing the result.
- Revisit if storage or query cost becomes measurable.

## Follow-up

- SPEC-0004 defines the snapshot fields and the scoring path.
- `database-design.md` updates the `SessionItem` entity when the practice spec is
  implemented.
- Metric that would trigger a revisit: session storage growth above the agreed
  budget, or query latency on history exceeding the performance target.

## Approval

Decisions for Phase 2 were delegated by the repository owner on 2026-11-06
("could you decide for me in decisions?"). This ADR may be superseded by a later
decision; it is not self-approved by an agent acting alone.
