# Liceria Coffee SPA - Investigation & Analysis Report

## Overview
This report provides a read-only architectural investigation and diagnostic analysis of the single-page application (SPA) codebase for **Liceria Coffee Roastery**, specifically focusing on identified layout rendering bugs, interactive scroll spy glitches, preloader/custom cursor issues, and test suite failure diagnoses (R1 to R4).

---

## 1. Architectural Structure (R1, R2, R3)

### R1: Preloader Skip & Body Lock
* **HTML/DOM Element**: `#liceria-intro` (the splash/preloader overlay).
* **CSS Files**: `css/intro.css` provides the loading screen layouts, panel divisions (left/right sliding doors), progress percentage bars, skip button layout, and structural z-indexes (set to `10000`).
* **JS Files**: `js/intro.js` orchestrates the preloader's loading sequence, safety timeouts, and exit animations:
  - **Scroll Lock**: The body is locked on page load by applying the class `.lc-lock` to prevent user scrolling during the cinematic entrance.
  - **Skip Button**: The click handler on `#lcSkip` accelerates the loading progress to 100% and triggers `exit()`.
  - **Safety Timeout**: A 16-second safety net timer is registered via `setTimeout` to automatically dismiss the preloader and release the scroll lock in case assets take too long to load.
  - **Handshake / Exit**: Once progress reaches 100%, GSAP animates the panels sliding away, updates the body class to include `.intro-complete`, and removes `.lc-lock`. It then fires a custom window event `liceria:introdone` which `js/main.js` listens for to trigger the page entrance animations (like hero copy split-text reveals).

### R2: Custom Cursors & Mobile Layout
* **HTML/DOM Elements**: `.cursor` (center dot) and `.cursor-follower` (outer tracking ring) elements are appended to the root document.
* **JS Files**: `js/main.js` checks if viewports are wider than 992px (`window.innerWidth > 992`). If true:
  - Listens to `mousemove` events to capture raw cursor coordinates.
  - Tweening calculations are updated inside the GSAP ticker loop (`gsap.ticker.add`) to interpolate cursor positioning with smooth following behavior (`lerp` approximation).
  - Hover triggers add `.hover` and `.drag-mode` (on product card hover) classes to expand the follower circle and display the "VIEW" text inside `.cursor-text`.
* **CSS Files**: `css/style.css` defines base styling (fixed positioning, sizes, background colors, and mix-blend-mode for difference filter colors).
  - Hides cursors on mobile screens (viewport width <= 992px) and no-hover touch screens.
  - Responsive layouts are managed via media queries (`@media (max-width: 992px)`, `@media (max-width: 768px)`, etc.), adjusting grid templates (e.g., 4-column product grid to 2-column or 1-column layouts, 6-column footer grid to 3-column or 2-column layouts).

### R3: Scroll Spy, Smooth Scroll, and Themes
* **Smooth Scrolling**: Powered by **Lenis** scroll engine wrapper in `js/main.js` bound to GSAP's requestAnimationFrame ticker.
* **Scroll Spy**: The window's scroll event listener runs a `scrollSpy()` check that computes target sections' bounding client rects. If a section crosses the `window.innerHeight * 0.4` threshold, the active class is shifted to its matching navigation link.
* **Theme Switching**: Defined in `js/main.js` using ScrollTrigger triggers for `#home`, `#shop`, `#about`, `#ritual`, and `#blog` sections. When a section scrolls to 45% of the viewport height, `setTheme(themeName)` is called to dynamically swap class lists on the `body` element (`theme-crema`, `theme-moss`, `theme-espresso`, etc.).

---

## 2. Test Suite Assertion Bugs (R4)
The test suite utilizes `pytest-playwright` and `playwright.sync_api.expect` assertions. All class checking assertions matching a regex pattern are written as raw python strings (e.g. `expect(locator).to_have_class(r'.*\bclass\b.*')`).
* **The Root Cause**: Playwright's `expect().to_have_class(expected)` checks if the class attribute of the element matches the expected pattern.
  - If a **string** is passed as the argument, Playwright performs an **exact string match**.
  - It only does a **regex pattern match** if the argument is a compiled regex object (e.g. from Python's standard `re.compile(...)`).
  - Consequently, assertions like `expect(body).to_have_class(r'.*\blc-lock\b.*')` try to verify if the class attribute of the body is literally `".*\\blc-lock\\b.*"`, which times out and fails.

---

## 3. Baseline Test Failures (Documentation)
A execution run of the test suite using `pytest -v -k "not test_static_assets_resolve"` yields several failures. Below is the documentation of these errors:

[TBD - Final Test Run Tracebacks to be inserted here]
