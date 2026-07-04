import pytest
import re
from playwright.sync_api import expect

def test_preloader_safety_timeout(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000', wait_until='commit')
    
    body = page.locator('body')
    intro = page.locator('#liceria-intro')
    
    # If page loaded so fast that preloader has already completed:
    if "intro-complete" in (body.get_attribute("class") or ""):
        expect(intro).to_be_hidden()
        expect(body).not_to_have_class(re.compile(r'.*\blc-lock\b.*'))
        return
        
    # Verify preloader is visible initially
    expect(intro).to_be_visible()
    
    # Verify body has lc-lock class
    expect(body).to_have_class(re.compile(r'.*\blc-lock\b.*'))
    
    # Wait for the safety net timeout (5s + 2s padding = 7s)
    page.wait_for_timeout(7000)
    
    # Verify preloader is hidden or removed
    intro_hidden = intro.evaluate("el => window.getComputedStyle(el).display == 'none' || window.getComputedStyle(el).opacity == '0'")
    assert intro_hidden or intro.count() == 0, "Expected intro preloader to be hidden or removed after safety timeout"
    
    # Verify scroll is unlocked (lc-lock is removed)
    expect(body).not_to_have_class(re.compile(r'.*\blc-lock\b.*'))

def test_product_hover_cursor(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000')
    try:
        page.locator('#lcSkip').click(timeout=2000)
    except Exception:
        pass
    page.locator('#liceria-intro').wait_for(state="hidden")
    page.wait_for_timeout(2000)
    
    # Hover over the first product card
    card = page.locator('.product-grid .product-card').first
    expect(card).to_be_visible()
    card.hover()
    page.wait_for_timeout(500)
    
    # Check custom cursor follower classes
    cursor_follower = page.locator('.cursor-follower')
    
    # Checking for .drag-mode
    expect(cursor_follower).to_have_class(re.compile(r'.*\bdrag-mode\b.*'))
    
    # Checking for .hover
    # Note: If this fails, it indicates a discrepancy in the implementation
    expect(cursor_follower).to_have_class(re.compile(r'.*\bhover\b.*'))
    
    # Check cursor text is "VIEW"
    cursor_text = page.locator('.cursor-text')
    expect(cursor_text).to_have_text('VIEW')

def test_brew_stepper(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000')
    try:
        page.locator('#lcSkip').click(timeout=2000)
    except Exception:
        pass
    page.locator('#liceria-intro').wait_for(state="hidden")
    page.wait_for_timeout(2000)
    
    # Initially step 1 is active
    step1 = page.locator('.stepper-step[data-step="1"]')
    step2 = page.locator('.stepper-step[data-step="2"]')
    step4 = page.locator('.stepper-step[data-step="4"]')
    
    expect(step1).to_have_class(re.compile(r'.*\bactive\b.*'))
    
    # Wait for autoplay to transition to step 2 (5s limit, wait 6s to be safe)
    page.wait_for_timeout(6000)
    expect(step2).to_have_class(re.compile(r'.*\bactive\b.*'))
    expect(step1).not_to_have_class(re.compile(r'.*\bactive\b.*'))
    
    # Click step 4 manually to override active index
    step4.click()
    page.wait_for_timeout(500)
    expect(step4).to_have_class(re.compile(r'.*\bactive\b.*'))
    expect(step2).not_to_have_class(re.compile(r'.*\bactive\b.*'))
    
    # Wait 6s to see if it auto-advances to step 1 from step 4
    page.wait_for_timeout(6000)
    expect(step1).to_have_class(re.compile(r'.*\bactive\b.*'))
    expect(step4).not_to_have_class(re.compile(r'.*\bactive\b.*'))

def test_testimonials_deck(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000')
    try:
        page.locator('#lcSkip').click(timeout=2000)
    except Exception:
        pass
    page.locator('#liceria-intro').wait_for(state="hidden")
    page.wait_for_timeout(2000)
    
    card0 = page.locator('.testi-card[data-index="0"]')
    card1 = page.locator('.testi-card[data-index="1"]')
    card2 = page.locator('.testi-card[data-index="2"]')
    
    # Verify initial z-indexes
    assert card0.evaluate("el => window.getComputedStyle(el).zIndex") == "3"
    assert card1.evaluate("el => window.getComputedStyle(el).zIndex") == "2"
    assert card2.evaluate("el => window.getComputedStyle(el).zIndex") == "1"
    
    # Scroll next button into view and wait for smooth scroll to settle
    next_btn = page.locator('#nextTesti')
    next_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(1000)
    next_btn.click()
    
    # Check that swipe-out is added immediately
    page.wait_for_timeout(100)
    expect(card0).to_have_class(re.compile(r'.*\bswipe-out\b.*'))
    
    # Wait for the transition to finish (setTimeout is 350ms) by checking when swipe-out is removed
    expect(card0).not_to_have_class(re.compile(r'.*\bswipe-out\b.*'), timeout=5000)
    # Wait another 400ms for the z-index transition delay (300ms) to complete
    page.wait_for_timeout(400)
    
    # Check new z-indexes (card1 is top = 3, card2 is middle = 2, card0 is bottom = 1)
    assert card1.evaluate("el => el.style.zIndex || window.getComputedStyle(el).zIndex") == "3"
    assert card2.evaluate("el => el.style.zIndex || window.getComputedStyle(el).zIndex") == "2"
    assert card0.evaluate("el => el.style.zIndex || window.getComputedStyle(el).zIndex") == "1"
