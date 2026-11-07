# SPEC-0005: Progress Analytics & Weak Topics

**Status:** Draft
**Owner:** Backend / Frontend
**Ticket:** KAB-105
**Related ADRs:** ADR-0003, ADR-0007
**Approved by:** —
**Approved on:** —
**Last updated:** 2026-11-07

## 1. Problem

Learners need clear visibility of what they know and what they need to study, so they can focus effectively. Progress should be computed reliably, using only submitted attempts and aligned with the rule-based weak-topic diagnosis from SPEC-0004.

## 2. Goals

- Accuracy computed per topic across submitted attempts only.
- Weak-topic rule: ≤3 attempts and ≤70% accuracy, with rule and attempt count visible.
- Learners see accuracy by subject and topic; weak-topic list with CTA to practise.
- History of recent attempts, newest first, paginated.
- Analytics endpoints scoped to the signed-in user only.
- No AI-based predictions; rule-based for MVP.

## 3. Non-goals

- Model-based diagnosis or personal study plans.
- Cohort or comparative analytics.
- Recommendations beyond "practise the weak topic”. 
- Tie-ins with external data.

## 4. Users and permissions

| Role | Can do | Cannot do |
| --- | --- | --- |
| Learner | View own analytics; see weak-topic list; access history; click to practice. | See other users' progress. |
| Curator | See aggregate counts (if required later) but not individual; manage content only. |

## 5. User flows

### 5.1 Dashboard view

1. Learner lands on catalogue home; sees quick summary: "Continue practising Numeric (80% | 6 attempts)".
2. Below, weak topics are listed: each with rule, attempt count, and "Practise".
3. Past sessions appear as card rows; can click to view full results.

### 5.2 History details

1. Click a session → full results view.
2. Return to progress page after viewing.

## 6. Behaviour

- **Accuracy:** computed from `PracticeResponse` where `is_correct = TRUE` across submitted attempts. Formula: `correct / total * 100`.
- **Attempt count:** number of distinct topics attempted, based on submissions only.
- **Weak-topic rule:** applied per topic: if `attempts ≥ 3` AND `accuracy < 70%`.
- **Topic visibility:** only topics for which the user has submitted attempts.
- **API: one endpoint for both subject- and topic-level analytics**: `/analytics/summary/` for subject-level; `/analytics/topics/` for topic-level.
- **Authorization:** every query includes `WHERE user_id = request.user_id`.

## 7. Data requirements

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `analytics_summary.id` | UUID | Yes | (or view, derived) |
| `analytics_summary.user_id` | UUID | Yes | |
| `analytics_summary.topic_id` | UUID | Yes | |
| `analytics_summary.subject_id` | UUID | Yes | |
| `analytics_summary.attempts` | int | Yes | |
| `analytics_summary.correct` | int | Yes | |
| `analytics_summary.accuracy` | numeric(5,2) | Yes | computed: `(correct * 100) / attempts` |
| `analytics_summary.last_practiced_at` | timestamptz | Yes | |
| `analytics_summary.updated_at` | timestamptz | Yes | |
| `analytics_topic_view.id` | UUID | Yes | (or view, derived) |
| `analytics_topic_view.user_id` | UUID | Yes | |
| `analytics_topic_view.topic_id` | UUID | Yes | |
| `analytics_topic_view.accuracy` | numeric(5,2) | Yes | |
| `analytics_topic_view.attempts` | int | Yes | |
| `analytics_topic_view.weak_topic` | bool | Yes | computed from rule |
| `analytics_topic_view.weak_reason` | varchar | Yes | "based on ≤3 attempts and ≤70% accuracy" |

## 8. API contract

| Method | Path | Auth | Request | Response | Errors |
| --- | --- | --- | --- | --- | --- |
| GET | `/analytics/summary/` | Session | — | `[{subject: {id, slug, name, accuracy, attempts}}]` | 401 |
| GET | `/analytics/topics/` | Session | — | `[{topic: {id, slug, name, accuracy, attempts, weak_topic?}}]` | 401 |

**Error envelope:** see SPEC-0001.

## 9. UI requirements

**Screens:**

- **Progress page:** cards per subject with accuracy and attempt count; list of weak topics below.
- **Weak-topic row:** badge with attempt count; disabled accuracy line.
- **History panel:** table of recent sessions: date, mode, score estimate, weak topics count.

**Accessibility:** labels, screen-reader order; weak topic label includes the rule text.

**Mobile:** 360 px width; subject cards vertical; weak topics are inline chips.

## 10. Edge cases

| Condition | Expected behaviour |
| --- | --- |
| No submitted attempts | Empty state: "Start practising with a topic.” |
| Only 1 or 2 attempts | No weak-topic label; accuracy visible. |
| Accuracy 70% exactly | Not weak (≤70%, not <70%). |
| Changing target exam | Progress scoped to that exam version; cross-exam history hidden. |
| Deleting account | All analytics rows deleted or anonymized (user FK to NULL).

## 11. Error states

| Condition | User-facing message | HTTP/status |
| --- | --- | --- |
| Validation error | “Please select a different topic.” | 400 |
| Unauthorized | “Please sign in to continue.” | 401 |
| Forbidden | “You cannot access this data.” | 403 |
| Server error | “Something went wrong. Please try again.” | 500 |

## 12. Analytics and observability

- **Events:** analytics_view, weak_topic_view, subject_accuracy_change.
- **Metrics:** time to compute accuracy, weak-topic list generation, empty-state rate.
- **Alerts:** no data leak; accuracy computation stable.

## 13. Security and privacy

- Object-level auth: user analytics rows filtered by `user_id`.
- No PII in analytics data.
- Delete cascade for account.

## 