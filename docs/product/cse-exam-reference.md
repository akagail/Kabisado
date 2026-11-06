# CSE Examination Reference

**Status:** Reference — verify before content ingestion
**Owner:** Product / Content
**Last updated:** 2026-11-06

This document records what the product assumes about the Philippine Civil Service
Examination (CSE). The **current official CSC examination announcement is always
authoritative**. Re-check it before seeding or updating content.

## 1. Official sources

- Civil Service Commission: <https://www.csc.gov.ph/>
- Examination announcements and advisories:
  <https://www.csc.gov.ph/examination-advisories/>
- 2026 schedule announcement:
  <https://www.csc.gov.ph/2026-civil-service-exam-schedule-and-application-timelines-released>
- Online application: <https://ocseas.csc.gov.ph/>
- Results: <https://erpo.csc.gov.ph/ocsergs/>

## 2. Examination levels

- **Professional** — first- and second-level positions, excluding positions
  requiring a professional licence or covered by special laws.
- **Subprofessional** — first-level positions.

Both are administered as a Pen and Paper Test (CSE-PPT) and, in some cases, a
Computerized Examination (COMEX).

## 3. Coverage (recent bulletins)

The following is the coverage reported in recent CSC-aligned announcements and
must be verified against the bulletin for the target exam date.

**Professional level (English and Filipino)**

- Numerical Ability — basic operations; word problems.
- Analytical Ability — word association (identifying assumptions and
  conclusions); logic; data interpretation.
- Verbal Ability — grammar and correct usage; vocabulary; paragraph
  organization; reading comprehension.

**Subprofessional level (English and Filipino)**

- Numerical Ability — basic operations; word problems.
- Clerical Ability — filing; spelling.
- Verbal Ability — grammar and correct usage; vocabulary; paragraph
  organization; reading comprehension.

**General information (both levels)**

- Philippine Constitution.
- Code of Conduct and Ethical Standards for Public Officials and Employees
  (R.A. 6713).
- Peace and human rights issues and concepts.
- Environment management and protection.

## 4. Format (recent bulletins)

| Item | Professional | Subprofessional |
| --- | --- | --- |
| Items | 170 | 165 |
| Time | 3 hours 10 minutes | 2 hours 40 minutes |
| Passing rate | 80.00% | 80.00% |

**Caution:** item counts, time limits, and coverage can change. Store the source
announcement date and URL with every seeded exam version.

## 5. Eligibility and application facts

The CSE is not a licence and does not guarantee appointment. Eligibility rules,
application requirements, fees, and schedules are set by CSC. Kabisado must not
claim to process applications or issue eligibility. Link users to the official
CSC channels.

## 6. Product mapping

The catalogue should model:

```text
ExamFamily (Civil Service)
└── Exam (CSE Professional, CSE Subprofessional)
    ├── ExamVersion (e.g. 2027 bulletin)
    └── Subject (Numerical Ability, Verbal Ability, ...)
        └── Topic (Basic Operations, Word Problems, ...)
```

Each `ExamVersion` records the official source URL, publication date, item count,
time limit, and passing rate. Practice content is scoped to an `ExamVersion` so a
bulletin change does not silently alter historical attempts.

## 7. Content and copyright policy

1. **Official coverage areas are facts.** Use them to structure the catalogue.
2. **Official exam items are not public domain by default.** Do not copy leaked,
   recalled, or reconstructed items. Write original questions against the
   published coverage.
3. **Third-party reviewers** require a recorded licence or written permission.
   Store the licence, territory, expiry, and attribution.
4. **User uploads** remain the user's responsibility. The user grants Kabisado a
   limited licence to process the file for their own study; the file is not
   republished.
5. **AI-generated items** must be labelled, source-linked, and reviewed before
   entering a shared pool.
6. **External discovery** must respect robots.txt, terms of service, paywalls,
   and access restrictions. Link out rather than mirroring content.
7. **Attribution** is stored as structured data, not only as prose.

## 8. Open questions

- Which exam date/version is the launch target?
- Will the first content set be original items, licensed items, or both?
- Who is the accountable content reviewer?
- What is the takedown and correction process?
- Should Subprofessional launch with Professional or later?
