# KAB-107: AI Platform — Adapter, Prompts, RAG, Quotas

**Status:** BACKLOG
**Type:** feature
**Priority:** P2
**Epic:** E7 AI Platform
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** required before implementation
**Related ADRs:** ADR-0005
**GitHub issue:** https://github.com/akagail/Kabisado/issues/20

## 1. Description

Build the provider-independent AI foundation: adapter interface, fake test
adapter, prompt registry, retrieval over material chunks, output validation,
quotas, cost accounting, and injection defences.

## 2. Business justification

AI features must be swappable, testable, safe, and cost-controlled. Building this
once prevents provider lock-in and scattered prompt logic.

## 3. Scope

In:

- `LLMAdapter` and `EmbeddingAdapter` interfaces.
- At least one real adapter and a deterministic fake adapter.
- Provider/model configuration and fallback policy.
- Versioned prompt files and a registry.
- Structured output schemas and validation.
- pgvector embeddings and owner-scoped retrieval.
- Token/cost accounting and per-user/global quotas.
- Caching by input hash + prompt version + model.
- Prompt-injection test fixtures.
- Error mapping and retry policy.
- Evaluation harness (manual/scheduled, not CI).

Out:

- User-facing generation flows (KAB-108).
- Fine-tuning.
- A general chat interface.
- Multi-provider routing by quality.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-106 | chunks/materials | pending |
| KAB-003 | AI provider selection | pending |
| KAB-005 | privacy review | pending |

## 5. Acceptance criteria

- [ ] Business code depends only on the adapter interface.
- [ ] A fake adapter makes tests deterministic; CI makes no live calls.
- [ ] Prompts are versioned files; the version is stored per generation.
- [ ] Retrieval is scoped to the owner and returns citations.
- [ ] Malformed/partial output is rejected, with one repair attempt.
- [ ] Quotas and a global spend cap are enforced.
- [ ] Injection fixtures do not change system behaviour.
- [ ] Costs are recorded per call and visible in admin/logs.
- [ ] Provider errors map to internal categories with retry rules.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement adapter interfaces and fake.
- [ ] Implement one real adapter behind config.
- [ ] Implement prompt registry and schemas.
- [ ] Implement embeddings/retrieval.
- [ ] Implement quotas, cost, caching.
- [ ] Implement injection tests and evaluation harness.
- [ ] Update docs and ADR status.

## 7. Testing checklist

- [ ] Adapter contract tests.
- [ ] Prompt assembly/delimiter tests.
- [ ] Output validation matrix.
- [ ] Owner-scoped retrieval test.
- [ ] Quota boundary tests.
- [ ] Injection fixtures.
- [ ] No live network in CI.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Do not expose provider SDK types outside `adapters/`.
- Do not log prompt text or document contents.
- A model change needs an evaluation run.
- Keep the interface conservative; do not leak vendor-specific features.

## 10. References

- `docs/architecture/ai-architecture.md`
- `docs/architecture/decisions/0005-ai-provider-abstraction.md`
