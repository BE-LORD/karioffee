## 2026-07-04T04:49:16Z

Fix all layout rendering issues, interactive scroll spy bugs, and custom cursor/preloader glitches in both mobile and desktop viewports on the Liceria Coffee Roastery single-page application.

Working directory: c:\Users\pr7n8\Downloads\anti coffee zip\anti coffee

## Requirements

### R1. Preloader Skip Button and Body Lock
- The Cinematic Preloader must show on initial load and lock scrolling (`lc-lock` class on body).
- Clicking the skip button (`#lcSkip`) or pressing Escape must dismiss the preloader immediately and unlock scrolling.
- A safety timeout of 16 seconds must automatically unlock scrolling if the preloader fails.

### R2. Custom Cursors and Mobile Layout
- Custom cursor and follower must be completely hidden on viewports smaller than 992px (`max-width: 992px` or `hover: none`).
- The navigation icons must be hidden on mobile (width 375px) and a mobile menu button (`.nav-mobile-btn`) with z-index 1001 must be visible.
- Product cards must stack vertically in a single column on viewports smaller than 768px.

### R3. Scroll spy, Smooth Scroll, and Themes
- Header navigation links must get the `active` class when their corresponding sections are in view.
- Smooth scrolling to target sections must center the section close to the viewport top (within 150px).
- Body theme classes (`theme-espresso`, `theme-crema`, `theme-moss`) must toggle correctly as different sections scroll into view.

### R4. Test Suite Quality Gate
- Python playwright tests in the `tests/` directory must run and pass.
- Address any bugs in the test assertions (e.g. string vs regex matching in Playwright's `to_have_class` assertions).

## Acceptance Criteria

### Preloader & Layout
- [ ] Preloader safety timeout removes scroll lock.
- [ ] Cursors are hidden at 375px width.
- [ ] Mobile menu button is visible at 375px width and has z-index 1001.
- [ ] Product cards stack vertically at 375px width.

### Scroll & Interaction
- [ ] Scroll spy correctly toggles active classes on navigation links.
- [ ] Clicking nav links scrolls sections to the top.
- [ ] Body background theme changes to matching themes when scrolling sections.
- [ ] Testimonials deck controls and swipe-out transitions work as designed.
- [ ] Stepper transitions automatically every 5 seconds or manually on click.

### Test Verification
- [ ] `pytest -v -k "not test_static_assets_resolve"` runs successfully and all 17 tests pass.

## 2026-07-04T08:46:52Z

Restructure and polish the Karioffee coffee brand website to ensure it is extremely polished, interactive, responsive, fast, and bug-free across both mobile and desktop views, creating a loop of continuous improvements.

Working directory: c:\Users\pr7n8\Downloads\anti coffee zip\anti coffee
Integrity mode: development

## Requirements

### R1. Complete Mobile & Desktop Polish
Ensure the website layout is fully responsive, has zero horizontal overflow, utilizes interactive swipeable snap carousels on mobile, and premium micro-interactions, smooth scrolling, and scroll-driven animations on desktop.

### R2. Code Quality & Performance Optimization
Validate HTML structure, optimize asset loading (ensure images are compressed and lazy-loaded), format CSS/JS files, ensure zero console errors/warnings, and check that the site runs perfectly at 60fps.

## Acceptance Criteria

### Interactive Experience & Layout Quality
- [ ] Zero horizontal scrolling or overflow bugs on mobile view (down to 320px width).
- [ ] Interactive horizontal scroll-snap carousels function correctly for products and ritual steps on mobile.
- [ ] Visual polish (glassmorphism, shimmer effects, hover states) is consistent and premium on both desktop and mobile.
- [ ] Prettier formatting check passes on all HTML, CSS, and JS files.
- [ ] Console logs are free of any warnings or errors.
