# Frontend Architecture

**Status:** Proposed — requires approval
**Owner:** Frontend
**Last updated:** 2026-11-06

## 1. Stack

- Next.js 16 App Router
- React 19
- TypeScript (strict)
- Tailwind CSS 4
- shadcn/ui components, copied into the repository
- Vitest + Testing Library for unit/component tests
- Playwright for end-to-end tests

## 2. Rendering strategy

- **Server components by default.** Data fetching happens on the server unless
  the interaction requires the client.
- **Client components at the leaves.** A page shell should remain a server
  component; only the interactive widget becomes `"use client"`.
- **Public/marketing pages** are statically rendered or revalidated.
- **Authenticated study pages** are dynamically rendered because they depend on
  the session.
- Avoid client-side waterfalls. Fetch independent data in parallel on the server.
- Streaming with `loading.tsx` and Suspense for slow, non-critical panels.

## 3. Route structure (proposed)

```text
frontend/src/app/
├── (marketing)/
│   ├── page.tsx                 # landing
│   └── layout.tsx
├── (auth)/
│   ├── login/page.tsx
│   ├── register/page.tsx
│   └── reset-password/page.tsx
├── (app)/
│   ├── layout.tsx               # authenticated shell
│   ├── dashboard/page.tsx
│   ├── exams/page.tsx
│   ├── materials/
│   │   ├── page.tsx
│   │   └── [id]/page.tsx
│   ├── practice/
│   │   ├── page.tsx
│   │   └── [id]/page.tsx
│   ├── flashcards/page.tsx
│   └── progress/page.tsx
├── api/
│   └── [...path]/route.ts       # same-origin proxy to Django (if not using rewrites)
├── layout.tsx
├── globals.css
└── not-found.tsx
```

Route groups do not affect the URL. Use them for layouts and access boundaries.

## 4. API access

There are two contexts:

1. **Browser → Next.js → Django.** The browser calls `/api/v1/...` on the same
   origin. Next.js proxies to `BACKEND_INTERNAL_URL` via a rewrite or route
   handler. Cookies remain first-party.
2. **Server component → Django.** The server calls
   `BACKEND_INTERNAL_URL/api/v1/...` directly and forwards the incoming cookie
   header.

Rules:

- One module (`src/lib/api/client.ts`) owns base URL, headers, error mapping,
  and retries.
- Components never build URLs by hand.
- API responses are typed. Generate types from OpenAPI or validate at the
  boundary; do not duplicate types manually.
- Mutations use server actions or route handlers, not ad-hoc `fetch` in
  components.
- Never expose `BACKEND_INTERNAL_URL` or any secret with `NEXT_PUBLIC_`.

## 5. Authentication handling

- The session cookie is `HttpOnly`; JavaScript cannot read it.
- The app shell fetches `/api/v1/auth/me` on the server. An unauthenticated
  response redirects to `/login`.
- Middleware is used only for cheap route protection and redirects, never as the
  sole authorization check. The API is authoritative.
- CSRF token is fetched and attached to unsafe requests by the API client.
- Logout calls the API, clears the session, and redirects.

## 6. State management

- **Server state:** fetch on the server; use React `useTransition` /
  `useOptimistic` for mutations.
- **URL state:** filters, pagination, and selected tabs belong in search params.
- **Local UI state:** `useState` / `useReducer` in the nearest client component.
- No global client store (Redux, Zustand) until a measured need exists.
- Do not cache user-specific data in a shared CDN cache.

## 7. Components

```text
src/
├── app/                 # routes only
├── components/
│   ├── ui/              # shadcn primitives
│   └── <domain>/        # composed domain components
├── lib/
│   ├── api/             # client, types, error mapping
│   ├── auth/            # session helpers
│   └── utils.ts
├── hooks/
├── styles/
└── tests/
```

Rules:

- `components/ui` is generated/vendored shadcn code; keep modifications minimal
  and documented.
- Domain components receive data as props; they do not fetch unless they are
  explicitly data containers.
- No business rules in components. Scoring, weak-topic logic, and permissions
  live in the backend.
- Every list has loading, empty, error, and unauthorized states.
- Every form has inline validation, a disabled pending state, and a server error
  path.

## 8. Styling

- Tailwind utility classes with design tokens in `globals.css`.
- shadcn/ui for accessible primitives (dialog, dropdown, tabs, form controls).
- No CSS-in-JS runtime.
- Use semantic tokens (`background`, `foreground`, `muted`, `destructive`) rather
  than raw hex values.
- Dark mode is a later decision; structure tokens so it is possible.
- Respect `prefers-reduced-motion`.

## 9. Accessibility

- WCAG 2.2 AA for core flows.
- Semantic landmarks, one `h1` per page, labelled controls.
- Visible focus rings; no `outline: none` without a replacement.
- Keyboard-operable dialogs, menus, and practice navigation.
- Announce score/time changes with appropriate ARIA live regions, without
  spamming screen readers.
- Colour is never the only signal for correct/incorrect.
- Test with keyboard and a screen reader before launch.

## 10. Performance budgets

- Initial route JS: ≤ 200 KB gzipped for marketing, ≤ 300 KB for app routes.
- LCP ≤ 2.5 s on a mid-range mobile device over 4G.
- CLS ≤ 0.1.
- No blocking third-party scripts.
- Images use `next/image`; fonts are self-hosted or use `next/font`.
- Heavy editors/viewers are dynamically imported.

Budgets are enforced by review initially; automate with Lighthouse CI later.

## 11. Error handling

- `error.tsx` per route group for recoverable rendering errors.
- `not-found.tsx` for missing resources.
- API errors map to a typed `ApiError` with `code`, `message`, and `fields`.
- Show actionable messages; never render raw stack traces.
- Network failures offer retry; mutations are idempotent where possible.
- Authentication expiry redirects to login with a return path.

## 12. Testing

| Layer | Tool | What |
| --- | --- | --- |
| Unit | Vitest | pure helpers, formatters, API error mapping |
| Component | Vitest + Testing Library | interactive components, states |
| E2E | Playwright | register → practise → results; upload → generate |
| Accessibility | axe (later) | core pages |

- Mock the API at the network boundary (MSW when needed), not by mocking React
  internals.
- Do not snapshot large DOM trees.
- E2E tests run against a built app and a seeded test database.

## 13. Environment variables

| Variable | Exposed | Purpose |
| --- | --- | --- |
| `BACKEND_INTERNAL_URL` | server only | Django base URL for server/proxy calls |
| `NEXT_PUBLIC_APP_URL` | browser | Canonical app URL |
| `NEXT_PUBLIC_API_BASE_PATH` | browser | Usually `/api/v1` |
| `NEXT_PUBLIC_SENTRY_DSN` | browser | Error reporting (optional, later) |

Secrets must never be prefixed with `NEXT_PUBLIC_`.

## 14. Open decisions

1. Vercel rewrites vs. a route handler for the API proxy.
2. Form library choice (native actions vs. react-hook-form + Zod).
3. Whether the app is a PWA at launch.
4. Dark mode and Filipino localization timing.
5. Error-reporting vendor.
