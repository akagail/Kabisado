# Target Users

**Status:** Draft — requires validation
**Owner:** Product
**Last updated:** 2026-11-06

## 0. Validation status

**Evidence level: none.** These personas are derived from the product brief, not
from interviews, surveys, or analytics. No user research has been conducted.

Do not present the personas, their pains, or their willingness to pay as research
findings. The PRD records the same assumptions as A1–A7.

### Research plan (proposed, not yet executed)

**Method:** 5–10 semi-structured interviews with recent or upcoming CSE takers,
plus a screening form. Recruit through applicant communities and personal
networks. Do not collect CSC application data or documents.

**Screening:** took or plans to take the CSE within 12 months; level
(Professional or Subprofessional); device used for study; study hours per week;
money already spent on review materials or centres.

**Interview outline:**

1. Walk me through how you prepared for the last exam, or plan to.
2. What did you use, what did it cost, and what did you stop using?
3. When you get an answer wrong, what do you do next?
4. How do you decide what to study on a given day?
5. Show me your current reviewer: format, length, and where it came from.
6. What would make you distrust an AI-generated explanation or question?
7. If a tool showed your weakest topics, what would you do with that?
8. What would make you stop using a study app after one week?

**What would change the product:** evidence that learners do not study from
documents; evidence that a plain question bank is already sufficient; evidence
that privacy concerns block uploads; evidence that Subprofessional demand exceeds
Professional at launch.

**Output:** a dated research note in `docs/product/` with participant count and
findings, then update the persona sections and PRD assumptions A1–A7.

## 1. Primary persona — The CSE Professional aspirant

**Profile**

- 21–35 years old, Filipino citizen, metro or provincial.
- Applying for a first- or second-level government position, or taking the CSE
  to improve eligibility.
- Studies alongside work, school, or job hunting.
- Uses a mid-range Android phone as the primary device; may also use a laptop.

**Goals**

- Pass the CSE Professional level on the next attempt.
- Know which subjects and topics are weakest.
- Practice under time pressure.
- Understand why an answer is wrong, not just the correct letter.

**Frustrations**

- Reviewers are long, undifferentiated PDFs.
- Answer keys lack explanations.
- Advice online is contradictory or outdated.
- Re-taking the exam means restarting without diagnosis.
- Limited budget for review centers.

**Triggers**

- Exam application period opens.
- A friend passes or fails.
- A new job posting requires eligibility.

**Success looks like**

- A realistic practice score trend.
- A short list of weak topics with targeted practice.
- Confidence going into exam day.

## 2. Secondary persona — The Subprofessional candidate

Shares the primary persona's goals but needs clerical ability coverage. The 2027
announcement confirms Clerical Ability replaces Analytical Ability at this level.
Lower willingness to pay, often first-time examinees. May enter through the same
catalogue with a different exam variant.

## 3. Secondary persona — The licensure exam candidate

Preparing for PRC board examinations. Needs a different taxonomy and often
memorization-heavy content. Not an MVP segment; the data model must not block
them.

## 4. Secondary persona — The student

Preparing for college entrance or academic assessments. Likely a later segment.
Requires school-specific catalogues and guardian/privacy considerations for
minors.

## 5. Internal persona — The content curator

**Responsibilities**

- Seed CSE subjects and topics.
- Review AI-generated items for accuracy and tone.
- Record source, licence, and attribution.
- Retire bad items and investigate complaints.

**Needs**

- A review queue with clear provenance.
- Bulk actions and audit history.
- A policy for copyright and official-source use.
- The ability to mark content as official, licensed, user-provided, or
  AI-generated.

## 6. Jobs to be done

| Situation | Job | Current workaround |
| --- | --- | --- |
| I have a reviewer PDF | Turn it into something I can practice | Manually make flashcards |
| I finished a practice test | Understand my mistakes | Look up answers one by one |
| I have two weeks left | Focus on what matters | Reread everything |
| I keep failing numerical ability | Drill the weak area | Search for random worksheets |
| I don't trust AI answers | Verify the source | Cross-check the reviewer |

## 7. Assumptions and how to test them

| # | Assumption | How to validate | Status |
| --- | --- | --- | --- |
| P1 | Users trust AI explanations more when the source passage is shown | Interview Q6; compare prototype with and without citations | Unverified |
| P2 | Uploading personal reviewers is a stronger hook than a question bank | Interview Q5; landing-page interest test | Unverified |
| P3 | Mobile practice is more common than desktop | Screening questions; beta analytics by device | Unverified |
| P4 | Users prefer short sessions (10–20 minutes) on weekdays over full mock exams | Interview Q1–Q4; session-length data at beta | Unverified |
| P5 | Price sensitivity is high and a free tier is expected | Interview Q2; beta conversion after any pricing test | Unverified |

## 8. Anti-personas

- Users seeking official CSC application processing or eligibility issuance.
- Users seeking guaranteed exam answers or leakage.
- Institutions requiring proctored, high-stakes certification.
- Users who want to upload other people's copyrighted material for
  redistribution.

## 9. Accessibility and inclusion

- Target WCAG 2.2 AA for core study flows.
- Support keyboard navigation and visible focus.
- Do not rely on colour alone for correctness or progress.
- Respect reduced-motion preferences.
- Design for low bandwidth: compress assets, avoid blocking video, allow
  text-first study.
- Provide clear English; Filipino localization is a later decision.

## 10. Open questions

1. What device mix do target users actually have?
2. How much are users willing to pay, and for what?
3. Do users want Filipino-language explanations?
4. How do users currently verify answer correctness?
5. What makes a user abandon a review app?
