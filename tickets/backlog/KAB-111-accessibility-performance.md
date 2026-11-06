# KAB-111: Accessibility and Performance Baseline

**Status:** BACKLOG
**Type:** task
**Priority:** P1
**Epic:** E12 Compliance and Accessibility
**Owner:** unassigned
**Created:** 2026-11-06
**Updated:** 2026-11-06
**Specification:** not required (quality baseline)
**Related ADRs:** none
**GitHub issue:** none

## 1. Description

Audit and fix the core study flows for WCAG 2.2 AA and establish performance
budgets and measurement.

## 2. Business justification

Target users are mobile-first and may use assistive technology or slow networks.
Accessibility and speed are product requirements, not polish.

## 3. Scope

In:

- Keyboard-only navigation of auth, practice, and results.
- Screen-reader labels and live regions for timer/score.
- Contrast and focus visibility.
- Reduced-motion support.
- 360 px layout.
- Lighthouse budget for core pages.
- Bundle-size check.
- Image/font optimization.

Out:

- Full manual audit of every page (iterate).
- Native app accessibility.
- Localization.
- Dark mode.

## 4. Dependencies

| Dependency | Type | Status |
| --- | --- | --- |
| KAB-101, KAB-104 | core flows | pending |

## 5. Acceptance criteria

- [ ] Core flows pass an automated axe scan with no serious issues.
- [ ] Keyboard-only completion of login and practice.
- [ ] Timer and score changes are announced without spamming.
- [ ] Focus is visible and restored after dialogs.
- [ ] Reduced-motion preference is respected.
- [ ] LCP ≤ 2.5 s on a mid-range mobile profile.
- [ ] Initial JS budget is met.
- [ ] Findings and fixes are documented.

## 6. Implementation checklist

- [ ] Run an accessibility audit.
- [ ] Fix critical/serious issues.
- [ ] Add automated axe checks where practical.
- [ ] Measure Lighthouse on core routes.
- [ ] Set bundle budgets.
- [ ] Document results and remaining issues.

## 7. Testing checklist

- [ ] Keyboard walkthrough.
- [ ] Screen-reader spot check.
- [ ] Contrast check.
- [ ] Reduced-motion check.
- [ ] Mobile viewport check.
- [ ] Lighthouse run.

## 8. Validation evidence

```text
Not started.
```

## 9. Risks and notes

- Automated tools catch only part of accessibility; manual checks are required.
- Performance budgets can regress silently; review bundle size per PR.
- Do not remove motion wholesale; respect the preference.

## 10. References

- `docs/architecture/frontend-architecture.md` §9–10
- `docs/product/product-requirements.md` NFR-UX
