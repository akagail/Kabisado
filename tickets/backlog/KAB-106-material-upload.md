# KAB-106: Material Upload and Extraction

**Status:** BACKLOG
**Type:** feature
**Priority:** P2
**Epic:** E6 Materials
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** required before implementation
**Related ADRs:** ADR-0006
**GitHub issue:** https://github.com/akagail/Kabisado/issues/19

## 1. Description

Implement private PDF/DOCX upload via presigned URLs, validation, asynchronous
text extraction and chunking, processing status, and deletion.

## 2. Business justification

Personal reviewers are the product differentiator. This ticket builds the secure
ingestion path that AI study aids depend on.

## 3. Scope

In:

- Upload initiation with quota and metadata validation.
- Presigned PUT/GET URLs.
- Completion verification (existence, size, checksum, magic bytes).
- Asynchronous extraction and chunking.
- Status: pending_upload, uploaded, processing, ready, failed.
- Retry and visible error.
- Material list/detail/delete UI.
- Deletion of object, chunks, and derived content.
- Abandoned upload cleanup job.

Out:

- OCR for scanned PDFs.
- Image/plain-text uploads.
- Sharing materials.
- AI generation (KAB-107/108).

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-101 | auth | pending |
| KAB-003 | object storage | pending |
| KAB-005 | security review | pending |

## 5. Acceptance criteria

- [ ] A user can upload a PDF under the size limit and see processing status.
- [ ] Invalid type, size, magic bytes, or checksum is rejected.
- [ ] Files are private; access requires a short-lived signed URL.
- [ ] Extraction runs in a worker, never in the request.
- [ ] Text and chunks are stored with page references.
- [ ] Failed extraction is visible and retryable.
- [ ] Deleting a material removes the object and derived rows.
- [ ] A user cannot access another user's material (IDOR).
- [ ] Abandoned uploads are cleaned up.
- [ ] DOCX support is included or explicitly deferred.

## 6. Implementation checklist

- [ ] Write and approve the specification.
- [ ] Write the technical design.
- [ ] Implement models and migrations.
- [ ] Implement storage adapter and presigning.
- [ ] Implement validation and completion.
- [ ] Implement extraction/chunking job.
- [ ] Implement status, retry, deletion.
- [ ] Build UI.
- [ ] Update docs and OpenAPI.

## 7. Testing checklist

- [ ] Upload validation matrix.
- [ ] Presign expiry/scope test.
- [ ] Extraction job test with fixture files.
- [ ] Retry/idempotency test.
- [ ] Deletion cascade test.
- [ ] IDOR test.
- [ ] Worker memory/time limit test.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Malware scanning is a launch requirement; document if deferred.
- Do not parse files in the API process.
- Store objects under server-generated keys.
- Keep original files immutable.

## 10. References

- `docs/architecture/decisions/0006-file-uploads.md`
- `docs/engineering/security-guidelines.md` §6
