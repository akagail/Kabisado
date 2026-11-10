# CSE Content Sourcing, Review, and Attribution Plan

**Status:** Draft — requires approval
**Owner:** Product / Content
**Last updated:** 2026-11-10
**Ticket:** KAB-004
**Related:** `docs/product/cse-exam-reference.md`, SPEC-0002, SPEC-0003

This plan defines where Kabisado's examination content comes from, how it is
reviewed, how provenance is recorded, and how it is corrected or retired. It is
an operations document: it constrains the question bank (KAB-103) but does not
write items.

**Approval:** the repository owner approves this plan. No shared item may be
published until this plan is `Approved`.

---

## 1. Source categories

Every item must belong to exactly one category, and the category determines
what evidence is required before publication.

| Category | What it covers | Allowed | Recorded evidence |
| --- | --- | --- | --- |
| **Official structure** | CSC bulletin coverage areas: subject and topic names | Yes — facts used to structure the catalogue | Exam version + source URL in `catalog_exam_version` |
| **Original authored** | Items written by Kabisado authors against the official coverage | Yes — the default source | Author, coverage topic, authoring date |
| **Licensed third-party** | Items from a reviewer or publisher under a licence or written permission | Only with recorded licence | Licence holder, instrument, territory, term, expiry, attribution text |
| **AI-assisted** | Items drafted by a model and finished by a human author | Yes, with disclosure and full human review | Model, prompt version, generation timestamp, reviewing curator |
| **User uploads** | A learner's own uploaded material (increment 2) | Processed only for that user | Uploader, retention policy; never republished |

### Prohibited

- Official CSC examination items, whether published, recalled, reconstructed, or
  "shared by someone who took the exam".
- Any item from a leaked test bank, a scanned reviewer of unknown origin, or a
  social-media post of exam content.
- Third-party content without a recorded licence or written permission.
- Content mirrored from a source that restricts copying, even if technically
  reachable.
- Content that suggests CSC affiliation, accreditation, or endorsement.

The prohibition on reproducing official items is not a quality preference; it is
a legal constraint recorded in `cse-exam-reference.md` §6 (R.A. 9416, CSC
announcement disclaimers).

---

## 2. The no-reproduction rule

**Rule:** Kabisado never stores, displays, or paraphrases an actual CSC
examination question.

Procedure applied to every submitted item:

1. The author states the source category. "Recalled from the exam" is not a
   valid answer and blocks submission.
2. If the item cites a third-party reviewer, the licence record must exist
   before the item enters review.
3. A reviewer checks the item against any cited source and confirms it is not a
   copy or close paraphrase of an official item.
4. If a reviewer recognises an official item, the item is rejected and the
   incident is recorded in the ticket that tracks content incidents.
5. Items are written as **original questions against a published coverage
   area**, not as reproductions of past exams.

A coverage area (for example "Word Analogy") is a fact and may be used freely.
An exam question about that coverage area is not.

---

## 3. Item schema and provenance record

The database enforces the structural fields (SPEC-0003). This plan defines the
authoring record that must be complete before an item can leave `draft`.

| Field | Required | Notes |
| --- | --- | --- |
| `topic_id` | Yes | Must belong to the exam version being authored for |
| `stem` | Yes | Self-contained; no reference to "the passage above" without the passage |
| Four choices | Yes | One correct; distractors plausible but unambiguously wrong |
| `explanation` | Yes | Why the answer is correct; may note why the best distractor is wrong |
| `difficulty` | Yes | 1–5, relative within the topic |
| `origin` | Yes | `human`, `ai_assisted`, `ai_generated` |
| `source_category` | Yes | One of §1 |
| `citation_url` | When required | Required for licensed third-party |
| `licence_id` | When required | Required for licensed third-party |
| `author_id` | Yes | The human accountable for the final text |
| `reviewer_id` | Yes at publish | Must differ from `author_id` |
| `reviewed_at` | Yes at publish | Set when published |
| `prompt_version`, `model`, `generated_at` | For AI-assisted | Stored with the generation record |

Attribution is structured data, not prose in the explanation field.

### Licence record

For licensed third-party material, record: rights holder, instrument (contract
or written permission) and its storage location, territory, permitted uses,
term and expiry, required attribution text, and the date verified. An expired
licence is a publication blocker, not a warning.

---

## 4. Review workflow

Roles, matching SPEC-0003 §4:

| Role | Responsibility | Cannot |
| --- | --- | --- |
| **Author** (curator) | Write items, map to a topic, complete the authoring record | Publish their own items |
| **Reviewer** (curator) | Check correctness, clarity, provenance, and duplication | Review their own items |
| **Editor** (owner or delegate) | Resolve disagreements, approve licences, own the quality bar | Bypass second review |

Flow:

```text
draft → in review → published
              └──→ draft (rejected with a reason)
published → retired (error, licence expiry, or takedown)
```

1. Author creates the item as `draft` with the full authoring record.
2. Author submits for review.
3. A different reviewer checks the item against the checklist in §5 and either
   publishes it or returns it to `draft` with a written reason.
4. Publishing records `reviewer_id`, `reviewed_at`, and an audit event.

**Second review is mandatory.** Self-review is prohibited in the product, so it
is prohibited in the process as well.

### Review checklist

An item is publishable only when all are true:

- [ ] The keyed answer is correct and unique.
- [ ] The explanation justifies the keyed answer.
- [ ] Distractors are wrong for a stated reason, not by trick wording.
- [ ] The language is plain, grammatical, and free of ambiguity.
- [ ] The item tests the mapped coverage area, not a neighbouring one.
- [ ] No official or leaked item is reproduced or closely paraphrased.
- [ ] The authoring record, including source category, is complete.
- [ ] No duplicate of an existing published item in the same topic.
- [ ] No unnecessary personal data or third-party trademark.
- [ ] Formatting renders correctly on a narrow screen.

---

## 5. Quality bar and rejection criteria

Reject immediately when:

- The correct answer depends on a contested interpretation.
- More than one choice is defensible.
- The explanation is missing or only restates the answer.
- The item reproduces or closely paraphrases exam or licensed content without
  rights.
- The provenance record is incomplete.
- The item cannot be mapped to a published coverage area.

**Recommendation:** keep a rejected-item log with the reason. Patterns in
rejections (for example "ambiguous quantifiers") drive author coaching and are
more useful than the rejection count itself.

---

## 6. Volume plan for increment 1

The roadmap sets a reviewed-content gate before the private alpha. The working
number is **300 reviewed CSE Professional items** (roadmap; MVP scope F-list).

**Recommendation:** distribute the initial 300 across the seeded Professional
topics, weighted by the number of official coverage areas per subject rather
than by guessed item counts (the CSC publishes no item distribution for the 2027
version):

| Subject | Topics | Suggested share | Items |
| --- | --- | --- | --- |
| General Information | 4 | 20% | 60 |
| Verbal Ability | 6 | 33% | 100 |
| Numerical Ability | 3 | 20% | 60 |
| Analytical Ability | 4 | 27% | 80 |
| **Total** | **17** | **100%** | **300** |

Every topic needs at least 10 published items before it can be offered as a
practice set, so a topic is either "ready" or hidden rather than half-populated.

**Assumption:** 300 items is enough for a private alpha and not enough for a
public launch. A public release needs a larger pool to avoid repeat exposure.

**Needs approval:** whether Subprofessional content is authored before or after
the Professional alpha. The catalogue is seeded for both, but the increment 1
gate only names Professional.

---

## 7. AI-assisted authoring

- The model runs only through the adapter in `apps/ai/` (ADR-0005); no provider
  SDK is called from content tooling.
- Every AI-assisted item stores the model, prompt version, and generation
  timestamp, and is marked `ai_assisted` or `ai_generated`.
- AI output is treated as untrusted input: it goes through the same review and
  the same second-reviewer rule as human content.
- AI-generated items may not enter the shared pool without a human author and a
  human reviewer. Unreviewed generation stays private to the requesting user.
- Prompts never contain exam items, uploaded documents from other users, or
  personal data.
- A sample of AI-assisted items is re-checked each cycle for factual drift, even
  after publication.

---

## 8. Flags, corrections, and takedown

1. A learner flags an item with a reason category and optional note (SPEC-0003).
2. The reviewer triages within **two working days** for correctness flags and
   **one working day** for rights or legal flags.
3. Correctness fix: edit the item, keep the previous version in the audit trail,
   notify the reporter.
4. Wrong key or unusable item: retire it immediately; attempts already recorded
   keep their historical result and are excluded from new practice sets.
5. Rights complaint: unpublish the item immediately, record the complaint and
   the licence position, and do not republish until the editor approves.
6. Every resolution records who decided, when, and why.

**Takedown contact:** the repository owner is the initial accountable contact
until a support process exists.

---

## 9. Operations

| Item | Decision |
| --- | --- |
| Accountable content reviewer | Repository owner (confirmed as initial alpha curator, 2026-11-07) |
| Authoring cadence | Not committed; depends on curator capacity (**Needs approval**) |
| Review sampling | 100% before first publication; after that, re-check 10% of newly published items per week for consistency |
| Tracking | One row per item in the authoring sheet, mirrored into the question bank; the database is authoritative after publication |
| Reporting | Weekly count of published, in review, retired items per topic, against the §6 gate |

**Recommendation:** keep the authoring sheet as an input only. Once an item is
published, the database record is the single source of truth; do not maintain two
editable copies.

---

## 10. Risks and open decisions

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Curator capacity is one person | Alpha gate slips | Author in small batches; track weekly count |
| Ambiguous item keys | Learner distrust | Second review; flag loop; retire quickly |
| Licensed content expires silently | Legal exposure | Licence expiry is a publication blocker; review licences quarterly |
| AI-assisted items look authoritative | Misinformation | Disclosure, human review, sampling |
| Bulletin change mid-authoring | Items map to the wrong version | Items bind to an `ExamVersion`; new bulletin means new version |

**Needs approval:**

1. Curator capacity and a weekly authoring commitment, or a second curator.
2. Whether Alpha content includes Subprofessional items.
3. Budget and approval path for any licensed third-party material.
4. The final definition of "reviewed" for the 300-item gate (published and
   second-reviewed, or published only).

---

## 11. How this unblocks KAB-103

KAB-103 implements the question bank: models, review states, admin, and the
authoring API. It needs three decisions this plan supplies:

1. **Required fields at publish** — §3 and SPEC-0003 agree on the provenance
   fields, so the model and serializers have a fixed contract.
2. **Review states and the self-review prohibition** — §4 maps directly onto
   `draft → in_review → published → retired`.
3. **The no-reproduction rule** — KAB-103 can reject submissions that do not
   declare a valid source category instead of discovering the problem at review.

KAB-103 can start once this plan is `Approved`; the item bank itself can be
authored in parallel with implementation.

---

## 12. References

- `docs/product/cse-exam-reference.md` — verified coverage and copyright rules
- `docs/specifications/SPEC-0002-cse-catalogue.md` — taxonomy items map to
- `docs/specifications/SPEC-0003-question-bank-and-review.md` — states, roles,
  review endpoints
- `docs/product/roadmap.md` — 300-item alpha gate
- `docs/engineering/security-guidelines.md` — untrusted input and PII rules
