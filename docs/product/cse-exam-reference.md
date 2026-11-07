# CSE Examination Reference

**Status:** Reference — scope verified for the 14 March 2027 CSE-PPT
**Owner:** Product / Content
**Last updated:** 2026-11-06

This document records verified facts about the Philippine Civil Service
Examination (CSE) used to structure the product catalogue. The **current official
CSC examination announcement is always authoritative**. Re-check it before
seeding or updating content, and record the version you verified against.

## 1. Source of record

| Field | Value |
| --- | --- |
| Source | Examination Announcement No. 06, s. 2026 |
| Title | Conduct of the 14 March 2027 CSE-PPT for Professional and Subprofessional Levels |
| Issuing office | CSC Examination, Recruitment and Placement Office |
| Signed | 21 October 2026 (Atty. Helene Grace T. Ramos, Director IV) |
| Published | CSC Examination Announcements and Advisories page |
| Accessed | 2026-11-06 |
| PDF | <https://csc.gov.ph/phocadownload/userupload/erpo/announcements/2026/ExamAnn_2026_06_Conduct%20of%2014%20March%202027%20CSE-PPT%20orig%20signed.pdf> |
| Landing page | <https://csc.gov.ph/examination-advisories/examination-announcement-no-06-s-2026-career-service-examination-pen-and-paper-test-for-professional-and-sub-professional-levels-14-march-2027> |

Supporting official channels:

- CSC website: <https://www.csc.gov.ph/>
- Examination advisories: <https://www.csc.gov.ph/examination-advisories/>
- Online application: <https://ocseas.csc.gov.ph/>
- Results: <https://erpo.csc.gov.ph/ocsergs/>

The announcement states that the CSC may issue a subsequent or supplemental
announcement amending the scope of examination. Treat any such issuance as a new
exam version.

## 2. Examination schedule facts

| Field | Value |
| --- | --- |
| Examination | Career Service Examination, Pen and Paper Test (CSE-PPT) |
| Levels | Professional and Subprofessional |
| Date | 14 March 2027 |
| Application period | 2 November 2026 until available slots are filled, or until otherwise announced |
| Testing center transfer deadline | 9 December 2026 |
| Examination fee | PHP 500.00 |
| Target release of results | On or before 11 May 2027 (may be adjusted by examinee volume) |
| Individual ratings | OCSERGS, within 14 days after the List of Passers is posted |

Testing centers and slot counts are listed per region in the announcement. The
CSC does not publish individual results by mail; only the List of Passers on the
CSC website is official.

## 3. Levels and resulting eligibility

| Level | Eligibility granted | Appropriate for |
| --- | --- | --- |
| Professional | Career Service Professional Eligibility | First-level (clerical) and second-level (technical) positions, including executive/managerial second-level positions |
| Subprofessional | Career Service Subprofessional Eligibility | First-level (clerical) positions only |

Both eligibilities exclude positions involving the practice of a profession or
covered by special laws. The Register of Eligibles (RoE) is the basis for
certification and appointment; it may also be a reference for private-sector
employment.

## 4. Scope of examination (verified)

Taken verbatim from section F of Announcement No. 06. In the official table,
General Information, Verbal Ability, and Numerical Ability cells span both
levels; Analytical Ability and Clerical Ability are level-specific.

| Subject area | Language | Professional | Subprofessional |
| --- | --- | --- | --- |
| General Information | English | Yes | Yes |
| Verbal Ability | English and Filipino | Yes | Yes |
| Numerical Ability | English | Yes | Yes |
| Analytical Ability | English | Yes | No |
| Clerical Ability | English | No | Yes |

### 4.1 General Information

1. Philippine Constitution
2. Code of Conduct and Ethical Standards for Public Officials and Employees
   (R.A. 6713)
3. Peace and Human Rights Issues and Concepts
4. Environment Management and Protection

### 4.2 Verbal Ability

1. Word meaning
2. Sentence completion
3. Error recognition
4. Sentence structure
5. Paragraph organization
6. Reading comprehension

### 4.3 Numerical Ability

1. Basic operations
2. Number sequence
3. Word problems

### 4.4 Analytical Ability (Professional only)

1. Word analogy
2. Symbolic logic/abstract reasoning
3. Identifying assumptions and drawing conclusions
4. Data interpretation

### 4.5 Clerical Ability (Subprofessional only)

1. Filing
2. Spelling

These are the only published coverage areas. The announcement publishes no
sub-topic weighting, item distribution, or difficulty specification.

## 5. Format

| Field | Professional | Subprofessional | Status |
| --- | --- | --- | --- |
| Passing grade | General rating of at least 80.00 | General rating of at least 80.00 | Verified |
| Number of items | Not published in this announcement | Not published in this announcement | Unverified |
| Time allotment | Not published in this announcement | Not published in this announcement | Unverified |

**Do not display item counts or time limits as fact.** The previously recorded
figures (170 / 165 items, 3 h 10 min / 2 h 40 min) do not appear in the 2027
announcement and have no cited official source. Treat them as unverified until a
CSC issuance for this exam version states them; store the source with the
`ExamVersion` when it does.

## 6. Facts that constrain product behaviour

From the announcement's disclaimers, data privacy notice, and prohibited acts:

1. **No CSC affiliation.** The CSC neither holds review classes nor publishes,
   distributes, or accredits review materials or review centers. Kabisado must
   not imply CSC endorsement, accreditation, or partnership.
2. **No CSC marks.** The CSC does not permit use of its name, logo, or former
   emblem in promotions or materials. Do not use CSC branding.
3. **No sharing of test questions.** The CSC denounces sharing or disseminating
   test questions and suggested answers, including on social media. Kabisado
   must not host, reproduce, or solicit recalled items.
4. **Cheating is criminal.** R.A. 9416 covers cheating and unauthorized
   possession, use, reproduction, or dissemination of examination materials.
   Product features must not enable any of these.
5. **Personal data.** Applicant information is handled under R.A. 10173 (Data
   Privacy Act of 2012). Kabisado collects its own users' data and must publish
   its own privacy notice; it must not claim to process CSC applications.
6. **Application and eligibility are CSC processes.** Kabisado informs and links
   out; it never files applications or issues eligibility.

## 7. Product mapping

```text
ExamFamily (Civil Service)
└── Exam (CSE Professional, CSE Subprofessional)
    └── ExamVersion (14 March 2027 CSE-PPT, Announcement No. 06 s. 2026)
        ├── Subject (General Information, Verbal, Numerical, Analytical, Clerical)
        │   └── Topic (e.g. Word analogy, Filing)
        └── Format facts (passing grade; item count and time limit when verified)
```

- The catalogue mirrors the published subject and topic names; do not invent
  topics beyond the official list. Sub-topics may be added later as study aids
  only if they are clearly not presented as CSC coverage.
- An `ExamVersion` records the source URL, publication date, access date, passing
  grade, and any verified format facts.
- Practice content is scoped to an `ExamVersion` so a supplemental announcement
  does not silently rewrite historical attempts.
- Subprofessional differs only by Clerical Ability in place of Analytical
  Ability. Content is not interchangeable between levels even where the subject
  name matches, because the level and difficulty differ.

## 8. Content and copyright policy

1. **Official coverage areas are facts.** Use them to structure the catalogue.
2. **Official exam items are not public domain.** Do not copy leaked, recalled,
   or reconstructed items. Write original questions against the published
   coverage.
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

## 9. Unverified items and open questions

| Item | Status | Resolution |
| --- | --- | --- |
| Item count per level | Unverified | Obtain an official CSC issuance for the 14 March 2027 version |
| Time allotment per level | Unverified | Same |
| Per-subject item distribution | Not published | Do not model as official; practice sets use our own composition |
| Scoring beyond the 80.00 general rating | Not published | Do not simulate an official score; label practice scores as estimates |
| Whether 2027 has additional CSE schedules | Not checked | Re-check CSC advisories before marketing a date |
| Computerized Examination (COMEX) scope and schedule | Not checked | Out of MVP scope; verify before any COMEX feature |

## 10. Review trigger

Re-verify this document when any of the following occurs:

- A supplemental CSC announcement changes the scope or format.
- The next CSE announcement is published.
- Content seeding begins for a new `ExamVersion`.
- A user or reviewer disputes a coverage claim.
