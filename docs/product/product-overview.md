# Product Overview

**Status:** Draft
**Owner:** Product
**Last updated:** 2026-11-07

## Vision

Kabisado turns a learner's own review materials and a curated examination
catalogue into a personalized study loop: **study → practice → understand the
mistake → focus on the weak topic → repeat**.

The platform should feel like a competent review coach, not a PDF viewer with a
chat box. Answers must be explainable, progress visible, and sources attributable.

## Product Principles

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

## Initial Audience

Students and applicants preparing for the Philippine Civil Service Examination
(CSE), starting with the Professional level. The architecture and taxonomy must
support additional examinations without a rewrite.

See [target-users.md](target-users.md) and [cse-exam-reference.md](cse-exam-reference.md).

## MVP Summary

The MVP is a **CSE Professional study loop** (private alpha):

1. Create an account and choose CSE Professional.
2. Practise seeded CSE topics, untimed or timed.
3. See the score, per-question explanations, and weak topics.
4. Return to the weak topic and practise again.

Personal reviewer upload and AI study aids follow in the fast-follow beta.

Full detail and explicit exclusions: [mvp-scope.md](mvp-scope.md).

## Non-goals for the MVP

- Replacing official CSC registration or eligibility records.
- Guaranteeing a passing score.
- Becoming a general-purpose chatbot.
- Social feeds, leaderboards, or public profiles.
- Native mobile applications.
- Paid subscriptions and payment processing.
- Republishing copyrighted reviewers without permission.

## Key References

- Master requirements: [prd.md](prd.md)
- Feature definitions: [mvp-scope.md](mvp-scope.md)
- User journeys: [specifications/](../specifications/)
- Verified exam scope: [cse-exam-reference.md](cse-exam-reference.md)
