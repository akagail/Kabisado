# KAB-109: Flashcard Study Mode

**Status:** BACKLOG
**Type:** feature
**Priority:** P2
**Epic:** E9 Flashcards
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** required before implementation
**Related ADRs:** ADR-0003
**GitHub issue:** https://github.com/akagail/Kabisado/issues/22

## 1. Description

Implement flashcard browsing and study mode with known/unknown tracking. No
spaced-repetition scheduling yet.

## 2. Business justification

Flashcards are a low-friction study mode and the most understandable output of AI
processing. They add value before a full scheduler exists.

## 3. Scope

In:

- Flashcard list by topic/material.
- Study mode: front → reveal → known/unknown.
- Per-user review record (last reviewed, known/unknown count).
- Keyboard and touch navigation.
- Empty, loading, and error states.

Out:

- Spaced repetition (FSRS/SM-2).
- Study plans.
- Sharing decks.
- Image occlusion.
- Public decks.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-108 | generated flashcards | pending |
| KAB-101 | auth | pending |

## 5. Acceptance criteria

- [ ] A user can open a flashcard set and study it.
- [ ] Reveal works by keyboard and touch.
- [ ] Known/unknown is saved per user and card.
- [ ] Another user's review state is inaccessible.
- [ ] Empty state explains how to create cards.
- [ ] Session survives refresh.
- [ ] Mobile layout works at 360 px.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement review model and migration.
- [ ] Implement API.
- [ ] Build study UI.
- [ ] Add keyboard shortcuts and focus handling.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Review persistence test.
- [ ] IDOR test.
- [ ] Component tests for reveal and controls.
- [ ] Keyboard test.
- [ ] Mobile viewport check.
- [ ] E2E study flow.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Do not call it "spaced repetition" until scheduling exists.
- Avoid gamification that pressures users.
- Keep the review record append-only enough to support a future scheduler.

## 10. References

- `docs/product/product-requirements.md` QST-04, REC-03
