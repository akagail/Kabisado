# ADR-0006: Presigned Direct-to-Object-Storage Uploads

**Status:** Proposed
**Date:** 2026-11-06
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
5. API verifies the object exists, size and checksum match, and magic bytes are
   acceptable; then enqueues extraction.
6. Downloads use short-lived presigned GET URLs; the bucket is private.

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

## Security requirements

- Bucket is private; no public ACLs.
- Presigned URLs expire in minutes and are scoped to one object/key.
- Maximum file size and allowed types enforced before signing and after upload.
- Verify magic bytes, not only the declared MIME type.
- Store objects under a non-guessable key; never trust the client filename.
- Antivirus/malware scanning is required before parsing if the provider supports
  it; otherwise document the residual risk and add it before public launch.
- Deleting a material deletes the object and derived rows.
- CORS allows only the application origin.

## Approval

Requires human approval and selection of the storage provider.
