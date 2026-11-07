# ADR-0005: Provider-Independent AI Adapter and RAG

**Status:** Approved in Principle
**Date:** 2026-11-06
**Approved in Principle:** 2026-11-07
**Deciders:** Engineering, Product
**Supersedes:** none

**Conditions for full approval:**
- Grounding and source attribution must be enforced in the adapter contract
- Structured output validation with schema rejection (not repair)
- Provider independence: no vendor SDK outside `adapters/`
- Privacy protections: contractual training prohibition, retention limits, redaction
- Human review required before shared publication
- Spend caps and per-user quotas mandatory

## Context

The product depends on LLM and embedding providers for summaries, flashcards,
questions, and grounded explanations. Provider pricing, quality, availability,
and data terms change quickly. Coupling business logic to one vendor would make
migration expensive and create lock-in.

## Decision

1. All model calls go through an adapter interface in `backend/apps/ai/`.
2. Provider and model are configuration, never hardcoded in business logic.
3. Generation uses RAG over the user's own material and approved content.
4. Outputs are structured, validated, and stored with provenance.
5. A deterministic fake adapter is used in tests; CI never calls a live provider.
6. Generated questions require human review before shared use.

## Alternatives considered

| Option | Why not now |
| --- | --- |
| Direct vendor SDK calls | Fast initially, but scattered lock-in and hard to test |
| LangChain/LlamaIndex orchestration | Heavy abstraction; hides prompts and costs; can be added later behind the adapter if justified |
| Fine-tuned model | No data or budget at MVP |
| No RAG (prompt-only) | Hallucination and citation failures are unacceptable for study content |
| External vector database | pgvector is sufficient at MVP scale |

## Consequences

Positive:

- Providers can be swapped or A/B tested.
- Costs and latency are observable in one place.
- Prompt injection and output validation are centralized.
- Tests are deterministic.

Negative:

- The adapter must cover provider-specific features conservatively.
- A lowest-common-denominator interface can hide useful capabilities.
- RAG adds chunking, embedding, and retrieval infrastructure.

## Guardrails

- No provider SDK outside `adapters/`.
- No prompt text outside `prompts/`.
- No live provider call in CI.
- No generated item without a source citation.
- No shared publication without review.
- Spend caps and per-user quotas are mandatory.

## Approval

Requires human approval, including the first provider and data-processing terms.
