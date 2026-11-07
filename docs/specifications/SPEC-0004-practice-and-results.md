# SPEC-0004: Practice & Results

**Status:** Draft
**Owner:** Backend / Frontend
**Ticket:** KAB-104
**Related ADRs:** ADR-0003, ADR-0004, ADR-0007
**Approved by:** —
**Approved on:** —
**Last updated:** 2026-11-07

## 1. Problem

Learners need a safe, self-contained practice loop: start a set, answer, save
answers, submit (timed or untimed), receive results, and retain history. The
snapshot behaviour (ADR-0007) must preserve the attempt even if content changes
later.

## 2. Goals

- Start untimed or timed practice sessions from a topic, subject, or full exam.
- Answers are saved per attempt, survive refresh, and are safe to retry.
- Submitting is idempotent; results computed once and stored.
- Timed sessions: server-recorded deadline; auto-submit at expiry; client clock
  not trusted; answers after deadline rejected.
- Results show score, per-item correctness, explanation, provenance; score is
  labelled an estimate, not an official rating.
- Attempts snapshot question content at session start (ADR-0007).

## 3. Non-goals

- Adaptive item selection (later).
- Per-item immediate feedback.
- Pause control (refresh-based resume only, post-MVP).
- Full mock exam simulation with section timing (later).
- Predicted pass rate or official rating prediction.

## 4. Users and permissions

| Role | Can do | Cannot do |
| --- | --- | --- |
| Learner | Start sessions; save answers; submit; view own results/history. | Submit for others; delete others’ attempts. |
| Curator | See aggregate counts only; no per-attempt content in MVP. |
| Admin | Review moderation only; no practice content in MVP. |

## 5. User flows

### 5.1 Untimed practice flow

1. Learner chooses subject/topic → starts untimed set (default size 20).
2. Client loads session items (snapshot); answers saved as they change; survive refresh.
3. Learner submits; unanswered items counted wrong and listed.
4. Results: score, per-item correctness, correct answer, explanation, provenance.
5. Learner views results, can flag item, or practise weak topic.

### 5.2 Timed practice flow

1. Learner starts timed set; server records deadline (`started_at + time_limit_seconds`).
2. Client shows countdown from server deadline; answers after deadline rejected with `409 session_expired`.
3. On expiry, attempt auto-submits (unanswered items count wrong).
4. Client clock is display-only; server is authoritative.

### 5.3 Resume

- After refresh while session is `in_progress`, session state restored from server.
- Resume allowed only if status is `in_progress`.
- Timed attempt resumed after expiry auto-submits with saved answers.

## 6. Behaviour

- **Session lifecycle:** `in_progress → submitted | expired | abandoned`.
- **Timed expiry:** server checks at submit time; auto-submit job or check-on-submission path. The client deadline is display-only.
- **Submit idempotency:** `POST /practice-sessions/{id}/submit/` returns the existing result with 200 if already submitted.
- **Answers:** saved via `PUT /practice-sessions/{id}/answers/{position}/`; idempotent upsert; blocked after deadline with 409.
- **Scoring:** computed once at submission, stored; results never recompute from live questions.
- **Snapshot:** `SessionItem` copies question content (stem, options, correct answer, explanation, provenance, difficulty) at session creation (ADR-0007).

## 7. Data requirements

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `practice_session.id` | UUID | Yes | |
| `practice_session.user_id` | UUID | Yes | FK user; cascade on delete |
| `practice_session.exam_version_id` | UUID | Yes | FK exam_version (historical attempts keep version) |
| `practice_session.mode` | varchar | Yes | untimed, timed |
| `practice_session.status` | varchar | Yes | in_progress, submitted, expired, abandoned |
| `practice_session.time_limit_seconds` | int | Nullable | Snapshot of timed limit (untimed = null) |
| `practice_session.started_at` | timestamptz | Yes | |
| `practice_session.expires_at` | timestamptz | Nullable | timed only |
| `practice_session.submitted_at` | timestamptz | Nullable | |
| `practice_session.score_correct` | int | Nullable | |
| `practice_session.score_total` | int | Nullable | |
| `session_item.id` | UUID | Yes | |
| `session_item.session_id` | UUID | Yes | FK session |
| `session_item.position` | int | Yes | |
| `session_item.question_id` | UUID | Yes | FK live question (reporting); snapshot content separate |
| `session_item.snapshot_stem` | text | Yes | Snapshot per ADR-0007 |
| `session_item.snapshot_options` | jsonb | Yes | Snapshot of options: `[{id, text, is_correct}]` |
| `session_item.snapshot_explanation` | text | Yes | |
| `session_item.snapshot_provenance` | text | Yes | |
| `session_item.snapshot_difficulty` | smallint | Yes | |
| `attempt_answer.session_item_id` | UUID | Yes | Unique |
| `attempt_answer.selected_option_id` | UUID | Nullable | |
| `attempt_answer.is_correct` | bool | Nullable | Computed on submit |
| `attempt_answer.answered_at` | timestamptz | Yes | |

## 8. API contract

| Method | Path | Auth | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| POST | `/practice-sessions/` | Session | `{topic: UUID?, subject: UUID?, exam_version: UUID?, mode: untimed\|timed, size: int}` | `{session}` | 400, 401 |
| GET | `/practice-sessions/{id}/` | Session | — | `{session, items: [{position, question: {...snapshot}, saved_answer}], expires_at?}` | 401, 403, 404 |
| PUT | `/practice-sessions/{id}/answers/{position}/` | Session | `{selected_option_id?}` | 204 | 401, 409 (session_expired), 404 |
| POST | `/practice-sessions/{id}/submit/` | Session | — | `{result: {score_correct, score_total, items: [...]}}` | 401, 409?no, 409? idempotency |
| GET | `/practice-sessions/{id}/results/` | Session | — | `{result}` | 401, 404 |
| GET | `/practice-sessions/` | Session | `page` | `[{session, status, score, mode}]` | 401 |

## 9. UI requirements

**Screens and states:**

- **Start set:** choose topic (or subject/exam) → size selector (1–50, validated server-side, default 20).
- **Session screen:** list of items in snapshot; answers saved as selected (not revealed before submit); countdown display; save indicator.
- **Submit:** confirm dialog; on submit show loading; results view.
- **Results:** score summary; per-item list: chosen vs correct; explanation; provenance; “Practise weak topic” CTA; flag item CTA.
- **History:** list of past sessions, newest first, paginated.

**Accessibility:** focus order, ARIA live for results; colour not sole indicator for correctness.

**Mobile:** 360 px width; countdown not overlapping controls; large answer buttons.

## 10. Edge cases

| Condition | Expected behaviour |
| --- | --- | --- |
| Start session with topic having no published items | 400 with friendly message; empty state in UI. |
| Start timed session with size > available | Use all available items; say so. |
| Submit after deadline | Auto-submit; answers received before deadline scored; after-deadline answers rejected and cannot change score. |
| Refresh mid-session (timed) | Restore items + saved answers; countdown continues from server deadline. |
| Submit twice | Second returns existing result (idempotent). |
| Answer save fails | Keep selection in UI as unsaved; retry with backoff; block submit until saved or explicitly confirmed. |
| Retire question after snapshot | Attempt keeps snapshot; result remains consistent. |
| Exam version change | Attempts stay on their version. |

## 11. Error states

| Condition | User-facing message | HTTP/status |
| --- | --- | --- |
| Validation error | “Please correct the highlighted fields.” | 400 |
| Unauthorized | “Please sign in to continue.” | 401 |
| Forbidden | “You don’t have permission to do that.” | 403 |
| Not found | “Practice session not found.” | 404 |
| Rate limited | “Too many attempts. Please wait X seconds.” | 429 |
| Session expired | “Your session expired. Please start a new practice.” | 409 |
| Server error | “Something went wrong. Please try again.” | 500 |

## 12. Analytics and observability

- **Events:** session_started, session_submitted, session_expired, answer_saved, result_viewed, session_abandoned.
- **Metrics:** session start→submit latency, auto-submit rate, error rate, snapshot integrity check.
- **Alerts:** no result lost after submission; duplicate submit rate low.

## 13. Security and privacy

- Answers scoped to session owner; learners cannot read others’ attempts (object-level auth).
- Results are estimates; no official rating claims.

## 14. Acceptance criteria

- [ ] Learner can start untimed and timed sessions.
- [ ] Answers saved per item and survive refresh.
- [ ] Submit is idempotent (second submit returns existing result).
- [ ] Timed sessions auto-submit at server deadline; answers after deadline rejected.
- [ ] Score computed once, stored, never recomputed.
- [ ] Results show explanation + provenance; score labelled estimate.
- [ ] Attempts snapshot question content (ADR-0007) with immutability tests.
- [ ] History paginated and owned by user.
- [ ] All endpoints tested: success, 400, 401, 403, 404, 409.
- [ ] Accessibility: labels, focus, ARIA live, colour not sole indicator.
- [ ] Snapshot tests: editing a question after an attempt does not change prior results.

## 15. Out of scope

- Adaptive item selection, per-item feedback, pause control, full mock exams, predictions.

## 16. Dependencies and risks

| Item | Type | Status |
| --- | --- | --- |
| ADR-0007 (snapshot) | Architecture | Approved 2026-11-07 |
| SPEC-0002 (topic data) | Spec | Draft |
| API contracts (api-contracts.md, planned) | Docs | To be written in Phase 3 |
| Error envelope from SPEC-0001 | Spec | Draft |

**Risks:**

- Auto-submit race condition (deadline hit during submit).
- Snapshot schema complexity (JSONB options).
- Idempotency key conflicts.

## 17. Rollout

- Feature flag: none.
- Migration: `practice_practice_session`, `practice_session_item`, `practice_attempt_answer` models.
- Backfill: none.
- Rollback: revert migration; sessions data must be handled carefully (see §18).

## 18. Open questions

1. Auto-submit mechanism: job vs. check-on-submit.
2. Score rounding and labelling (percentage vs raw).
3. How to handle timed sessions that expire while offline.

## 19. Approval

- **Status:** Draft — awaiting Phase 3 technical-plan final approval.
- **Related ADR:** ADR-0007 (Approved 2026-11-07) with approval condition about snapshots.
