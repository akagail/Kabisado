# ADR-0006: Presigned Direct-to-Object-Storage Uploads

**Status:** Approved — with conditions
**Date:** 2026-11-06
**Approved:** 2026-11-07
**Deciders:** Engineering, Security
**Supersedes:** none

## Context

Users upload PDF and DOCX reviewers. Files may be large (tens of MB). Routing
bytes through Next.js serverless functions or the Django API would hit body-size
and timeout limits, consume application memory, and complicate scaling. Files
must remain private and be deleted on request.

## Decision

Use **direct browser uploads to private S3-compatible storage via short-lived
presigned URLs** issued by the API.

Flow:

1. Client sends metadata (filename, size, content type, checksum) to the API.
2. API validates quota and metadata, creates a `Material` row in
   `pending_upload`, and returns a presigned upload URL plus required headers.
3. Browser uploads directly to storage.
4. Client calls `POST /materials/{id}/complete`.
5. API verifies the object exists, size and checksum match, magic bytes are
   acceptable, ownership is confirmed, and extraction is enqueued **idempotently**.
6. Downloads use short-lived presigned GET URLs; the bucket is private;
   ownership is re-checked before issuing any download URL.

Security controls (see also [`file-upload-architecture.md`](../file-upload-architecture.md)):

- **Ownership**: every read or write to a `Material` (completion, download URL
  generation, deletion) requires the authenticated user to own the material.
- **Idempotent completion**: `POST /materials/{id}/complete` uses
  `(material_id, input_hash)` as an idempotency key; completing twice yields the
  same extraction job without duplication.
- **Expiration and orphan cleanup**: uploads older than a configurable period
  (default 7 days) are eligible for orphan cleanup; a background job deletes
  expired pending objects and marks the row `deleted`, with retries for transient
  storage errors.
- **Malware scanning**: if the provider supports server-side scanning, the scan
  result blocks extraction; otherwise, manual review/content moderation is queued
  and held before parsing begins — the deferred-moderation path is documented
  security control and is resolved before public launch.
- **Presigned URL reuse**: S3 presigned PUT/GET URLs can be reused until their
  expiration unless an application-level protection (single-use assertion of the
  storage signature on completion) is enforced. Application-level protections:
  completion hashes the uploaded object against the stored `checksum_sha256`;
  a completed-but-reuploaded attempt is rejected at completion, preventing a
  replay that could bypass extraction.

## Alternatives considered

| Option | Why not |
| --- | --- |
| Upload through Next.js route handler | Serverless body/time limits; memory cost |
| Upload through Django | Ties up API workers; poor for large files |
| Public bucket + obscure URLs | Not private; unacceptable |
| Client SDK with long-lived credentials | Leaks credentials to the browser |

## Consequences

Positive:

- Large files do not touch application servers.
- Storage scales independently.
- Upload can resume with standard S3 mechanisms later.
- Private-by-default access.

Negative:

- Validation must be split between metadata (before) and content (after upload).
- Orphaned uploads need a cleanup job.
- Presigned URL configuration is provider-specific.
- CORS rules on the bucket must be maintained.

## Open decisions

- Object storage provider: **selected under O2**; not yet chosen. Provider
  selection remains a separate open decision and does not change this design.

## Approval

Approved in principle on 2026-11-07 with conditions:

- Ownership verification on completion and download URL generation.
- Idempotent completion for extraction jobs.
- Upload expiration, orphan cleanup, retry handling.
- Malware scanning or documented alternative before parsing.
- Documentation of presigned URL reuse and application-level protections.
