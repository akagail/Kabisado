# Traceability

**Status:** Current for Phase 2 (2026-11-06)
**Owner:** Product / Engineering
**Last updated:** 2026-11-06

Maps every requirement to the specification that will define it, the ticket that
will implement it, and the verification it needs. Requirement IDs are stable and
live in [product-requirements.md](product-requirements.md); feature IDs in
[mvp-scope.md](mvp-scope.md).

## 1. Planned specifications

None are written yet. They are proposed here so tickets reference a real target.

| Spec | Title | Feature(s) | Ticket | Release |
| --- | --- | --- | --- | --- |
| SPEC-0001 | Accounts and profile | F1, F2, F11 | KAB-101 | MVP |
| SPEC-0002 | CSE catalogue | F3 | KAB-102 | MVP |
| SPEC-0003 | Question bank, review, and flags | F4, F10 | KAB-103 | MVP |
| SPEC-0004 | Practice and results | F5, F6, F7 | KAB-104 | MVP |
| SPEC-0005 | Progress analytics and weak topics | F8, F9 | KAB-105 | MVP |
| SPEC-0006 | Material upload and extraction | Beta | KAB-106 | Beta |
| SPEC-0007 | AI platform: adapter, prompts, RAG, quotas | Beta | KAB-107 | Beta |
| SPEC-0008 | AI study aids and review | Beta | KAB-108 | Beta |
| SPEC-0009 | Flashcards | Beta | KAB-109 | Beta |

Launch hardening (KAB-110, KAB-111, KAB-112) is operational work, not a feature
spec.

## 2. Verification key

`U` unit or service test, `A` API/integration test, `C` component test, `E`
end-to-end test, `M` manual check, `CI` pipeline gate, `SEC` security test.

## 3. Functional requirements

### Authentication and profile

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| AUTH-01 | SPEC-0001 | KAB-101 | A, E |
| AUTH-02 | SPEC-0001 | KAB-101 | A, E |
| AUTH-03 | SPEC-0001 | KAB-101 | U |
| AUTH-04 | SPEC-0001 | KAB-101 | A |
| AUTH-05 | SPEC-0001 | KAB-101 | A, C |
| AUTH-06 | Hardening | **Gap** | A |
| AUTH-07 | Post-MVP | — | — |
| AUTH-08 | SPEC-0001 | KAB-101 | A, E |

### Examination catalogue

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| CAT-01 | SPEC-0002 | KAB-102 | U, CI |
| CAT-02 | SPEC-0002 | KAB-102 | A |
| CAT-03 | SPEC-0001, SPEC-0002 | KAB-102 | A |
| CAT-04 | SPEC-0002 | KAB-102 | U |
| CAT-05 | Post-MVP | KAB-102 (schema test) | U |

### Personal materials (beta)

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| MAT-01 | SPEC-0006 | KAB-106 | A |
| MAT-02 | SPEC-0006 | KAB-106 | U, SEC |
| MAT-03 | SPEC-0006 | KAB-106 | A, SEC |
| MAT-04 | SPEC-0006 | KAB-106 | A |
| MAT-05 | SPEC-0006 | KAB-106 | Worker, E |
| MAT-06 | SPEC-0006 | KAB-106 | A, E |
| MAT-07 | SPEC-0006 | KAB-106 | Worker |
| MAT-08 | Post-MVP | — | — |

### AI processing (beta)

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| AI-01 | SPEC-0007 | KAB-107 | U |
| AI-02 | SPEC-0007 | KAB-107 | U |
| AI-03 | SPEC-0007, SPEC-0008 | KAB-107 | A |
| AI-04 | SPEC-0008 | KAB-108 | C, E |
| AI-05 | SPEC-0008 | KAB-108 | A, E |
| AI-06 | SPEC-0007 | KAB-107 | SEC |
| AI-07 | SPEC-0007 | KAB-107 | U, A |
| AI-08 | SPEC-0007 | KAB-107 | U |
| AI-09 | Post-MVP | — | — |
| AI-10 | SPEC-0008 | KAB-108 | A, E |
| AI-11 | SPEC-0007 | KAB-107 | A |
| AI-12 | SPEC-0007 | KAB-107 | CI |

### Questions and flashcards

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| QST-01 | SPEC-0003 | KAB-103 | U, A |
| QST-02 | SPEC-0003 | KAB-103 | U, A |
| QST-03 | SPEC-0003 | KAB-103 | U |
| QST-04 | SPEC-0009 | KAB-109 | A, E |
| QST-05 | SPEC-0003 | KAB-103 | A, E |
| QST-06 | Post-MVP | — | — |
| QST-07 | Post-MVP | — | — |

### Practice

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| PRA-01 | SPEC-0004 | KAB-104 | A, E |
| PRA-02 | SPEC-0004 | KAB-104 | A, E |
| PRA-03 | SPEC-0004 | KAB-104 | A, E |
| PRA-04 | SPEC-0004 | KAB-104 | A, E |
| PRA-05 | SPEC-0004 | KAB-104 | A |
| PRA-06 | SPEC-0004 | KAB-104 | A |
| PRA-07 | Post-MVP | — | — |
| PRA-08 | Post-MVP | — | — |

### Analytics

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| ANL-01 | SPEC-0005 | KAB-105 | U |
| ANL-02 | SPEC-0005 | KAB-105 | A |
| ANL-03 | SPEC-0005 | KAB-105 | A |
| ANL-04 | SPEC-0005 | KAB-105 | U, A |
| ANL-05 | SPEC-0005 | KAB-105 (if schedule) | A |
| ANL-06 | Post-MVP | — | — |

### Administration

| ID | Spec | Ticket | Verification |
| --- | --- | --- | --- |
| ADM-01 | SPEC-0003 | KAB-103 | A |
| ADM-02 | SPEC-0003 | KAB-103 | U |
| ADM-03 | — | **Gap** | A |
| ADM-04 | SPEC-0003 | KAB-103 | A |

### Post-MVP areas

| IDs | Area | Note |
| --- | --- | --- |
| REC-01..03 | Recommendations and scheduling | Post-MVP |
| DIS-01, DIS-02 | External discovery and attribution | Post-MVP; requires a licensing process |
| DIS-03 | No ingestion without recorded rights | Policy enforced in SPEC-0003 and SPEC-0006; reviewed in KAB-004 |

## 4. Non-functional requirements

| IDs | Verification | Owner / gate |
| --- | --- | --- |
| NFR-SEC-01 | Deployment check | KAB-112 |
| NFR-SEC-02 | A across SPEC-0001..0006 | Each spec |
| NFR-SEC-03 | CI secret scan | CI |
| NFR-SEC-04 | A, rate-limit tests | KAB-101; KAB-106/107 in beta |
| NFR-SEC-05 | SEC worker isolation | KAB-106 |
| NFR-SEC-06 | Log review | KAB-110 |
| NFR-SEC-07 | A, E | KAB-101 |
| NFR-SEC-08 | Contract plus redaction test | KAB-107 |
| NFR-SEC-09 | CI dependency and container scan | CI |
| NFR-PERF-01 | Load test | KAB-111 |
| NFR-PERF-02 | Perf test, 20-item set | KAB-104, KAB-111 |
| NFR-PERF-03 | A | KAB-106 |
| NFR-PERF-04 | A, worker test | KAB-107 |
| NFR-PERF-05 | Build budget check | KAB-111 |
| NFR-REL-01 | Worker retry and dead-letter test | KAB-106, KAB-107 |
| NFR-REL-02 | A (double submit) | KAB-104 |
| NFR-REL-03 | Restore drill | KAB-112 |
| NFR-REL-04 | Smoke test | Core scaffold, KAB-112 |
| NFR-UX-01 | Accessibility audit | KAB-111 |
| NFR-UX-02 | C, E per view | Every spec |
| NFR-UX-03 | E at 360 px and keyboard | KAB-111 |
| NFR-UX-04 | C, M | KAB-111 |
| NFR-UX-05 | C | KAB-111 |
| NFR-MNT-01 | Code review | Every spec |
| NFR-MNT-02 | Review against AGENTS.md | Every spec |
| NFR-MNT-03 | OpenAPI schema check | CI + every API spec |
| NFR-MNT-04 | `makemigrations --check` | CI |
| NFR-MNT-05 | Log review | KAB-110 |
| NFR-COST-01..03 | U, worker test | KAB-107 |

## 5. Gaps before specification work

| # | Gap | Resolution |
| --- | --- | --- |
| 1 | `AUTH-06` email verification has no ticket | Fold into KAB-110 (hardening) or create a small ticket |
| 2 | `ADM-03` account suspension has no owner | Extend KAB-101 or create a ticket; suspend must be audited |
| 3 | Content seeding execution (300 items) has a plan ticket (KAB-004) but no delivery ticket | Decide whether seeding is part of KAB-103 or its own ticket |
| 4 | Flag resolution UI is implied by KAB-103 but not in its acceptance criteria | Add to KAB-103 during spec work |
| 5 | KAB-104 does not mention snapshot acceptance criteria | Add under ADR-0007 when SPEC-0004 is written |
| 6 | `database-design.md` still shows `SessionItem` without snapshot fields | Update with SPEC-0004; do not edit during Phase 2 |
| 7 | Export format undefined | Decide in SPEC-0001 |

## 6. Proposed issue changes after spec approval

No issue is created or edited until the specs are approved.

| Issue | Proposed change |
| --- | --- |
| KAB-101 | Add suspension (ADM-03), export format, and deletion audit to scope |
| KAB-103 | Add flag queue and resolution, plus content-review audit |
| KAB-104 | Add snapshot fields and immutability tests (ADR-0007) |
| KAB-105 | Confirm whether the score trend (ANL-05) is inside the MVP schedule |
| KAB-110 | Add email verification (AUTH-06) if hardening keeps it |
| KAB-111 | Confirm WCAG audit scope, 360 px, and keyboard E2E |
| New (if approved) | Content seeding execution ticket with reviewer ownership |

## 7. Maintenance

Update this file when a requirement is added, a spec is written, a ticket changes
scope, or a release mapping changes. A requirement with no spec, ticket, or
verification is a defect in planning, not a detail to fix later.
