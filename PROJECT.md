# Project: Karioffee Website Restructuring and Polishing

## Architecture
- Single-page application using:
  - HTML5 structure in `index.html`.
  - CSS custom properties, grid/flexbox layouts, responsive design in `css/style.css` and `css/intro.css`.
  - Vanilla JS for state management, scroll handling, stepper autoplay, and testimonials slider in `js/main.js` and `js/intro.js`.
  - Animations powered by GSAP and ScrollTrigger.
  - Smooth scrolling powered by Lenis.
  - 3D elements powered by Three.js.

## Code Layout
- `index.html` - Core HTML skeleton
- `css/` - Style sheets (style.css, intro.css)
- `js/` - JavaScript logic (main.js, intro.js)
- `assets/` - Image/font assets
- `tests/` - Playwright E2E test files (test_tier1.py, test_tier2.py, test_tier3.py, test_tier4.py)

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Baseline Exploration | Audit the codebase, identify existing bugs, overflow issues, formatting status, and test failures. | None | IN_PROGRESS |
| 2 | Mobile & Desktop Polish | Eliminate horizontal scroll/overflow down to 320px. Implement mobile-friendly swipeable snap carousels for products and ritual steps. Add glassmorphism, shimmer effects, and hover states. | M1 | PLANNED |
| 3 | Core Interactivity Fixes | Fix preloader safety timeout/lock, custom cursors/mobile visibility, scroll spy, smooth scroll top offset, and theme shifts. | M2 | PLANNED |
| 4 | Code Quality & Performance | Format code with Prettier. Eliminate console warnings/errors. Verify 60fps performance and optimize asset loading. | M3 | PLANNED |
| 5 | E2E Testing & Hardening | Run all tests (Tiers 1-4). Run Forensic Audit (Integrity Verification). | M4 | PLANNED |

## Interface Contracts
- None (Single-page client-only application).
