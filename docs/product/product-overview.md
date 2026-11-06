# Product Overview

**Status:** Draft — requires approval
**Owner:** Product
**Last updated:** 2026-11-06

## 1. Problem

Preparing for Philippine government and professional examinations is expensive,
fragmented, and hard to personalize. Reviewers are often static PDFs or
unstructured social-media material. Learners cannot easily tell what they do not
know, why an answer is wrong, or what to study next. High-quality review content
is scattered across books, handouts, and unofficial sources with unclear
ownership.

## 2. Vision

Kabisado turns a learner's own review materials and a curated examination
catalogue into a personalized study loop: **study → practice → understand the
mistake → focus on the weak topic → repeat**.

The platform should feel like a competent review coach, not a PDF viewer with a
chat box. Answers must be explainable, progress must be visible, and sources must
be attributable.

## 3. Initial audience

Students and applicants preparing for the Philippine Civil Service Examination
(CSE), starting with the Professional level. The architecture and taxonomy must
support additional examinations without a rewrite.

See [target-users.md](target-users.md) and
[cse-exam-reference.md](cse-exam-reference.md).

## 4. Value proposition

| For | Kabisado provides |
| --- | --- |
| CSE candidates | A structured CSE study path with practice, explanations, and weak-topic feedback |
| Self-directed learners | Their own notes and reviewers turned into flashcards and practice questions |
| Repeat takers | Diagnosis of weak areas instead of restarting from page one |
| Content curators | A traceable pipeline from source material to approved learning items |

## 5. Product principles

1. **Learning outcome over engagement.** Do not optimize for streaks or time in
   app at the expense of understanding.
2. **Explain, don't just answer.** Every practice item should teach.
3. **Source integrity.** AI output is labelled, traceable, and never presented as
   official CSC material.
4. **Personal material stays personal.** Uploaded documents are private by
   default and never used to train third-party models without explicit consent.
5. **Accessible and low-bandwidth aware.** Philippine learners may use mid-range
   phones and intermittent connections.
6. **No dark patterns.** No fake urgency, hidden subscriptions, or manipulative
   notifications.

## 6. Capability map

| Capability | MVP | Later |
| --- | --- | --- |
| Registration, authentication, profile | Yes | SSO, institutional accounts |
| Examination catalogue (CSE) | Yes | PRC, UPCAT, other government exams |
| Personal material library | Yes | Sharing, groups |
| PDF/DOCX upload and extraction | Yes | OCR for scanned files, images |
| AI summaries and explanations | Yes | Multi-document synthesis |
| Multiple-choice practice | Yes | Adaptive item selection |
| Identification exercises | No | Yes |
| Flashcards | Yes | Generated decks from broad material |
| Timed practice examinations | Yes (basic) | Full mock exam simulation |
| Answer explanations | Yes | Socratic tutoring mode |
| Progress analytics | Yes (topic accuracy) | Cohorts, predicted readiness |
| Weak-topic identification | Yes (rule-based) | Model-based diagnosis |
| Study recommendations | No | Personalized plans |
| Spaced repetition | No | FSRS-based scheduler |
| External material discovery | No | Licensed partner content |
| Offline mode | No | PWA cache |

## 7. Success measures (proposed)

These are hypotheses, not commitments.

- **Activation:** a new user completes one practice session within 24 hours.
- **Learning loop:** median user completes 3 sessions in the first week.
- **Explanation quality:** ≥ 80% of rated explanations are helpful.
- **Diagnostic usefulness:** weak-topic labels match user self-report in
  usability testing.
- **Retention:** 4-week return rate for activated users.
- **Trust:** zero unresolved copyright takedowns and zero confirmed cross-user
  data exposure.

Baselines and targets require product approval after beta data exists.

## 8. MVP summary

The MVP is a **CSE Professional study loop**:

1. Create an account and choose CSE Professional.
2. Upload a personal reviewer (PDF/DOCX) or use seeded CSE topics.
3. Generate flashcards and multiple-choice practice items from approved sources.
4. Take an untimed or timed practice set.
5. See the score, per-question explanations, and weak topics.
6. Return to the weak topic and practice again.

Full detail and explicit exclusions: [mvp-scope.md](mvp-scope.md).

## 9. Non-goals for the MVP

- Replacing official CSC registration or eligibility records.
- Guaranteeing a passing score.
- Becoming a general-purpose chatbot.
- Social feeds, leaderboards, or public profiles.
- Native mobile applications.
- Paid subscriptions and payment processing.
- Republishing copyrighted reviewers without permission.

## 10. Assumptions and open decisions

**Assumptions**

- Users have a browser and an email address.
- Most initial content will be English and Filipino; Tagalog UI copy may be
  needed later.
- CSE Professional is the highest-demand initial segment.
- Users will upload their own reviewers if the privacy story is clear.

**Needs approval**

- Confirm CSE Professional as the sole launch exam.
- Confirm whether personal upload is MVP or a fast follow.
- Confirm the free/paid model before building entitlements.
- Confirm data-retention and AI-provider policies before public launch.

## 11. Research sources

- Civil Service Commission official site: <https://www.csc.gov.ph/>
- CSC examination announcements (current bulletin is authoritative)
- CSC 2026 examination schedule announcement:
  <https://www.csc.gov.ph/2026-civil-service-exam-schedule-and-application-timelines-released>

Competitor and learner research is not yet documented. Do not cite invented
research.
