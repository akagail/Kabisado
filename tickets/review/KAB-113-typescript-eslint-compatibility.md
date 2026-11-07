# KAB-113: TypeScript/eslint compatibility pin

**Status:** REVIEW
**Type:** task
**Priority:** P1
**Epic:** none
**Owner:** unassigned
**Created:** 2026-11-07
**Updated:** 2026-11-07
**Specification:** not applicable (toolchain fix)
**Related ADRs:** none
**GitHub issue:** none

## 1. Description

`frontend/package.json` declares `typescript@^7.0.2`, but
`eslint-config-next@16.4.5` bundles `typescript-eslint@8.72.1`, which refuses to
load under TypeScript 7:

```text
typescript-eslint does not support TS 7.0.
Error: typescript-eslint does not support TS 7.0.
```

A clean `npm ci` therefore fails `npm run lint`. Local `node_modules` had a
stale TypeScript 5.9.3 install, which hid the failure.

## 2. Business justification

The `frontend` CI check is required. While it fails on `main` and on every open
PR, no feature branch can merge.

## 3. Scope

In:

- Pin `typescript` to `^5.9.3` in `frontend/package.json`.
- Regenerate `frontend/package-lock.json`.

Out:

- Upgrading `eslint-config-next` or `typescript-eslint` (no released version
  supports TypeScript 7 yet).
- Any application code or test changes.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| typescript-eslint TS 7 support | upstream | Not available as of 2026-11-07 |

## 5. Acceptance criteria

- [x] `npm ci` installs TypeScript 5.9.3.
- [x] `npm run lint` passes.
- [x] `npm run typecheck`, `npm test -- --run`, and `npm run build` pass.
- [x] Lockfile diff only removes TypeScript 7 native platform packages.

## 6. Implementation checklist

- [x] Code implemented within scope.
- [x] No migrations or API schema changes.
- [x] PR records the dependency justification.

## 7. Testing checklist

- [x] Clean install (`npm ci`) then lint.
- [x] Typecheck.
- [x] Unit test.
- [x] Production build.
- [ ] E2E: unaffected, no application change.

## 8. Validation evidence

```text
npm ci                                  passed; typescript 5.9.3
npm run lint                            passed
npm run typecheck                       passed
npm test -- --run                       1 passed
npm run build                           passed (3 pages)
```

## 9. Risks and notes

- This is a deliberate downgrade from the Dependabot TypeScript 7 bump. Remove
  the pin once `typescript-eslint` supports TypeScript 7.
- TypeScript 7 native platform packages are removed from the lockfile as a
  result; expected.

## 10. References

- Failing run: https://github.com/akagail/Kabisado/actions/runs/42342838886
- Dependabot PR #12 (`typescript` 5.9.3 → 7.0.2)
- https://github.com/typescript-eslint/typescript-eslint/issues/10940
