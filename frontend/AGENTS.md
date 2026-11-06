# AGENTS.md — Frontend

Read the root [`AGENTS.md`](../AGENTS.md) first. This file adds frontend-specific
rules; it does not replace the root.

## Stack

Next.js 16 App Router, React 19, TypeScript strict, Tailwind CSS 4, shadcn/ui.
Tests: Vitest + Testing Library; E2E: Playwright.

## Commands

```bash
cd frontend
npm ci
npm run dev
npm run lint
npm run typecheck
npm test -- --run
npm run build
npx playwright test
```

## Structure

```text
src/
├── app/                 # routes, layouts, loading/error/not-found
├── components/ui/       # shadcn primitives
├── components/<domain>/ # composed domain components
├── lib/api/             # client, types, error mapping
├── lib/auth/            # session helpers
├── hooks/
└── tests/
```

## Rules

- Server components by default. Add `"use client"` only at the interactive leaf.
- Never fetch directly in a client component; use the shared API client or a
  server action/route handler.
- One API client owns base URL, CSRF, credentials, and error mapping.
- The browser uses same-origin `/api/v1/...`; never hardcode the backend origin.
- No business rules in components. Scoring, permissions, and weak-topic logic
  live in the backend.
- Keep filters, pagination, and tabs in the URL.
- Do not add a global state library without a measured need.
- Every data view has loading, empty, error, and unauthorized states.
- Use semantic Tailwind tokens, not raw hex values.
- Use accessible primitives; label every input and icon-only button.
- Respect `prefers-reduced-motion`.
- Do not use `dangerouslySetInnerHTML` on user or AI content.
- Secrets never use `NEXT_PUBLIC_`.

## Testing

- Test user-visible behaviour with Testing Library queries by role/label.
- Mock at the network boundary, not React internals.
- Add an E2E test for new critical journeys.
- No arbitrary sleeps in Playwright; wait for state.
- If a check cannot run, say so; do not claim it passed.

## Dependencies

- Do not add a package for a few lines of code.
- Justify new dependencies in the PR (maintenance, licence, size).
- Keep `package-lock.json` in sync.
- Do not upgrade majors in a feature PR.

## Prohibited

- Business logic or direct database/AI access in the frontend.
- Storing tokens in `localStorage`.
- Bypassing the API for authorization decisions.
- Unlabelled form controls or colour-only status.
- Committing `.env` or secrets.

<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
