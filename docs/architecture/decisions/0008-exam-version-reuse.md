# ADR-0008: Exam-version topic reuse vs duplication

**Status:** Draft
**Date:** 2026-11-07
**Deciders:** Product / Backend
**Supersedes:** none
**Related:** [database-design.md](../database-design.md), [cse-exam-reference.md](../../product/cse-exam-reference.md),
SPEC-0002 (planned), KAB-102, O7 in [open-decisions.md](../../decisions/open-decisions.md)

## Context

The Civil Service Commission publishes a new examination announcement before each
CSE sitting. The announcement defines the coverage (subjects, topics, and
sub-topics) for that specific exam version. Coverage can change between
versions: topics may be added, removed, reworded, or re-ordered.

The current schema (per `database-design.md`) models:

```text
ExamVersion → Subject → Topic → Question
```

Each `ExamVersion` owns its `Subject` rows, which own their `Topic` rows. A new
CSE announcement would create a new `ExamVersion` and a fresh tree of subjects
and topics. Questions link to a `Topic`, so they are implicitly version-scoped.

This is simple and guarantees historical isolation: a learner's 2027 practice
results are never affected by a 2028 coverage change. The downside is that
seeding a new version duplicates the topic tree, even for topics that are
identical across versions.

The alternative is to share `Topic` rows across versions via a many-to-many
`ExamVersionTopic` table that stores version-specific metadata (display order,
item count, weight, language). Questions would link to the shared `Topic`. A
version change would add or remove mappings rather than duplicate rows.

The decision must be made before a second `ExamVersion` is seeded, because
changing the model after data exists requires a migration and a content
reconciliation.

## Decision

**Default: duplicate the topic tree per `ExamVersion`.**

- A new CSC announcement creates a new `ExamVersion` and its own `Subject` and
  `Topic` rows, seeded from the official coverage.
- Topics are not shared across versions unless an explicit cross-version mapping
  is added later (a separate table, not part of the MVP).
- Questions always link to a version-specific `Topic`, so they are bound to the
  coverage they were authored for.
- Historical practice results and analytics read only the version the attempt
  used; a new version cannot silently alter past data.

## Alternatives considered

| Option | Pros | Cons | Why not chosen |
| --- | --- | --- | --- |
| Duplicate per version (chosen) | Simple; historical isolation guaranteed; no silent changes when a new version is added; matches the CSC's publication model (each bulletin is a standalone document) | Seeding effort repeats for unchanged topics; cross-version reporting ("how did I do on Word Analogy across all versions?") needs a separate mapping table | — |
| Shared topics with `ExamVersionTopic` mapping | DRY; easy cross-version progress tracking; fewer rows to seed for minor changes | A topic edit (reword, reorder) affects all versions that map to it; CSC changes are not always compatible (e.g., a topic split or merge); version-specific metadata (item count, weight) lives on the mapping, adding complexity | Silent cross-version changes violate the principle that historical results must not change |
| Hybrid: core topics shared, overlays per version | Balances reuse and isolation | Still requires a rule for what is "core"; overlay logic adds complexity; no clear CSC signal for core vs version-specific | Over-engineering for MVP |

## Consequences

Positive:

- Zero risk of a 2028 bulletin silently rewriting 2027 learner analytics.
- Seeding script is straightforward: parse the announcement, create the tree.
- No migration needed when the next announcement arrives.

Negative:

- Seeding the 2028 version repeats work for topics that are identical to 2027.
- Cross-version analytics require a mapping table (can be built later, not in
  MVP).
- Topic IDs are not stable across versions; a "Word Analogy" topic in 2027 and
  2028 are different rows.

Mitigations:

- Build a seeding utility that copies the previous version's tree and applies a
  diff from the new announcement, so only changed topics are manually edited.
- Defer the cross-version mapping table until reporting needs it; it is purely
  analytical, not functional.

## Follow-up

- When the next CSC announcement is published, seed the new version using the
  duplication approach. Measure the actual seeding effort.
- If seeding effort becomes a bottleneck, propose ADR-0008 amendment to add a
  `TopicMapping` table for explicit reuse, with a migration that backfills the
  2027 topics as the "base" version.
- Update `database-design.md` when the mapping table is added (not before).

## Approval

Required before a second `ExamVersion` is modelled in SPEC-0002 or seeded in
KAB-102. This ADR remains `Draft` until explicitly approved.