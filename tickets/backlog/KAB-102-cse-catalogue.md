# KAB-102: CSE Catalogue and Seed

**Status:** BACKLOG
**Type:** feature
**Priority:** P1
**Epic:** E2 CSE Catalogue
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** required before implementation
**Related ADRs:** ADR-0001, ADR-0003
**GitHub issue:** https://github.com/akagail/Kabisado/issues/15

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
- Target exam selection on the profile.

Out:

- Question content (KAB-103).
- Other exam families.
- Localization.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-002 | approval | pending |
| KAB-004 | content plan | pending |

## 5. Acceptance criteria

- [ ] A seeded CSE Professional catalogue exists with subjects and topics.
- [ ] A seeded CSE Subprofessional catalogue exists.
- [ ] Each exam version stores its official source and metadata.
- [ ] The catalogue is readable by authenticated users.
- [ ] Staff can create/edit catalogue entries in admin.
- [ ] A user can select a target exam.
- [ ] Attempts reference an immutable exam version.
- [ ] Seed is idempotent and environment-guarded.
- [ ] API tests cover access and shape.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement models, constraints, and indexes.
- [ ] Implement the seed command.
- [ ] Implement read endpoints and serializers.
- [ ] Implement admin.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Model constraint tests.
- [ ] Seed idempotency test.
- [ ] API access tests.
- [ ] Admin smoke test.
- [ ] Verify no official exam items are reproduced.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Coverage can change; version everything.
- Do not hardcode 170/165 items as universal constants.
- Topic names should be stable slugs, not display labels.

## 10. References

- `docs/product/cse-exam-reference.md`
- `docs/architecture/database-design.md`
