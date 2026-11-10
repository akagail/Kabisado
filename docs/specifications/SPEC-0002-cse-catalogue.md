# SPEC-0002: CSE Catalogue

**Status:** Approved
**Owner:** Backend / Frontend
**Ticket:** KAB-102
**Related ADRs:** ADR-0002, ADR-0003, ADR-0004, ADR-0005
**Approved by:** Repository owner
**Approved on:** 2026-11-07
**Last updated:** 2026-11-07

## 1. Problem

Users need a predictable, authoritative examination structure that aligns with
the official CSE bulletin. The catalogue must reflect the official subjects and
topics exactly, enabling learners to know what they should know and to locate
practice items by the same classification.

## 2. Goals

- Expose the CSE Professional exam structure (`General Information`, `Verbal`,
  `Numerical`, `Analytical`) as an official catalogue.
- Subprofessional exposes (`General Information`, `Verbal`, `Numerical`, `Clerical`).
- Subjects are scoped to an exam version; topics scoped to a subject.
- Support a single exam version (2027 bulletin) in the MVP, enabling future version
  migration without rewriting data.
- All catalogue items are read-only for learners.
- Expose a weak-topic status per topic with attempt count.

## 3. Non-goals

- Other exam families (PRC, UPCAT, etc.).
- Dynamic or learner-created topics.
- External material discovery.
- Mobile-only or brand-new taxonomy.

## 4. Users and permissions

| Role | Can do | Cannot do |
| ---Ϡ–¿–| --- | --- |
| Learner (authenticated) | View all catalogue; see own accuracy and weak-topic status per topic; start practice per topic. | See exam version details; edit catalogue. |
| Content curator (staff) | Edit subject, topic; create or retire questions per topic. | Access learners' practice answers or uploaded material. |
| Admin | Everything staff can do, plus suspend users and manage staff. | See anything beyond moderation audit. |

## 5. User flows

### 5.1 Browse catalogue (first visit)

1. Learner with profile chooses exam family → Exams → CSE Professional.
2. The catalogue shows subjects in official order.
3. Click a subject → see its topics, each with accuracy and attempts.
4. Choose a topic with published items → Start practice.

### 5.2 Progress-visible catalogue

1. On subject/topic views, learners see their own accuracy (e.g. `Numerical — 80% (6 attempts)`).
2. Topics with low attempts or poor accuracy are marked weak, with a count.
3. Weak topics are labelled with the rule (“≤3 attempts and ≤70% accuracy”) and link to practice.
4. Changing target exam reloads the catalogue; past attempts stay with their exam version.

## 6. Behaviour

- **Exam family:** always `Civil Service` in the MVP; slug `cse`.
- **Exam level:** `professional` or `subprofessional`.
- **Exam version:** points to the official 14 March 2027 bulletin (`slug: "2027-bulletin"`).
- **Subjects and topics are version-scoped:** they are imported once per exam version.
- **Everything in catalogue is immutable.** Content curators can edit subjects/topics only in the admin; they cannot edit them via UI.
- **Weak-topic rule:** an item is weak if `attempts ≥ 3` and `accuracy < 70%`.
- **API exposes per-user accuracy:** computed from `PracticeResponse` per `Topic`.

## 7. Data requirements

| Field | Type | Required | Validation | Notes |
| --- | --- | --- | --- | --- |
| `catalog_exam_family.id` | UUID | Yes | Unique, slug unique, immutable after seeding. |
| `catalog_exam.id` | UUID | Yes | Unique, slug unique, `family_id` FK. |
| `catalog_exam_version.id` | UUID | Yes | Unique, `exam_id` FK, immutable. |
| `catalog_exam_version.source_url` | text | Yes | Official CSC announcement URL. |
| `catalog_exam_version.published_at` | date | Yes | Match source. |
| `catalog_subject.id` | UUID | Yes | Unique, `exam_version_id` FK. |
| `catalog_subject.slug` | varchar | Yes | Unique per version, used for SEO and matching. |
| `catalog_subject.name` | varchar | Yes | As in official bulletin. |
| `catalog_subject.display_order` | int | Yes | Ordering from source; applies within version. |
| `catalog_topic.id` | UUID | Yes | Unique, `subject_id` FK, optional `parent_id` self-FK. |
| `catalog_topic.slug` | varchar | Yes | Unique within its parent (subject) and version. |
| `catalog_topic.name` | varchar | Yes | As in official bulletin. |
| `catalog_topic.display_order` | int | Yes | Ordering within subject. |

**Retention and seeding:**

- Catalogue never changes after the initial import (MVP). Moving to a new version will add a new `ExamVersion` row with its own subjects/topics; past attempts stay with their version.
- The exam version displays its source URL and publication date.

## 8. API contract

| Method | Path | Auth | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| GET | `/exams/` | Session | — | `{exam_families: [{id, slug, name, exams: [{id, slug, name, level}]}]}` | 401 |
| GET | `/exam-versions/{id}/subjects/` | Session | — | `[{id, slug, name, display_order}]` | 401, 404 |
| GET | `/subjects/{id}/topics/` | Session | — | `[{id, slug, name, display_order, accuracy?, attempts?}]` | 401, 404 |
| GET | `/topics/{id}/` | Session | — | `{id, slug, name, display_order, accuracy?, attempts?, weak-topic?}` | 401, 404 |

**Error envelope:** see SPEC-0001.

## 9. UI requirements

**Screens and states:**

- `/exams/` — dropdown/rail of exam families, with their exams. Selecting an exam loads the subjects screen.
- `/subjects/{id}/` — list of topics in the selected exam version; each row shows name, accuracy (if data exists), and attempt count.
- `/topics/{id}/` — topic detail, with a large start-practise button and weak-topic badge if applicable.
- **Accessibility:** labels, visible focus, ARIA live for toasts, keyboard navigable. Topic rows are touch targets ≥44px.
- **Mobile:** catalog uses vertical stacking; weak-topic list is a card per topic.

## 10. Edge cases

| Condition | Expected behaviour |
| --- | --- |
| Exam version has no subjects (should not happen) | Empty state with a link to the exam page. |
| Subject has no topics (data inconsistency) | Skip in UI; system logs an error. |
| Changing target exam while on a topic page | Redirect to the new catalogue root. |
| No weak topics | Empty state on the topic view (“You are strong here! Start a review session.”). |
| Catalog version mismatch (e.g. two exams with same slug) | Fail the import and require human review. |

## 11. Error states

| Condition | User-facing message | HTTP/status |
| --- | --- | --- |
| Validation error | “Please select a different topic.” | 400 |
| Unauthorized | “Please sign in to continue.” | 401 |
| Forbidden | “You cannot access this subject.” | 403 |
| Not found | “Subject not found.” | 404 |
| Rate limited | “Too many requests. Please wait X seconds.” | 429 |
| Server error | “Something went wrong. Please try again.” | 500 |

## 12. Analytics and observability

- **Events (no PII):** catalogue_view, subject_view, topic_view, weak_topic_view, accuracy_changed.
- **Metrics:** catalogue page load time, weak-topic usage rate.
- **Alerts:** no catalogue items missing in production, zero accuracy without attempts.

## 13. Security and privacy

- Every query filters by `request.user`; users can only access their profile's exam version scope.
- Public catalogue is accessible only through authentication; catalogue metadata is not hidden from staff.
- Staff can view catalogue usage but cannot edit the official source.

## 14. Acceptance criteria

- [ ] Exam families and exams expose `/exams/` (CSE only).
- [ ] Subjects and topics are seeded from `cse-exam-reference.md`.
- [ ] Weak-topic computation matches rule (≤3 attempts, ≤70% accuracy).
- [ ] `/subjects/{id}/topics/` shows per-user accuracy and attempt count.
- [ ] `/topics/{id}/` marks weak topics with badge and count.
- [ ] Changing target exam reloads catalogue and preserves history.
- [ ] All endpoints have tests for success, 401, 404.
- [ ] Accessibility: focus visible, labels present, screen-reader friendly.
- [ ] OpenAPI schema generated and matches implementation.

## 15. Out of scope

- Other exam families, external discovery, dynamic topics.
- Edit subjects/topics via UI (admin only).
- Public catalogue without login.

## 16. Dependencies and risks

| Item | Type | Status |
| --- | --- | --- |
| Exam reference document | Specification | Draft, verified with CSC bulletin |
| ADR-0004 (session auth) | Architecture | **Proposed** — needs security design review |
| Content seeding execution (KAB-004) | External work | Not started; 300 items gate |
| Database schema (catalog tables) | Schema | Requires SPEC-0002 acceptance |
| Provider-independent AI (O1) | External | Pending selection; not used in MVP |

**Risks:**

- Importing wrong subjects/topics due to ambiguous bulletin language.
- Weak-topic rule feels arbitrary to learners; document with examples.
- Target exam change without data migration.

## 17. Rollout

- Feature flag: none (core MVP).
- Migration: `catalog_exam_family`, `catalog_exam`, `catalog_exam_version`, `catalog_subject`, `catalog_topic` models + migration.
- Backfill: none.
- Rollback: revert migration; enrolment data unaffected.

## 18. Open questions

1. Exact width of catalogue entries on mobile.
2. Slug uniqueness guarantee in the import script.
3. Whether to pre-seed Subprofessional subjects immediately (requires content).
4. If weak-topic badge should be shown in the catalogue or only on the topic detail.

## 19. Implementation notes — KAB-102 (2026-11-10)

Approved deviations recorded during implementation:

1. **Accuracy, attempts, and weak-topic are stubbed.** No practice responses
   exist until KAB-104, so the topic endpoints return `accuracy: null`,
   `attempts: 0`, `weak_topic: false`. The weak-topic rule is unchanged and is
   implemented with KAB-104/KAB-105. §14's weak-topic criteria therefore remain
   open against this ticket.
2. **`/exams/` returns `current_version`** per exam (additive). The contract in
   §8 gave the client no way to obtain an `ExamVersion` id, which
   `/exam-versions/{id}/subjects/` requires.
3. **Exam slugs are `cse-professional` and `cse-subprofessional`**; the level is
   a separate `level` field (`professional` / `subprofessional`). The profile
   request accepts the exam slug and the response returns
   `{id, slug, name}`, matching the `target_exam` object shape in SPEC-0001 §8.
4. **`ExamVersion` gains `slug` and `accessed_at`.** §6 names a version slug
   (`2027-bulletin`) while the database design only had `label`; both are kept.
   `accessed_at` records when the bulletin was verified.
5. **Item count and time limit stay null** for the 2027 bulletin because the CSC
   announcement does not publish them (see `cse-exam-reference.md` §5).
6. **Seeding is a management command**, not a data migration:
   `manage.py seed_cse_catalogue`. It is idempotent and refuses to run outside
   `DEBUG` without `--force`. The migration only creates the two `Exam` rows the
   profile FK needs.
7. **"Attempts reference an immutable exam version"** cannot be verified until
   practice sessions exist (KAB-104); the schema supports it, the test does not
   yet.