# Security Guidelines

**Status:** Approved for foundation use
**Owner:** Engineering / Security
**Last updated:** 2026-11-06

Security is a design constraint, not a review step. If a change weakens a control,
stop and raise it.

## 1. Assets

- User accounts, credentials, and session tokens.
- Uploaded study materials and derived text.
- Practice history and performance data.
- AI prompts, outputs, and provider credentials.
- Content licences and attribution records.
- Audit logs and administrative actions.

## 2. Threat model (initial)

| Actor | Capability | Primary risk |
| --- | --- | --- |
| Anonymous visitor | Public endpoints | Enumeration, scraping, abuse |
| Authenticated user | Own data | IDOR, quota evasion, malicious uploads |
| Malicious document | Text processed by AI | Prompt injection, data exfiltration |
| Compromised account | Valid session | Data access, spam, cost abuse |
| Insider/staff | Admin access | Unauthorized content or data access |
| Dependency attacker | Supply chain | Code execution, credential theft |
| External provider | Receives prompts | Data retention/training, breach |

Trust boundaries: browser → Next.js, Next.js → Django, API → database, worker →
storage, worker → AI provider, admin → back office.

## 3. Authentication

- Passwords hashed with Django's current default (Argon2 preferred).
- Minimum length 10; reject common and breached passwords (implementation
  pending).
- No password hints or security questions.
- Login and reset responses do not reveal whether an email exists.
- Session rotation on login; logout flushes server-side.
- Session cookies: `HttpOnly`, `Secure`, `SameSite=Lax`.
- CSRF protection on all unsafe methods.
- Optional MFA for staff before public launch.
- Email verification before uploads/AI generation (recommended).
- Rate-limit and lock out after repeated failures, with a safe unlock path.

## 4. Authorization

- Default deny.
- Check object ownership in the service layer for every read and write.
- Never trust `user_id`, `owner_id`, or role fields from the request body.
- Staff endpoints require `is_staff` plus an explicit permission.
- Test cross-user access for every resource (IDOR).
- Do not use sequential IDs; UUIDs reduce enumeration.
- Admin actions are audited with actor, object, and timestamp.

## 5. Input validation

- Validate on the server; client validation is only UX.
- Use DRF serializers and Pydantic; do not hand-parse JSON.
- Enforce length, type, range, and enum allowlists.
- Reject unknown fields where practical.
- Escape output; React escapes by default, but avoid `dangerouslySetInnerHTML`.
- Use the ORM; no string-built SQL.
- Validate file names; never use them as storage keys.
- Limit request body size at the proxy and API.

## 6. File uploads

- Allowed types: PDF, DOCX (initial). Enforce extension, declared MIME, magic
  bytes, and size.
- Private bucket; no public ACLs.
- Presigned URLs expire quickly and are scoped to one key.
- Generate storage keys server-side (UUID), not from user input.
- Verify checksum and size after upload.
- Scan for malware before parsing if the provider supports it; otherwise document
  the residual risk and add scanning before public launch.
- Parse in a worker with memory/time limits; do not parse in the API process.
- Treat extracted text as untrusted.
- Delete object and derived rows on user deletion.
- Clean up abandoned uploads on a schedule.

## 7. AI-specific security

- Delimit untrusted text and keep system policy separate.
- The adapter has no tools, database access, or network access beyond the model
  call.
- Retrieval is scoped by owner in the query.
- Validate structured output; reject unsupported citations.
- Human review before shared publication.
- Rate-limit and meter usage; enforce a global spend cap.
- Do not log prompts or document text.
- Contractually prohibit provider training on user content, or redact.
- Run prompt-injection fixtures in CI.
- Label AI output clearly; never present it as official CSC content.

## 8. Secrets

- Stored in environment variables or a secret manager; never in git.
- `.env` is ignored; `.env.example` contains names and placeholders only.
- No secrets in client bundles (`NEXT_PUBLIC_*` is public).
- No secrets in logs, error messages, or AI prompts.
- Rotate on suspected exposure.
- CI uses placeholder values.
- Separate credentials per environment.
- Least privilege for storage, database, and AI keys.

## 9. Data privacy

Kabisado processes personal data and is subject to the Philippine Data Privacy
Act (R.A. 10173) and applicable NPC guidance. This section is engineering
guidance, not legal advice.

- Collect only what the product needs.
- Explain purpose, retention, and sharing in the privacy notice.
- Obtain consent for optional processing.
- Support access, correction, export, and deletion requests.
- Encrypt in transit (TLS) and at rest (provider-managed).
- Restrict staff access; log it.
- Do not use production data in development or tests.
- Set retention periods and enforce deletion.
- Record subprocessors (hosting, AI, email, storage).
- Report breaches through the documented incident process.
- Minors: not an initial target; if added, require guardian consent.

## 10. Logging and monitoring

- Log authentication events, authorization failures, admin actions, upload
  failures, and AI cost anomalies.
- Do not log passwords, tokens, full documents, prompts, or unnecessary PII.
- Use pseudonymous user IDs in logs.
- Protect logs from tampering; restrict access.
- Alert on spikes in 401/403/429, failed jobs, and AI spend.
- Retain security logs for at least 90 days; align with the privacy policy.

## 11. Rate limiting and abuse

- Login, registration, password reset.
- Upload initiation and completion.
- AI generation.
- Content flags and support contact.
- Use per-IP and per-user limits; return 429 with `Retry-After`.
- Do not let a single account exhaust the global AI budget.
- Add CAPTCHA only if measured abuse requires it.

## 12. Dependencies and supply chain

- Pin versions and commit lockfiles.
- Review new dependencies for maintenance, licence, and security.
- Run `npm audit` and `pip-audit` in CI.
- Enable Dependabot alerts and security updates.
- Do not install packages from untrusted sources.
- Do not run postinstall scripts from unvetted packages.
- Rebuild container images regularly for base-image patches.

## 13. Infrastructure

- HTTPS everywhere outside local.
- Database not publicly reachable.
- Redis not publicly reachable; require auth.
- Bucket private; CORS restricted to the app origin.
- Least-privilege IAM/credentials.
- Backups encrypted and restore-tested.
- Staging isolated from production data.
- No debug mode or verbose errors in production.
- Keep admin paths protected and monitored.

## 14. Incident response

1. **Detect** — alert, report, or dependency advisory.
2. **Contain** — rotate credentials, disable the endpoint/account, isolate the
   service.
3. **Assess** — scope, data affected, legal/notification obligations.
4. **Eradicate** — fix the root cause, patch dependencies.
5. **Recover** — restore service, verify integrity.
6. **Notify** — affected users and authorities as required.
7. **Learn** — blameless post-incident review and tickets.

Do not delete evidence. Do not publicly disclose an unpatched vulnerability.
Report security issues privately to the maintainer.

## 15. Copyright and content security

- Do not ingest or republish content without a recorded right to use it.
- Respect robots.txt, terms of service, paywalls, and access controls.
- Store licence, territory, expiry, and attribution.
- Provide a takedown path and act on valid complaints.
- Do not reproduce official exam items or leaked material.
- AI output may reproduce source text; keep quotations short and attributed.

## 16. Security review checklist

- [ ] Authentication and session handling are correct.
- [ ] Every object access checks ownership or staff permission.
- [ ] Inputs are validated server-side.
- [ ] Uploads are type/size/magic-byte validated and private.
- [ ] Secrets are not in code, logs, or client bundles.
- [ ] AI input is delimited and output validated.
- [ ] Rate limits exist for abuse-prone endpoints.
- [ ] Errors do not leak internals.
- [ ] Dependencies pass audit.
- [ ] Logs exclude sensitive data.
- [ ] Data deletion works end to end.
- [ ] Tests cover cross-user access and CSRF.
