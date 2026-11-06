# KAB-108: AI Study Aids and Review Queue

**Status:** BACKLOG
**Type:** feature
**Priority:** P2
**Epic:** E8 Study Aids
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** required before implementation
**Related ADRs:** ADR-0005
**GitHub issue:** none

## 1. Description

Generate summaries, flashcards, and multiple-choice questions from a user's
material, with citations, provenance, a review queue, and flagging.

## 2. Business justification

This is the AI-assisted personalization promise: turning a static reviewer into
study material. It must be trustworthy and auditable.

## 3. Scope

In:

- Summary generation with citations.
- Flashcard generation with source excerpts.
- MCQ generation with exactly one correct answer and explanation.
- Provenance: source chunk, model, prompt version, timestamp.
- Review queue for staff; approve/reject/edit.
- User-private generated items until reviewed.
- Content flagging for AI output.
- UI: generate, progress, view source, flag.
- Quotas and cost display (server-enforced).

Out:

- Autonomous publication.
- Multi-document synthesis.
- Socratic chat.
- Identification items.
- Full mock exam generation.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-107 | AI platform | pending |
| KAB-103 | question model | pending |
| KAB-106 | materials | pending |

## 5. Acceptance criteria

- [ ] A user can generate a summary and flashcards from a ready material.
- [ ] A user can generate MCQs; they remain private until reviewed.
- [ ] Every generated item shows a source excerpt and provenance.
- [ ] Invalid output is rejected, not stored.
- [ ] Staff can approve, reject, or edit generated items.
- [ ] Approved items can enter the shared pool; rejected items do not.
- [ ] Users can flag an item with a reason.
- [ ] Generation is asynchronous with visible progress.
- [ ] Quota exhaustion returns a clear message.
- [ ] Injection attempts in a document do not alter system behaviour.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement generation services and jobs.
- [ ] Implement provenance and citations.
- [ ] Implement review queue and audit.
- [ ] Implement flagging.
- [ ] Build UI.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Generation orchestration with fake adapter.
- [ ] Citation validation test.
- [ ] Review lifecycle test.
- [ ] Quota test.
- [ ] Injection fixture test.
- [ ] E2E: upload → generate → view source.
- [ ] Staff review E2E.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Never publish unreviewed output.
- Keep generated content labelled and distinguishable from human content.
- Source excerpts must be short and attributed.
- A failed generation must not block studying the original material.

## 10. References

- `docs/architecture/ai-architecture.md` §9
- `docs/product/mvp-scope.md` increment 2
