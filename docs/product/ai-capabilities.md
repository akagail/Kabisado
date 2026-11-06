# AI Capabilities and Limitations

**Status:** Approved — product decisions delegated by the repository owner,
2026-11-06. Provider-dependent items remain gated.
**Owner:** Product / AI
**Last updated:** 2026-11-06

Product-level policy for AI features. Implementation details and component
boundaries are in [ai-architecture.md](../architecture/ai-architecture.md); this
document decides **what AI may do, what it must show, and what it must never do**.

**Release status:** no AI feature is in the MVP. Everything here is fast-follow
beta (increment 2) except personalized recommendations, which are post-MVP.

## 1. Principles

1. **Grounded, not generative.** Output must be derived from retrieved source
   passages the user can open. If the source does not support the claim, the
   system refuses rather than guesses.
2. **Attributed by default.** Every generated artifact stores and displays its
   source passage, model, prompt version, and generation time.
3. **Human-reviewed before shared.** Generated items never enter a shared pool
   without passing automated validation and human review.
4. **Never official.** Nothing is presented as CSC material, an official answer,
   or an eligibility statement.
5. **Private by default.** A user's documents, generated items, and attempts are
   visible only to that user; staff see them only through a documented moderation
   action.
6. **Bounded.** Per-user quotas, a global spend cap, and a kill switch that
   disables generation without disabling study features.
7. **Replaceable.** Provider and model are configuration; a change requires a
   re-run of the evaluation set before release.

## 2. Capability matrix

| Capability | Release | Grounding | Human review | User-visible label |
| --- | --- | --- | --- | --- |
| Document processing (extraction, chunking, embedding) | Beta | Source file itself | Not applicable | Extraction status and errors |
| Summarization | Beta | Retrieved passages | Before shared use | AI-generated summary + citations |
| Question generation | Beta | Retrieved passages | Required for shared pool | AI-generated; unverified or reviewed |
| Answer explanations | Beta | Cited passage plus curated answer | Required before replacing curated text | AI-generated explanation + citation |
| Topic explanations | Beta | Curated catalogue plus cited sources | Required for shared use | AI-generated + citation |
| Flashcards | Beta | Retrieved passages | Not required for private study | AI-generated + citation |
| Personalized recommendations | Post-MVP | The user's own attempt data | Not applicable | "Based on your practice" + rule shown |

Anything not in this table is out of scope: no general chatbot, no tutoring
dialogue, no voice, no image generation, no model training or fine-tuning.

## 3. Document processing

Not a generative feature, but it feeds every other capability and carries the
same trust requirements.

- Accepted types: PDF and DOCX in the beta; no images or scanned PDFs.
- Files are validated by extension, MIME type, magic bytes, and size before
  storage; parsing runs in a constrained worker (`NFR-SEC-05`).
- Extraction reports one of: `queued`, `processing`, `ready`, `failed`,
  `needs_ocr`. Scanned documents are flagged, never silently treated as empty.
- A part-extracted document is marked with what was read; the UI never implies
  full coverage.
- Chunks retain page or section references so citations resolve to a location.
- Embeddings and extracted text are deleted with the material.

## 4. Summarization

- Summaries cover only the retrieved passages, not the document "in general".
- Every summary claim links to at least one passage; uncited sentences are
  removed or flagged before display.
- A summary states its coverage ("pages 3–7 of 20") so omission is visible.
- Users can open the passage from the summary.
- AI summaries never overwrite the uploaded file or a curated summary.

## 5. Question generation

**Purpose:** turn an approved source into practice items without inventing
coverage.

Rules:

- Generated items must be scoped to an existing catalogue topic. Generating
  content for a topic outside the official coverage is refused.
- The correct answer must be supported by the cited passage; the explanation must
  reference it.
- Automatic checks reject an item when: the schema is invalid, there is not
  exactly one correct answer, options duplicate each other, an option is
  ambiguous with the key, the citation does not resolve, or the item restates an
  official exam item verbatim.
- Generated items never claim to be official, recalled, or actual CSC questions.
- Shared pools require review by a human other than the item's owner, with the
  review recorded.
- The generator may practise their own unverified items (see §7); nobody else
  can see them.

## 6. Explanations and topic explanations

- An explanation answers **why the key is correct and why the main distractor is
  wrong**, using the cited passage.
- When a curated item already has a human explanation, AI may draft an
  alternative but cannot replace the curated text without review.
- Topic explanations summarize the official coverage area, cite curated sources,
  and must not add coverage the CSC has not published.
- If the retrieved material does not cover the question, the system returns "not
  in this material" instead of a plausible-sounding answer.

## 7. The review boundary

Two tiers, and nothing in between:

| Tier | Who sees it | How it is labelled | Allowed behaviour |
| --- | --- | --- | --- |
| Unverified private | Only the generating user | "AI-generated · not reviewed" | View, study as flashcards, practise in a labelled set |
| Reviewed shared | Any learner with access to the topic | "AI-generated · reviewed" | Appears in normal practice sets and analytics |

Rules:

- An unverified item is never shown to another user and never enters a shared
  set.
- Attempts on unverified items are labelled and **excluded from weak-topic
  diagnosis**, so generated content cannot steer the curated study path.
- Attempts on reviewed items behave like curated items.
- Deleting the source material deletes its derived items and cards.
- Reviewing or retiring an item is audited with actor, time, and reason.

This resolves the `AI-05` conflict: users may practise their own unreviewed
items, but only privately, labelled, and outside diagnosis.

## 8. Source attribution

Every generated artifact stores, and the UI exposes:

| Field | Example |
| --- | --- |
| Source type | User material, curated source, catalogue coverage |
| Source reference | Material id + page or section |
| Passage | The exact text used |
| Model | Provider and model identifier |
| Prompt version | Versioned prompt file id |
| Generated at | ISO 8601 UTC |
| Review state | Unverified or reviewed, with reviewer and date |

Attribution is structured data, not only prose. A citation the user cannot open
is treated as missing, and the item fails validation.

For original authored items, provenance is the authoring record (author, coverage
area, review date, reviewer) — the same rule agreed in the MVP scope.

## 9. Hallucination prevention

Layered, in this order:

1. **Retrieval gate.** No generation without retrieved passages above a relevance
   threshold. Below threshold, refuse and say so.
2. **Constrained output.** The model returns a fixed schema; malformed output is a
   failure, never repaired by guessing.
3. **Deterministic checks.** Exactly one key, no duplicate options, citation
   resolves, answer text appears in or is entailed by the passage, no verbatim
   official item.
4. **Human review.** Required before shared use; reviewers can reject with a
   reason that feeds the evaluation set.
5. **Feedback loop.** User flags, reviewer rejections, and corrections are
   reviewed weekly during beta and added to the regression set.

Known limits we do not hide: retrieval can miss context; long documents can
exceed the window; Filipino-language output is less reliable than English;
numeric and symbolic items are the most likely to be subtly wrong.

## 10. Privacy and data handling

- Uploading a document is consent to process it for that user's study features;
  it is not consent to train a model or to publish content.
- The provider must contractually prohibit training on user content and limit
  retention (`NFR-SEC-08`). Without those terms, the feature does not ship.
- Only the chunks needed for a request are sent, not the whole document.
- Prompts are logged by hash and version, not by full document content.
- Logs exclude document text, passwords, tokens, and unnecessary PII.
- Account or material deletion removes extracted text, chunks, embeddings, and
  derived items; backups expire on the documented schedule.
- No cross-user context: one user's material or history never appears in another
  user's prompt.

## 11. Prompt injection and untrusted input

- Uploaded documents are untrusted input. Their text is delimited and labelled as
  data, never as instructions.
- The instruction hierarchy is explicit: system policy, then task, then quoted
  source. Source text cannot override policy.
- Detected injection attempts are refused, logged as a security event, and
  reported to the user without echoing the payload.
- The injection test suite is part of CI for the AI module.

## 12. Cost and quotas

- Per-user daily generation limits, per-job limits, and a global daily spend cap.
- Hitting a cap disables generation only; practice, results, and history keep
  working.
- Caching by input hash plus prompt version avoids paying twice for the same
  output.
- Cheaper models may draft; the reviewed output is what users see.
- Cost per monthly active user is measured and reported against the approved cap
  (M9).

## 13. Evaluation and quality gates

Before beta and before any model or prompt change:

| Gate | Measure | Proposed threshold |
| --- | --- | --- |
| Citation validity | Published AI items whose citation resolves | 100% |
| Automated validation | Generations that pass all deterministic checks | ≥ 95% |
| Factual correctness | Sampled generated items judged correct by a reviewer | ≥ 90% |
| Explanation usefulness | Sampled explanations rated helpful by a reviewer | ≥ 80% |
| Injection resistance | Adversarial suite cases blocked or safely handled | 100% |
| Cross-user exposure | Confirmed exposures | 0 |
| Cost | Cost per monthly active user | Within the approved cap |

Evaluation uses a fixed golden set per capability, run without live provider calls
in CI where possible; a small live smoke test runs on a schedule, not on every
commit. Prompt files are versioned; a prompt change is a reviewed change.

## 14. Disclosure and UX

- Every AI artifact carries a visible label and a link to its source.
- The label distinguishes **unverified** from **reviewed**.
- The UI states the limitation in plain language: AI can be wrong; verify against
  the source; it is not official CSC material.
- No anthropomorphic claims ("I know the answer"), no implied authority, no
  urgency or engagement pressure.
- Refusals are honest: "this is not covered in your material" is a valid,
  expected outcome.
- Users can flag any AI output; flags enter the same queue as content flags.

## 15. Prohibited uses

- Reproducing, reconstructing, or soliciting actual CSC exam items.
- Presenting generated content as official, accredited, or CSC-endorsed.
- Answering eligibility, application, or legal questions as fact.
- Autonomous publication or self-approval of generated content.
- Training or fine-tuning on user content, or using one user's data for another.
- Generating content from unlicensed third-party material.
- General-purpose chat or tutoring beyond the defined capabilities.
- Using AI to predict an official rating or a pass/fail outcome.

## 16. Failure behaviour and kill switch

| Failure | Behaviour |
| --- | --- |
| Provider timeout or 5xx | Job fails with retry; no partial output shown as complete |
| Invalid schema | Generation rejected; logged; user asked to retry |
| Low retrieval confidence | Honest refusal with a suggestion to upload better material |
| Spend cap reached | Generation paused with a reset time; study features unaffected |
| Suspected injection | Request refused and logged; user notified generically |
| Provider incident | Global kill switch disables AI; the product remains usable |

## 17. Decisions and remaining questions

| Question | Decision |
| --- | --- |
| Provider and model with training prohibition | **Open** — `KAB-003`; blocks beta |
| Per-user generation quota | 20 jobs per user per day, 200 per month; provisional until provider pricing is known (D8) |
| Filipino-language generation | English output in beta; Filipino source passages are quoted, not paraphrased |
| Who reviews AI content | The repository owner until a curator is appointed; same rule as content review (D3) |
| Retention of unverified private items | Kept until the source material or account is deleted; no automatic expiry in beta |
| Consent before first upload | Privacy notice plus an explicit acknowledgement at first upload |

Remaining unknowns: provider terms, real cost per generation, and review volume at
beta.

## 18. Traceability

| Policy area | Requirements |
| --- | --- |
| Grounding and attribution | AI-03, AI-04, QST-02 |
| Review boundary | AI-05, AI-10 |
| Validation | AI-06 |
| Cost and quotas | AI-07, NFR-COST-01..03 |
| Privacy | NFR-SEC-08, NFR-SEC-06 |
| Evaluation gates | AI-12 |
| Kill switch | AI-11 |
| Disclosure | AI-04, NFR-UX-02 |
