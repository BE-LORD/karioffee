# Project: Liceria Coffee SPA Fixes

## Architecture
- The application is a single-page HTML/JS/CSS application ("Liceria Coffee Roastery").
- Files involved:
  - `index.html`: Main HTML structure.
  - `css/intro.css` & `css/style.css`: Styles for the intro preloader and main design.
  - `js/intro.js` & `js/main.js`: Interactive scripts, including Lenis smooth scrolling, cursors, and custom transitions.
  - `tests/`: Pytest Playwright test suite (Tiers 1-4).

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Test Suite Assertion Fix | Fix Playwright regex assertions in `tests/test_tier1.py`, `tests/test_tier3.py`, `tests/test_tier4.py` (string vs compiled regex). | None | PLANNED |
| M2 | Preloader Skip & Body Lock | Implement cinematic preloader initial show, scrolling lock (`lc-lock`), click/Escape dismiss, and 16s safety timeout. | M1 | PLANNED |
| M3 | Custom Cursors & Mobile Layout | Hide custom cursor on mobile viewports (<992px). Hide nav icons on mobile (375px), make `.nav-mobile-btn` with z-index 1001 visible. Stack product cards. | M2 | PLANNED |
| M4 | Scroll Spy, Smooth Scroll & Themes | Implement scroll spy class toggling, Lenis smooth scroll within 150px viewport top, and toggle body theme classes correctly. | M3 | PLANNED |

## Interface Contracts
### `intro.js` ↔ `index.html`
- `#liceria-intro` represents the intro preloader.
- `#lcSkip` skip button.
- Escape key listener to dismiss the preloader.
- CSS class `.lc-lock` locks body scroll.

### `main.js` ↔ `style.css`
- Navigation links `#navLinks a`.
- Body theme classes: `theme-espresso`, `theme-crema`, `theme-moss`.
