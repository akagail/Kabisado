# KAB-102: CSE Catalogue and Seed

**Status:** REVIEW
**Type:** feature
**Priority:** P1
**Epic:** E2 CSE Catalogue
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-10
**Specification:** SPEC-0002 (approved 2026-11-07)
**Related ADRs:** ADR-0002, ADR-0003, ADR-0008 (draft; one exam version in MVP)
**Branch:** `feat/KAB-102-cse-catalogue`
**GitHub issue:** https://github.com/akagail/Kabisado/issues/15
**Pull request:** https://github.com/akagail/Kabisado/pull/36

## 1. Description

Implement the exam taxonomy (family → exam → version → subject → topic) and seed
the CSE Professional and Subprofessional catalogue from the official coverage
areas.

## 2. Business justification

Questions, practice sessions, and analytics all depend on a stable taxonomy.
Without exam versions, bulletin changes would rewrite historical attempts.

## 3. Scope

In:

- Models and migrations for family, exam, version, subject, topic.
- Parent/child topics with display order.
- Seed command/data for CSE Professional and Subprofessional.
- Exam version records with source URL, date, item count, time limit, passing
  rate.
- Read API for the catalogue.
- Admin management.
- Target exam selection on the profile (replaces the KAB-101 slug field with the
  `catalog.Exam` FK).
- Catalogue screens: `/exams`, `/subjects/[id]`, `/topics/[id]` (SPEC-0002 §9).

Out:

- Question content (KAB-103).
- Other exam families.
- Localization.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| SPEC-0002 | specification | approved 2026-11-07 |
| Category A gate | approval | cleared 2026-11-07 (`phase-4-clearance-model.md`) |
| KAB-004 | content plan | pending — blocks question content (KAB-103), not the taxonomy seed |
| KAB-101 | ticket | completed 2026-11-08 (target exam selection depends on it) |

## 5. Acceptance criteria

- [x] A seeded CSE Professional catalogue exists with subjects and topics.
- [x] A seeded CSE Subprofessional catalogue exists.
- [x] Each exam version stores its official source and metadata.
- [x] The catalogue is readable by authenticated users.
- [x] Staff can create/edit catalogue entries in admin.
- [x] A user can select a target exam.
- [ ] Attempts reference an immutable exam version — **deferred:** practice
      sessions do not exist until KAB-104; the schema supports it.
- [x] Seed is idempotent and environment-guarded.
- [x] API tests cover access and shape.

## 6. Implementation checklist

- [x] Write and approve the specification (SPEC-0002, 2026-11-07).
- [x] Technical design — SPEC-0002 §7–8 plus §19 implementation notes.
- [x] Implement models, constraints, and indexes.
- [x] Implement the seed command.
- [x] Implement read endpoints and serializers.
- [x] Implement admin.
- [x] Update docs and OpenAPI.

## 7. Testing checklist

- [x] Model constraint tests.
- [x] Seed idempotency test.
- [x] API access tests.
- [x] Admin smoke test.
- [x] Verify no official exam items are reproduced — no items are in scope;
      the seed contains coverage-area names only.

## 8. Validation evidence

```text
backend    ruff format --check   clean
           ruff check            clean
           manage.py check       no issues
           makemigrations --check no changes
           pytest                51 passed
frontend   npm run lint          0 errors
           npm run typecheck     passed
           npm test -- --run    26 passed (10 files)
           npm run build         passed; /exams, /subjects/[id], /topics/[id] added
           npx playwright test   3 passed
seeding    manage.py seed_cse_catalogue → 2 exams, 8 subjects, 32 topics;
           second run adds 0
```

## 9. Risks and notes

- Coverage can change; version everything.
- Do not hardcode 170/165 items as universal constants — the 2027 bulletin
  publishes neither item count nor time limit, so both are null.
- Topic names should be stable slugs, not display labels.
- `accuracy`, `attempts`, and `weak_topic` are placeholders until KAB-104;
  SPEC-0002 §14 weak-topic criteria are not yet verifiable.
- Follow-up when practice lands: compute per-topic accuracy from
  `PracticeResponse` and enforce the immutable `exam_version` FK on attempts.

## 10. References

- `docs/specifications/SPEC-0002-cse-catalogue.md`
- `docs/architecture/api-contracts.md` §Catalogue
- `docs/engineering/phase-4-clearance-model.md` — Category A gate dependency
