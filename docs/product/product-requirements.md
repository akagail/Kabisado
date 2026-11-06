# Product Requirements

**Status:** Draft — requires approval
**Owner:** Product
**Last updated:** 2026-11-06

Requirement IDs are stable. Add new requirements; do not renumber existing ones.
Priority is relative to the release that introduces the area: `MUST` = required
for that release, `SHOULD` = included if schedule allows, `COULD` = later. The
release assigned to each area is in
[mvp-scope.md](mvp-scope.md#6-requirement-area-release-map).

## 1. Functional requirements

### Authentication and profile (`AUTH`)

| ID | Priority | Requirement |
| --- | --- | --- |
| AUTH-01 | MUST | A user can register with email and password. |
| AUTH-02 | MUST | A user can log in and log out. |
| AUTH-03 | MUST | Passwords are hashed with a modern password hasher; minimum length and breached-password checks apply. |
| AUTH-04 | MUST | A user can reset a forgotten password by email. |
| AUTH-05 | MUST | A user can view and edit display name, target exam, and study preferences. |
| AUTH-06 | SHOULD | Email verification is required before generating AI content or uploading files. |
| AUTH-07 | COULD | Social login (Google) and institutional SSO. |
| AUTH-08 | MUST | A user can delete their account and personal data. |

### Examination catalogue (`CAT`)

| ID | Priority | Requirement |
| --- | --- | --- |
| CAT-01 | MUST | The system models exam categories, exams, subjects, and topics. |
| CAT-02 | MUST | CSE Professional and Subprofessional are seeded as catalogue entries. |
| CAT-03 | MUST | A user selects a target exam; content and practice are scoped to it. |
| CAT-04 | SHOULD | Topics carry a display order and parent/child hierarchy. |
| CAT-05 | COULD | Additional exam families (PRC, UPCAT) can be added without schema changes. |

### Personal materials (`MAT`)

| ID | Priority | Requirement |
| --- | --- | --- |
| MAT-01 | MUST | A user can upload PDF and DOCX files up to a configurable size limit. |
| MAT-02 | MUST | Uploads are validated by extension, MIME type, magic bytes, and size. |
| MAT-03 | MUST | Files are stored in private object storage; downloads use short-lived signed URLs. |
| MAT-04 | MUST | Each material records ownership, original filename, size, checksum, status, and timestamps. |
| MAT-05 | MUST | Text is extracted asynchronously; failures are visible to the owner and retryable. |
| MAT-06 | MUST | A user can delete a material and its derived content. |
| MAT-07 | SHOULD | Scanned PDFs are detected and flagged as requiring OCR. |
| MAT-08 | COULD | Image and plain-text uploads. |

### AI processing (`AI`)

| ID | Priority | Requirement |
| --- | --- | --- |
| AI-01 | MUST | All model calls go through a provider-independent adapter. |
| AI-02 | MUST | The active provider and model are configuration, not code. |
| AI-03 | MUST | Generated summaries and questions record source material, model, prompt version, and timestamp. |
| AI-04 | MUST | AI output is labelled as AI-generated and is never presented as official CSC content. |
| AI-05 | MUST | Generated items can be reviewed, accepted, or rejected before entering a practice set. |
| AI-06 | MUST | Prompt inputs delimit untrusted document text and resist prompt injection. |
| AI-07 | MUST | Token, cost, and rate limits are enforced per user and globally. |
| AI-08 | SHOULD | Generated content is cached by input hash and prompt version. |
| AI-09 | COULD | Streaming responses and multi-document synthesis. |

### Questions and flashcards (`QST`)

| ID | Priority | Requirement |
| --- | --- | --- |
| QST-01 | MUST | The system supports multiple-choice questions with one correct answer. |
| QST-02 | MUST | Each question has an explanation and a source reference. |
| QST-03 | MUST | Questions are scoped to a topic and difficulty. |
| QST-04 | MUST | Flashcards have a front, back, and source reference. |
| QST-05 | MUST | Users can flag an item as incorrect or unclear. |
| QST-06 | SHOULD | Question variants and distractor rationales. |
| QST-07 | COULD | Identification and fill-in-the-blank exercises. |

### Practice (`PRA`)

| ID | Priority | Requirement |
| --- | --- | --- |
| PRA-01 | MUST | A user can start an untimed practice set by topic or material. |
| PRA-02 | MUST | A user can start a timed practice set with a visible countdown. |
| PRA-03 | MUST | Answers are saved per attempt and survive a page refresh. |
| PRA-04 | MUST | Submitting shows score, correct answers, and explanations. |
| PRA-05 | MUST | A timed session auto-submits when time expires. |
| PRA-06 | MUST | The system prevents duplicate submission. |
| PRA-07 | SHOULD | Pause/resume for untimed sets. |
| PRA-08 | COULD | Full CSE mock exam simulation with section breaks. |

### Analytics (`ANL`)

| ID | Priority | Requirement |
| --- | --- | --- |
| ANL-01 | MUST | The system records attempts, responses, time spent, and correctness. |
| ANL-02 | MUST | A user sees accuracy by subject and topic. |
| ANL-03 | MUST | A user sees recent practice history. |
| ANL-04 | MUST | Weak topics are identified with a documented rule (e.g. ≥ 3 attempts and < 70% accuracy). |
| ANL-05 | SHOULD | Score trend over time. |
| ANL-06 | COULD | Predicted readiness and cohort comparison. |

### Recommendations and scheduling (`REC`)

| ID | Priority | Requirement |
| --- | --- | --- |
| REC-01 | COULD | Recommend the next topic based on weak-topic rules. |
| REC-02 | COULD | Generate a study schedule from exam date and available time. |
| REC-03 | COULD | Spaced-repetition scheduling for flashcards. |

### Discovery and attribution (`DIS`)

| ID | Priority | Requirement |
| --- | --- | --- |
| DIS-01 | COULD | Discover external review material with source attribution. |
| DIS-02 | COULD | Record licence, access terms, and attribution for every external source. |
| DIS-03 | MUST | The system does not ingest or republish material without a recorded right to use it. |

### Administration (`ADM`)

| ID | Priority | Requirement |
| --- | --- | --- |
| ADM-01 | MUST | Staff can manage catalogue entries and review AI-generated items. |
| ADM-02 | MUST | Staff actions on content are audited. |
| ADM-03 | MUST | Staff can suspend an account and remove abusive content. |
| ADM-04 | SHOULD | A dashboard shows ingestion, generation, and error queues. |

## 2. Non-functional requirements

### Security and privacy (`NFR-SEC`)

| ID | Requirement |
| --- | --- |
| NFR-SEC-01 | All traffic uses HTTPS in non-local environments. |
| NFR-SEC-02 | Object-level authorization is enforced on every user-owned resource. |
| NFR-SEC-03 | Secrets live only in environment/secret storage; no secrets in git. |
| NFR-SEC-04 | Authentication, upload, and AI endpoints are rate-limited. |
| NFR-SEC-05 | Uploaded files are untrusted; parsing runs in a constrained worker. |
| NFR-SEC-06 | Logs exclude passwords, tokens, full documents, and unnecessary PII. |
| NFR-SEC-07 | Personal data is deletable and exportable on request. |
| NFR-SEC-08 | AI providers are contractually prohibited from training on user data, or user content is redacted before sending. |
| NFR-SEC-09 | Dependency and container scans run in CI before release. |

### Performance (`NFR-PERF`)

| ID | Requirement |
| --- | --- |
| NFR-PERF-01 | p95 API latency < 400 ms for non-AI CRUD endpoints under expected MVP load. |
| NFR-PERF-02 | Practice session start returns within 1 s for a 20-item set. |
| NFR-PERF-03 | Upload initiation returns within 500 ms; processing is asynchronous. |
| NFR-PERF-04 | AI generation is queued and reports progress; no request waits on a model call. |
| NFR-PERF-05 | Frontend initial route JS stays within the budget set in the frontend architecture. |

### Reliability (`NFR-REL`)

| ID | Requirement |
| --- | --- |
| NFR-REL-01 | Background jobs retry with backoff and land in a dead-letter state after a bounded number of attempts. |
| NFR-REL-02 | Submitting a practice session is idempotent. |
| NFR-REL-03 | Database backups are taken daily in production; restore is tested before launch. |
| NFR-REL-04 | The API exposes liveness and readiness endpoints. |

### Accessibility and usability (`NFR-UX`)

| ID | Requirement |
| --- | --- |
| NFR-UX-01 | Core flows meet WCAG 2.2 AA. |
| NFR-UX-02 | Every data view has loading, empty, error, and unauthorized states. |
| NFR-UX-03 | Core flows work on a 360 px viewport and with keyboard only. |
| NFR-UX-04 | Correctness is never communicated by colour alone. |
| NFR-UX-05 | Reduced-motion preferences are respected. |

### Maintainability (`NFR-MNT`)

| ID | Requirement |
| --- | --- |
| NFR-MNT-01 | Business logic lives in services, not views, serializers, components, or tasks. |
| NFR-MNT-02 | Every module has an owner and documented boundary. |
| NFR-MNT-03 | Public API changes update the OpenAPI schema and tests. |
| NFR-MNT-04 | Migrations are checked in CI. |
| NFR-MNT-05 | Logs are structured and include a request/job correlation ID. |

### Cost (`NFR-COST`)

| ID | Requirement |
| --- | --- |
| NFR-COST-01 | AI spend is metered per user and per job. |
| NFR-COST-02 | A global daily spend cap can stop generation without taking down study features. |
| NFR-COST-03 | Object storage lifecycle rules delete abandoned uploads. |

## 3. Out of scope for the MVP

See [mvp-scope.md](mvp-scope.md) for the authoritative list.

## 4. Assumptions

- The CSE catalogue can be seeded from official coverage areas and original
  questions; official CSC items are not reproduced.
- A single-region deployment is acceptable for the MVP.
- Email delivery can use a transactional provider to be selected.
- Users accept AI-generated practice items when provenance and review status are
  visible.

## 5. Open questions

1. Is personal upload in the MVP or a fast follow?
2. Is email verification required at launch?
3. What is the free-tier limit for AI generation?
4. Which AI providers are approved for user documents?
5. What data-retention period applies to uploaded materials?
6. Is Filipino-language output required at launch?
7. What is the policy for user-reported incorrect items?
8. Which analytics events are allowed under the privacy policy?
