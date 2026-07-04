# Original User Request

## Initial Request — 2026-07-04T10:19:16+05:30

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
