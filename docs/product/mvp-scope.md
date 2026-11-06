# MVP Scope

**Status:** Proposed — requires approval (Phase 2, Checkpoint 3)
**Owner:** Product
**Last updated:** 2026-11-06

## 1. One definition of MVP

**The MVP is the CSE Professional core practice loop — account, catalogue,
reviewed question bank, untimed and timed practice, explanations, progress
analytics, and rule-based weak-topic diagnosis — released as a private alpha.**

| Release | Contents | Audience |
| --- | --- | --- |
| MVP (increment 1) | Features F1–F11 | Invited private alpha |
| Fast-follow beta (increment 2) | Personal materials, AI platform, AI study aids, flashcards | Public beta |
| Launch hardening (increment 3) | Verification, abuse controls, observability, backups, legal pages, accessibility audit, load test | Public availability |

If a capability is not in the F-list in §2, it is not in the MVP. Other documents
link here instead of restating scope.

**What the MVP proves**

- Learners return to practise, and explanations are used and rated helpful.
- Weak-topic diagnosis is understandable and leads to a next action.
- The loop is usable on a mid-range phone and a keyboard.

**What it does not prove**

- Willingness to upload personal reviewers or to pay.
- AI quality, cost, and review economics.
- Subprofessional demand.

**Recommendation (needs approval):** MVP = increment 1 only. The alternative —
increments 1 and 2 together — is rejected because it makes provider selection,
content licensing, and the AI review boundary, none of them approved, block the
first release.

## 2. MVP feature list

| ID | Feature | Priority | Requirements | Depends on | Ticket |
| --- | --- | --- | --- | --- | --- |
| F1 | Accounts | MUST | AUTH-01..04, AUTH-08 | — | KAB-101 |
| F2 | Profile and target exam | MUST | AUTH-05, CAT-03 | F1 | KAB-101, KAB-102 |
| F3 | CSE catalogue | MUST | CAT-01, CAT-02, CAT-04 | — | KAB-102 |
| F4 | Question bank and review | MUST | QST-01..03, ADM-01, ADM-02 | F3 | KAB-103 |
| F5 | Untimed practice | MUST | PRA-01, PRA-03, PRA-06 | F4 | KAB-104 |
| F6 | Timed practice | MUST | PRA-02, PRA-05 | F5 | KAB-104 |
| F7 | Results and explanations | MUST | PRA-04 | F5 | KAB-104 |
| F8 | Progress analytics | MUST | ANL-01..03 | F5, F7 | KAB-105 |
| F9 | Weak-topic diagnosis | MUST | ANL-04 | F8 | KAB-105 |
| F10 | Content flagging | MUST | QST-05 | F5 | KAB-103 |
| F11 | Account deletion and export | MUST | AUTH-08, NFR-SEC-07 | F1 | KAB-101 |

Cross-cutting MVP requirements: NFR-SEC-01..03, NFR-SEC-06; NFR-PERF-01,
NFR-PERF-02, NFR-PERF-05; NFR-REL-02, NFR-REL-04; NFR-UX-01..05; NFR-MNT-01..05.
Ticket: KAB-111 for the accessibility and performance baseline.

Journeys, error states, and edge cases per feature: [user-flows.md](user-flows.md).

### F1 — Accounts

**Purpose.** Let a learner own a persistent practice history securely.

**User story.** As a CSE candidate, I can create an account so my results and
progress are saved and private.

**Expected behaviour.** Register with email and password; log in and out; reset a
forgotten password through an emailed single-use link. Passwords are hashed with
a modern hasher, enforce a minimum length, and are checked against breached
password lists. Authentication errors are generic to avoid account enumeration;
authentication endpoints are rate-limited.

**Acceptance criteria.**

- Registration creates a session; a duplicate email is rejected with a generic
  message.
- A wrong password returns a generic error and is rate-limited.
- A reset link is single-use and expires; using it invalidates existing sessions.
- Logout invalidates the session server-side.
- No plaintext password is logged or stored.

**Out of scope.** Social login, SSO, magic links, MFA, email verification
(launch hardening).

### F2 — Profile and target exam

**Purpose.** Scope content to the learner's exam and remember their defaults.

**User story.** As a learner, I can set my target exam so I only see relevant
subjects.

**Expected behaviour.** Editable display name, target exam (Professional or
Subprofessional), and a preferred practice mode used as the default when
starting a set. Switching target exam changes the catalogue view but never
deletes history.

**Acceptance criteria.**

- Edits persist across sessions.
- Switching target exam does not delete or hide past attempts.
- Practice defaults follow the selected target exam and preference.

**Out of scope.** Avatar upload, public profiles, multiple simultaneous targets.

### F3 — CSE catalogue

**Purpose.** Structure content exactly as the official coverage defines it.

**User story.** As a learner, I can browse the subjects and topics of my exam
before practising.

**Expected behaviour.** `ExamFamily → Exam → ExamVersion → Subject → Topic`, seeded
from [cse-exam-reference.md](cse-exam-reference.md). Professional has General
Information, Verbal, Numerical, and Analytical; Subprofessional has General
Information, Verbal, Numerical, and Clerical. The exam version records its source
URL, publication date, and access date. Learners see read-only catalogue data.

**Acceptance criteria.**

- Seeded subjects and topics match the verified reference exactly; no invented
  topics.
- Subprofessional shows Clerical Ability and not Analytical Ability; Professional
  the reverse.
- Every topic belongs to a subject and an exam version.
- The exam version displays its official source.

**Out of scope.** Other exam families, external material discovery, learner-created
topics, COMEX variants.

### F4 — Question bank and review

**Purpose.** Supply original, reviewed items with explanations and provenance.

**User story.** As a content curator, I can author, review, and publish items so
learners practise trustworthy material.

**Expected behaviour.** Multiple-choice items with one correct answer, an
explanation, and provenance. Provenance is an external citation **or** an
authoring record (author, coverage area, review date). Items move through
`draft → in review → published → retired`; publishing requires a reviewer other
than the author and records an audit entry. Retired items leave new sets but
remain visible in historical results.

**Acceptance criteria.**

- An item cannot be published without an explanation and provenance.
- A published practice set contains only published items for the target topic.
- Retiring an item removes it from new sets and keeps it in past results.
- Every publish, retire, and edit action is audited with actor, time, and change.

**Out of scope.** AI generation and its review queue (increment 2), bulk import,
question variants, distractor rationales, community contributions.

### F5 — Untimed practice

**Purpose.** Practise a chosen topic without time pressure.

**User story.** As a learner, I can practise a subject or topic and check my
answers when I submit.

**Expected behaviour.** Choose subject/topic and set size (default 20). No timer.
Answers are saved per attempt and survive a refresh. Submitting shows results;
the submission is idempotent.

**Acceptance criteria.**

- A set contains only published items in the chosen topic, up to the requested
  size.
- Answers survive a page refresh before submission.
- Submitting twice produces one attempt and one result.
- An empty topic shows an empty state with a next action, not an error.
- Requested size is bounded and validated server-side.

**Out of scope.** Adaptive item selection, per-item immediate feedback, an
explicit pause control (refresh-based resume only), full mock exams.

### F6 — Timed practice

**Purpose.** Practise under exam-like time pressure.

**User story.** As a learner, I can take a timed set and see how time affects my
accuracy.

**Expected behaviour.** Visible countdown; the server records the deadline and
rejects answers submitted after it; the attempt auto-submits at expiry. The
client clock is not trusted.

**Acceptance criteria.**

- Remaining time survives a refresh and matches the server deadline.
- The attempt auto-submits at expiry without further user action.
- Answers after the deadline are rejected and cannot change the score.
- No pause or time extension in a timed set.

**Out of scope.** Section timing and breaks, exam-day replication, proctoring,
official rating prediction.

### F7 — Results and explanations

**Purpose.** Turn each mistake into a learning moment.

**User story.** As a learner, I see my score, the correct answers, and why each
answer is correct.

**Expected behaviour.** Results show score, per-item correctness, the explanation,
and the item's provenance. Practice scores are labelled as estimates, not official
CSC ratings. Results persist in history.

**Acceptance criteria.**

- Displayed correctness matches the saved answers.
- Every published item has an explanation and provenance displayed with it.
- The score is explicitly labelled an estimate.
- Results remain available in history after the session ends.

**Out of scope.** Simulated official ratings, eligibility claims, tutor chat,
predicted pass probability.

### F8 — Progress analytics

**Purpose.** Make progress visible and comparable over time.

**User story.** As a learner, I can see my accuracy by subject and topic and my
recent practice history.

**Expected behaviour.** Accuracy computed from submitted attempts only, always
shown with an attempt count so a single answer is not mistaken for a trend.
Recent sessions are paginated. Data is visible only to its owner.

**Acceptance criteria.**

- Accuracy matches the underlying attempts for every subject and topic.
- Every percentage is shown with its attempt count.
- History is paginated and scoped to the signed-in user.
- One user cannot read another user's analytics.

**Out of scope.** Cohort comparison, predicted readiness, shareable reports.

### F9 — Weak-topic diagnosis

**Purpose.** Tell the learner what to study next.

**User story.** As a learner, I see my weakest topics ranked, with a one-click way
to practise them.

**Expected behaviour.** A documented rule identifies weak topics (at least 3
attempts and below 70% accuracy), shows the basis ("based on N answers"), and
links to practice for that topic.

**Acceptance criteria.**

- The same inputs always produce the same weak-topic list.
- Each weak topic states the rule and the attempt count behind it.
- A learner with no weak topics sees an encouraging empty state with a suggestion.
- The rule is documented and testable.

**Out of scope.** Model-based diagnosis, study plans, scheduling, recommendations
(`REC`).

### F10 — Content flagging

**Purpose.** Catch incorrect or unclear content quickly.

**User story.** As a learner, I can report an item that is wrong or confusing.

**Expected behaviour.** Flag with a reason category and optional note; flags are
stored with the item and reporter; staff see a queue and can dismiss or retire the
item. Flags are never public.

**Acceptance criteria.**

- A flag persists and appears in the staff queue.
- Repeating the same flag on the same item by the same user does not create a
  duplicate.
- Resolving a flag records the decision and actor.
- The reporter is not identified publicly.

**Out of scope.** Public comments, appeals workflow, learner edits, reputation.

### F11 — Account deletion and export

**Purpose.** Meet privacy commitments without retaining personal data.

**User story.** As a learner, I can delete my account and take my data with me.

**Expected behaviour.** Deletion requires confirmation, removes profile data and
user content, and de-identifies remaining practice records so aggregate content
quality can survive without the person. Export is requested in-app and delivered
as a machine-readable archive; at alpha, fulfilment may be manual.

**Acceptance criteria.**

- After deletion, login fails and the email can be used to register again.
- No profile personal data remains, and attempts are no longer attributable.
- The export contains profile, attempts, results, and flags, in a documented
  format.
- Deleted users do not appear in staff lists.

**Out of scope.** Instant self-service export, portability to third-party formats,
retention beyond a documented legal minimum.

## 3. Deferred to the fast-follow beta (increment 2)

| Capability | Requirements | Gate |
| --- | --- | --- |
| PDF/DOCX upload, validation, private storage, async extraction | MAT-01..07, NFR-PERF-03, NFR-SEC-05 | Storage provider selected; KAB-005 threat model |
| Provider-independent AI adapter, prompts, RAG, quotas | AI-01..12, NFR-COST-01..03, NFR-PERF-04, NFR-SEC-08 | KAB-003 provider decision and data-processing terms; see [ai-capabilities.md](ai-capabilities.md) |
| AI summaries, generated items, review queue | AI-03..05, ADM-04 | AI platform; content review capacity |
| Flashcards | QST-04 | Materials or curated decks |
| Email verification before upload or AI use | AUTH-06 | Email provider (already required for password reset) |

Nothing in this table may be pulled into the MVP without a scope-change approval
that states the schedule, cost, and risk impact.

## 4. Launch hardening (increment 3)

Not a feature increment. Required before public availability: abuse controls and
rate limits beyond MVP defaults, structured logging and alerting, backups with a
tested restore, privacy policy and terms, accessibility audit, load test,
incident runbook, and a production deployment approval.

## 5. Explicitly out of scope for the MVP

- Identification and fill-in-the-blank exercises.
- Full CSE mock exam simulation with section timing.
- Personalized study plans and scheduling.
- Spaced repetition (FSRS or SM-2).
- Model-based weak-topic prediction; rule-based only.
- External material discovery and ingestion.
- Payments, subscriptions, entitlements, and invoices.
- Social features, leaderboards, public profiles, and sharing.
- Native mobile apps and offline/PWA mode.
- Multi-tenant institutions.
- Examinations other than CSE.
- OCR for scanned documents.
- Filipino-language interface and explanations.
- Proctoring or high-stakes certification.

Any addition requires a scope-change approval with impact on schedule, cost, and
risk.

## 6. Requirement-area release map

| Area | MVP | Fast-follow beta | Post-MVP |
| --- | --- | --- | --- |
| `AUTH` | 01–05, 08 | 06 | 07 |
| `CAT` | 01–04 | — | 05 |
| `QST` | 01, 02, 03, 05 | 04 | 06, 07 |
| `PRA` | 01–06 | — | 07, 08 |
| `ANL` | 01–04 | 05 (if schedule allows) | 06 |
| `ADM` | 01–03 | 04 | — |
| `MAT` | — | 01–07 | 08 |
| `AI` | — | 01–12 | — |
| `REC` | — | — | 01–03 |
| `DIS` | 03 (policy) | — | 01, 02 |

Non-functional requirements apply from the release that introduces the affected
area. `NFR-COST` applies from increment 2.

## 7. Exit criteria for the private alpha

- A new user can register, practise 20 items, and see a per-topic breakdown.
- 300+ human-reviewed CSE Professional items live, covering all four Professional
  subjects.
- Every MVP acceptance criterion above has a passing test.
- No open critical or high security finding.
- 10 usability sessions completed; most participants can name their next study
  action from the weak-topic view (M6).
- Core flows work at 360 px width and with a keyboard only.
- No unverified item count or time limit is displayed anywhere.

## 8. Dependencies and gates

| Dependency | Needed by | Status |
| --- | --- | --- |
| Approved PRD and exam reference | MVP | Draft, verified scope |
| Approved architecture and ADRs | MVP | Proposed |
| CSE content sourcing and review plan (KAB-004) plus a named reviewer | MVP | Not started |
| Threat model and privacy review (KAB-005) | MVP alpha | Not started |
| Transactional email provider | MVP (password reset) | Not selected |
| Alpha hosting environment | MVP alpha | Not selected |
| Object storage provider | Increment 2 | Not selected |
| AI provider and data-processing terms | Increment 2 | Not selected |

Transactional email moves into the MVP because password reset (`AUTH-04`) cannot
work without it. Local development can use the console email backend.

## 9. Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Reviewed content takes longer than engineering | Launch delay | Start content operations in parallel; 300-item gate is explicit |
| Original items are lower quality than expected | Trust loss | Review workflow, flagging, retire-and-replace loop |
| Learners do not return after one session | No validation | Instrument activation and day-7 return from the first alpha cohort |
| Rule-based weak topics feel arbitrary | Low trust | Show the rule and attempt count; test comprehension in usability sessions |
| Scope creep into AI or mock exams | Delay | Explicit out-of-scope list; scope change requires approval |
| Small team capacity | Quality loss | Small increments, automated checks, no speculative features |

## 10. Decisions required

1. Approve the MVP as increment 1 only.
2. Approve Subprofessional as catalogue-only at launch, with Clerical Ability
   modelled and content deferred.
3. Approve the 300-item content gate and name the accountable content reviewer.
4. Confirm that explicit pause/resume is not required (`PRA-07` stays `SHOULD`,
   scheduled post-MVP); refresh-based resume is the MVP behaviour.
5. Defer the question-history question (snapshot versus live reference) to the
   Checkpoint 6 data review, with snapshot recommended.
