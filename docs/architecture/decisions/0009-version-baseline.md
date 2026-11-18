# ADR-0009: Version baseline after ADR-0002

**Status:** Approved
**Date:** 2026-11-17
**Approved:** 2026-11-17
**Deciders:** Repository owner, Engineering
**Supersedes:** version rows of ADR-0002 (partial)
**Related:** ADR-0002, KAB-002, KAB-113, O7

## Context

ADR-0002 approved the initial stack with Django 5.2 LTS and a policy that Django
stays on an LTS line and does not adopt a feature release without an ADR. The
backend was then built and tested on Django 6.1.3. TypeScript was pinned to
5.9.3 because `typescript-eslint` does not support TypeScript 7 yet (KAB-113).

The version rows in ADR-0002 no longer describe the repository. Two documents
(ADR-0002 and `backend-architecture.md`) claim Django 5.2 LTS, while
`backend/requirements.txt` pins `Django>=6.1.3,<6.2`.

## Decision

Record the versions actually in use. Everything else in ADR-0002 — stack
choices, upgrade policy, hosting direction — remains in force.

| Layer | Version |
| --- | --- |
| Frontend | Next.js 16.4.x, React 19.3.x, Tailwind CSS 4.3.x |
| TypeScript | 5.9.x, pinned |
| Backend | Python 3.13, Django 6.1.x, Django REST Framework 3.18.x |
| Database | PostgreSQL 17 |
| Queue | Celery + Redis 7 (when async work lands) |
| Files | S3-compatible object storage |

**Django.** 6.1 is a feature release, adopted under ADR-0002's escape hatch
("do not adopt a feature release without an ADR"). Stay on 6.1 through the
14 March 2027 launch. Upgrade to 6.2 LTS when it ships (expected April 2027) and
record the upgrade. Do not adopt a later feature release without another ADR.

**TypeScript.** Pin 5.9.x. Major upgrades are gated by `typescript-eslint`
support; Dependabot ignores TypeScript majors until that support lands (KAB-113).

## Alternatives considered

| Option | Why not chosen |
| --- | --- |
| Downgrade to Django 5.2 LTS | Policy-compliant, but the backend is built and tested on 6.1; a downgrade adds risk and retesting without a launch benefit. 6.1 is supported through the next LTS. |
| Leave the docs as they are | Contradictory version statements cause agents and reviewers to make wrong assumptions. |

## Consequences

Positive:

- Documentation matches the code.
- No downgrade churn before the launch.

Negative:

- Django 6.1 is not an LTS; the 6.2 upgrade is a scheduled task, not optional.
- Feature releases have a shorter support window than LTS lines.

Mitigation:

- Create the 6.2 LTS upgrade ticket after the March 2027 launch; CI covers the
  upgrade.

## Approval

Approved on 2026-11-17 by the repository owner as part of KAB-002. This ADR
supersedes only the version rows of ADR-0002; the rest of ADR-0002 remains
approved.
