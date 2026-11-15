# SPEC-0003: Question Bank & Review

**Status:** Approved
**Owner:** Backend / Frontend / Product
**Ticket:** KAB-103
**Related ADRs:** ADR-0003, ADR-0004
**Approved by:** Repository owner
**Approved on:** 2026-11-07
**Last updated:** 2026-11-07

## 1. Problem

Learners practise trustworthy material that is verified, explained, and traceable. Content curators need a simple draft → review → publish workflow so the question bank grows safely without any one person publishing unreviewed items.

## 2. Goals

- Multiple-choice items with one correct answer, explanation, and provenance.
- Items live in `draft → in review → published → retired` states.
- Publishing requires a reviewer other than the author and records an audit entry.
- Items are linked to topics (never directly to exam version).
- Learners flag items with reasons; staff see a queue and can resolve or retire.
- Retired items stay visible in historical results but are removed from new sets.
- No AI-generated content in the MVP.

## 3. Non-goals

- Bulk import of items.
- Question variants or distractor rationales.
- Community contributions.
- AI question generation (increment 2).
- Item-level immediate feedback (i.e., per-item reveal during practice).

## 4. Users and permissions

| Role | Can do | Cannot do |
| --- | --- | --- |
| Learner | Practise published items; flag items with a reason category; see published items in sets. | See draft/review items; create items; see other users' flags. |
| Curator (staff) | Author drafts; review others' drafts; publish; retire items; resolve flags. | Publish their own items without review. |
| Admin | Everything staff can do, plus suspend users. | See learners' practice answers beyond moderation audit. |

## 5. User flows

### 5.1 Content curator flow

1. Curator creates a draft item: selects topic, stem, options, correct answer, explanation, provenance.
2. Curator submits for review; item enters `in review`.
3. Another curator reviews and either approves (`published`) or rejects (`in review` with reason).
4. Publishing records an audit entry.
5. Curator retires an item if an error is found; item removed from new sets, kept in results.
6. Staff open the flag queue and resolve flags (dismiss, retire question).

### 5.2 Learner flagging flow

1. Learner sees a result item.
2. Learner clicks flag and chooses a reason category; optional note.
3. Flag is stored; staff see it in the admin queue.
4. Staff resolve the flag with a note and decision; resolution is recorded and audit-logged.

## 6. Behaviour

- **Lifecycle:** `draft → in review → published → retired`. Drafts and `in review` items are not visible in practice sets.
- **Provenance:** either an external citation URL or an authoring record (author, coverage area, review date).
- **Publishing rule:** only items with an explanation and provenance can be published.
- **Self-review is prohibited:** a curator cannot publish their own item.
- **Retire keeps history:** practice attempts that snapshotted a retired question keep their snapshot.
- **Uniqueness:** exactly one correct option per question, enforced service-side and by partial unique index.
- **No duplicates:** flagging the same item twice by the same user merges into one flag.

## 7. Data requirements

| Field | Type | Required | Validation | Notes |
| --- | --- | --- | --- | --- |
| `question.id` | UUID | Yes | Unique | Immutable after publish |
| `question.topic_id` | UUID | Yes | FK to catalog_topic | Version-scoped via topic |
| `question.stem` | text | Yes | Required | Question text |
| `question.explanation` | text | Yes | Required if published | “Why the key is correct and main distractor wrong” |
| `question.provenance` | text | Yes | Required if published | External citation or authoring record |
| `question.difficulty` | smallint | Yes | 1–5 | 1 = easiest |
| `question.status` | varchar | Yes | Choices: draft, in_review, published, retired | Default draft |
| `question.author_id` | UUID | Yes | FK to User | Auto-set on create |
| `question.reviewer_id` | UUID | Nullable | FK to User | Set on review; ≠ author |
| `question.reviewed_at` | timestamptz | Nullable | | |
| `created_at, updated_at` | timestamptz | | | |
| `option.id` | UUID | Yes | Unique | |
| `option.question_id` | UUID | Yes | FK | |
| `option.text` | text | Yes | | |
| `option.is_correct` | bool | Yes | Exactly one true per question | |
| `option.rationale` | text | Yes | | Why correct/wrong |
| `option.display_order` | int | Yes | | |
| `content_flag.id` | UUID | Yes | Unique | |
| `content_flag.question_id` | UUID | Yes | FK | |
| `content_flag.reporter_id` | UUID | Nullable | FK to User | Nullable per retention |
| `content_flag.reason` | varchar | Yes | Category | Predefined categories |
| `content_flag.note` | text | Nullable | | Free text |
| `content_flag.status` | varchar | Yes | open, resolved, dismissed | Default open |
| `content_flag.resolved_by` | UUID | Nullable | FK to User | |
| `content_flag.resolved_at` | timestamptz | Nullable | | |
| `content_flag.resolution_note` | text | Nullable | | |

## 8. API contract

| Method | Path | Auth | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| POST | `/questions/` | Staff | `{topic, stem, options, correct_answer_index, explanation, provenance}` | `{question}` | 400, 401, 403 |
| POST | `/questions/{id}/submit-for-review/` | Staff | — | `{question, status}` | 400, 401, 403 |
| POST | `/questions/{id}/review/` | Staff | `{approve: boolean, reason?}` | `{question, status}` | 400, 401, 403 |
| POST | `/questions/{id}/retire/` | Staff | `{reason?}` | `{question, status}` | 400, 401, 403 |
| GET | `/topics/{id}/questions/` | Session | `size, page` | `[{question}]` | 401, 404 |
| POST | `/questions/{id}/flags/` | Session | `{reason, note?}` | `{flag}` | 400, 401, 409 |
| GET | `/admin/flags/` | Staff | — | `[{flag, reporter, question}]` | 401, 403 |

**Error envelope:** see SPEC-0001.

## 9. UI requirements

**Screens and states:**

- **Create item** (curator only): fields for topic, stem, options (at least 2), correct index, explanation, provenance; inline validation; “Submit for review”.
- **Item detail** (curator/admin): status badge, explanation, provenance, audit trail.
- **Review queue** (curator/admin): list of `in review` items with approve/reject and reason.
- **Flag queue** (curator/admin): list of open flags with question preview, reason, note; resolve actions.
- **Learner flag** (on results): reason radio, optional text, submit button.

**Accessibility:** labels, focus order, ARIA live for validation errors, keyboard navigable. Delete actions require confirmation dialogs.

**Mobile:** forms stack vertically; flag button is a full-width secondary action.

## 10. Edge cases

| Condition | Expected behaviour |
| --- | --- |
| Publish attempted without explanation/provenance | Block with field-level error |
| Curator submits their own item for review | Allowed but another curator must review; self-review prohibited |
| Reviewer approves with missing explanation | Validation rejects before state change |
| Retire item used by an active attempt | Allowed; attempt keeps its snapshot |
| Learner flags same item twice | One flag per user per question; update existing |
| Flagged item hidden from learner? | No — item remains visible; flag does not hide |
| Staff view another staff’s flag resolution | Visible in admin with actor and timestamps |

## 11. Error states

| Condition | User-facing message | HTTP/status |
| --- | --- | --- |
| Validation error | “Please correct the highlighted fields.” | 400 |
| Invalid credentials | “Invalid email or password.” | 401 |
| Account inactive | “This account is inactive.” | 401 |
| Rate limited | “Too many attempts. Please wait X seconds.” | 429 + Retry-After |
| Unauthorized | “Please sign in to continue.” | 401 |
| Forbidden | “You don’t have permission to do that.” | 403 |
| Not found | “Item not found.” | 404 |
| Server error | “Something went wrong. Please try again.” | 500 |

## 12. Analytics and observability

- **Events:** question_created, question_submitted_for_review, question_published, question_retired, flag_created, flag_resolved.
- **Metrics:** publish time (days from draft to publish), flag resolution time, rejected item count.
- **Alerts:** publish failure rate, item stuck in review > 7 days.

## 13. Security and privacy

- Object-level authorization: curators can edit only items they authored; review/publish/retire allowed for staff.
- Learners see only published items; drafts/review items are never exposed in practice sets.
- Learner identities in flags are not public; `reporter_id` can be NULL per retention rules.
- Audit entries record actor, action, object, change, timestamp — append-only.

## 14. Acceptance criteria

- [ ] Curator can create a draft item with topic, stem, options, correct answer, explanation, provenance.
- [ ] Draft item cannot be published without explanation and provenance.
- [ ] Publishing requires a reviewer other than the author.
- [ ] Published items appear in practice sets for their topic.
- [ ] Retired items are removed from new sets but remain in historical results.
- [ ] Learner can flag an item; staff see it in the queue.
- [ ] Flagging same item twice by same user produces one flag.
- [ ] Staff can resolve/dismiss flags with audit entry.
- [ ] All publish/retire/review actions are audited.
- [ ] All endpoints tested: success, 400, 401, 403, 404, 409.
- [ ] Accessibility: labels, focus, keyboard, ARIA live.

## 15. Out of scope

- AI generation and its review queue (increment 2).
- Bulk import, question variants.
- Community contributions.
- Public item library without auth.

## 16. Dependencies and risks

| Item | Type | Status |
| --- | --- | --- |
| SPEC-0002 (catalogue topics) | Spec | Draft; questions FK to topics |
| Topic data seeded | Data | Required before question creation |
| ADR-0007 (snapshot) | Architecture | Approved; affects sessions, not questions |
| 300 reviewed Professional items | Product goal | Content curation execution |
| Stored procedure/rules for exactly-one-correct | Backend | Enforced in service + partial unique index |

**Risks:**

- Self-review bypass if auditing not enforced at the service layer.
- Published items changing text after attempts (mitigated by ADR-0007 snapshots).
- Queue volume overwhelming a single curator at alpha.

## 17. Rollout

- Feature flag: none.
- Migration: `questions_question`, `questions_question_option`, `questions_content_flag` models.
- Backfill: none.
- Rollback: revert migration; catalogue and accounts unaffected.

## 18. Open questions

1. Maximum options per question (4 fixed in MVP).
2. Provenance URL validation (external citation format).
3. Whether staff can see flag reporter email in admin.
4. Difficulty scale semantics (1–5 vs 1–10).

## 19. Implementation notes — KAB-103 (2026-11-10)

Recorded during implementation. The default readings are the nearest approved
statement; anything still open is listed as deferred.

1. **Model/table naming.** The database design and this spec's acceptance
   wording use "choices"; the option table is `questions_choice` (model
   `Choice`). The API field remains `options` as written in §8.
2. **Flag field name.** `note` is implemented (§7). The database design
   previously called it `comment`; that document now says `note`.
3. **Duplicate detection.** `stem_hash` is a SHA-256 of the whitespace-collapsed,
   lower-cased stem, indexed. Duplicates are detectable but not blocked.
4. **Learner payload withholds answers.** `GET /topics/{id}/questions/` returns
   published items only and omits `is_correct`, `rationale`, `explanation`, and
   `provenance`. Staff create/review responses include them.
5. **Flag resolution path.** §8 lists no resolve endpoint, so staff resolve or
   dismiss flags from the Django admin flag queue. The service is audited, and
   the admin action is the only caller.
6. **Duplicate flags.** A second open flag by the same reporter returns `409`
   (§8 error list). A resolved flag allows a new report; the partial unique index
   covers open flags only.
7. **No content is seeded.** KAB-103 implements the bank and workflow only. The
   300-item gate and sample-content review wait for KAB-004 approval.
8. **Deferred acceptance criteria.** "Published items appear in practice sets"
   and "retired items remain in historical results" need KAB-104. The learner
   flag UI and its accessibility checks also need the KAB-104 results screen.
9. **Bulk import stays out.** §3 lists bulk import as a non-goal; the older
   ticket text that promised CSV/JSON import was corrected.
10. **Curator UI.** The curator workflow runs through the staff API and Django
    admin (review/flag queues). Dedicated frontend curator screens are not part
    of the KAB-103 issue scope.