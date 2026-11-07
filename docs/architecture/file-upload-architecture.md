# File Upload Architecture

**Status:** Proposed — needs security controls review (ADR-0006)  
**Owner:** Backend / Architecture  
**Last updated:** 2026-11-07  

## 1. Goals

- Enable secure, private upload of study materials (PDF, DOCX) for learner use.
- Implement presigned direct-to-object-storage uploads with proper security controls.
- Ensure uploaded content is private, expires appropriately, and is cleaned up properly.
- Support extraction, embedding, and AI processing workflows.

## 2. Non-goals

- Public sharing of uploaded materials.
- Unlimited upload size or unlimited storage.
- Public API for file uploads (use presigned URLs only).
- Direct file storage in Django app storage (must use external storage).

## 3. Architecture Overview

The upload flow consists of:

1. **Client Request**: Client requests a presigned URL from the backend API.
2. **Backend Validation**: Backend validates file type, size, and MIME type.
3. **Presigned URL Generation**: Backend generates a presigned URL with appropriate expiration.
4. **Client Upload**: Client uploads file directly to object storage using the presigned URL.
5. **Storage & Metadata**: Object storage stores the file with a generated key and metadata.
6. **Backend Verification**: Backend verifies file integrity (checksum) and status.
7. **Processing**: File is queued for processing (extraction, embedding, AI generation).
7. **Cleanup**: Abandoned or expired uploads are cleaned up according to retention policy.

## 4. Security Controls

### 4.1 Authentication and Authorization

- Uploads are scoped to the authenticated user (user_id in request).
- Backend validates that the user is authenticated before generating presigned URLs.
- User cannot request uploads for other users.

### 4.2 File Validation

- **Type**: Accept only PDF and DOCX files (configurable).
- **Size**: Maximum file size (configurable, e.g., 100 MB).
- **MIME Type**: Must match declared content type.
- **Magic Bytes**: Verify file content matches declared type.
- **Checksum**: Store and verify SHA256 checksum for integrity.

### 4.3 Presigned URL Security

- **Expiration**: URLs expire after a short period (e.g., 15 minutes).
- **Scope**: URL is scoped to one key (object path), not user-wide.
- **Method**: PUT/POST to storage endpoint only.
- **Integrity**: Backend verifies checksum after upload before marking file as "uploaded".

### 4.4 Storage Security

- **Private Bucket**: No public ACLs; objects are private by default.
- **Lifecycle Rules**: Auto-delete abandoned uploads after configurable period (e.g., 7 days).
- **Access Control**: Presigned URLs are scoped to one key and one user.
- **Encryption**: At-rest encryption enabled by storage provider (e.g., AWS SSE-S3).

### 4.5 Privacy and Data Handling

- **Consent**: User must acknowledge privacy notice at first upload.
- **Data Minimization**: Only store necessary metadata (filename, size, type, key).
- **Deletion**: File and derived content (chunks, embeddings) are deleted when user deletes account or material.
- **No Cross-User Access**: User cannot access another user's files or metadata.

## 5. API Endpoints

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| POST | `/materials/upload/presigned-url/` | Session | Request presigned URL |
| POST | `/materials/upload/` | Session | Upload file to storage using presigned URL |
| GET | `/materials/{id}/` | Session | Get file metadata (read-only) |
| DELETE | `/materials/{id}/` | Session | Delete file and derived content |

## 5.1 Presigned URL Request

Request:

```json
{
  "filename": "study-material.pdf",
  "content_type": "application/pdf",
  "size_bytes": 1048576
}
```

Response:

```json
{
  "url": "https://storage.example.com/private/abc123.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...",
  "expires_at": "2026-12-01T12:00:00Z",
  "fields": {
    "X-Amz-Algorithm": "AWS4-HMAC-SHA256",
    "X-Amz-Date": "20261201T120000Z",
    "X-Amz-Expires": "900",
    "X-Amz-SignedHeaders": "host",
    "X-Amz-Signature": "abc123..."
  }
}
```

## 6. Implementation Details

- **Backend**: Django view that validates file metadata and generates presigned URL using storage provider SDK.
- **Storage**: S3-compatible object storage (e.g., AWS S3, Cloudflare R2, Backblaze B2, or self-hosted MinIO).
- **Processing**: File is queued for processing via Celery after successful upload.
- **Error Handling**: 
  - File too large → 413
  - Invalid type/size → 400
  - Upload failure → 500
- **Idempotency**: Backend validates checksum after upload to prevent duplicates.

## 7. Security Considerations

- **CSRF**: All upload endpoints require CSRF protection (same-origin proxy).
- **Rate Limiting**: Apply rate limits on upload endpoint to prevent abuse.
- **Input Validation**: Server-side validation of file metadata before generating presigned URL.
- **Audit Logging**: Log upload requests with user_id, file_hash, and outcome.
- **Content Filtering**: Provider may scan for malware; if not supported, document residual risk.
- **Regulatory Compliance**: Ensure provider supports data residency requirements for PH/SG.

## 8. Dependencies

- `file-upload-architecture.md` (this document)
- `api-contracts.md` (API endpoints)
- `security-guidelines.md` (security controls)
- `deployment.md` (storage provider selection)
- `ai-architecture.md` (processing pipeline integration)

## 8.1 Implementation Phases

1. **Phase 1**: Basic upload flow with presigned URLs (MVP)
2. **Phase 2**: File validation and processing pipeline integration
3. **Phase 3**: Advanced features (versioning, lifecycle rules, content scanning)

## 8.2 Open Questions

- Exact expiration time for presigned URLs (15 min vs. 1 hour)
- Maximum file size for MVP
- How to handle file size limits (reject vs. chunked upload)
- How to handle file type spoofing (magic bytes vs. extension)

## 8.3 Security Review Checklist

- [ ] Presigned URL expiration is short and user-scoped
- [ ] File type, size, and magic bytes are validated server-side
- [ ] Storage is private with no public access
- [ ] Presigned URL cannot be reused after expiration
- [ ] Backend verifies file integrity after upload
- [ ] Abandoned uploads are cleaned up on schedule
- [ ] Rate limiting applied to upload endpoint
- [ ] Audit logs include user, file hash, and outcome