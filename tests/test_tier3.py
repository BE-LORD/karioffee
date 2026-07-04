import pytest
import re
from playwright.sync_api import expect

def test_nav_scroll(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000', wait_until='networkidle')
    try:
        page.locator('#lcSkip').click(timeout=2000)
    except Exception:
        pass
    page.locator('#liceria-intro').wait_for(state="hidden")
    
    # Wait for initial load and Lenis setup
    page.wait_for_timeout(2000)
    
    links = {
        "#shop": 'a[href="#shop"]',
        "#about": 'a[href="#about"]',
        "#ritual": 'a[href="#ritual"]',
        "#contact": 'a[href="#contact"]'
    }
    
    for target_id, selector in links.items():
        # Find link and click it
        link = page.locator(selector).first
        expect(link).to_be_visible()
        link.click()
        
        # Wait for Lenis smooth scroll to settle
        page.wait_for_timeout(2500)
        
        # Check target position
        target = page.locator(target_id)
        box = target.bounding_box()
        assert box is not None, f"Target {target_id} bounding box is None"
        # The top of the section should be within 150px of the viewport top
        assert abs(box['y']) < 150, f"Section '{target_id}' did not scroll to top. Bounding box: {box}"

def test_nav_links_active_state(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000', wait_until='networkidle')
    try:
        page.locator('#lcSkip').click(timeout=2000)
    except Exception:
        pass
    page.locator('#liceria-intro').wait_for(state="hidden")
    page.wait_for_timeout(2000)
    
    # Home link should be active initially
    home_link = page.locator('#navLinks a[href="#home"]')
    expect(home_link).to_have_class(re.compile(r'.*\bactive\b.*'))
    
    # Click shop link
    shop_link = page.locator('#navLinks a[href="#shop"]')
    shop_link.click()
    page.wait_for_timeout(2500)
    
    # Verify active class shifted to shop link
    expect(shop_link).to_have_class(re.compile(r'.*\bactive\b.*'))
    expect(home_link).not_to_have_class(re.compile(r'.*\bactive\b.*'))

def test_theme_shifts(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000')
    try:
        page.locator('#lcSkip').click(timeout=2000)
    except Exception:
        pass
    page.locator('#liceria-intro').wait_for(state="hidden")
    page.wait_for_timeout(2000)
    
    body = page.locator('body')
    
    # 1. Scroll to #home
    page.locator('#home').scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    expect(body).to_have_class(re.compile(r'.*\btheme-espresso\b.*'))
    
    # 2. Scroll to #shop
    page.locator('#shop').scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    expect(body).to_have_class(re.compile(r'.*\btheme-crema\b.*'))
    
    # 3. Scroll to #about
    page.locator('#about').scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    expect(body).to_have_class(re.compile(r'.*\btheme-moss\b.*'))
    
    # 4. Scroll to #ritual
    page.locator('#ritual').scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    expect(body).to_have_class(re.compile(r'.*\btheme-crema\b.*'))
    
    # 5. Scroll to #blog
    page.locator('#blog').scroll_into_view_if_needed()
    page.wait_for_timeout(1500)
    expect(body).to_have_class(re.compile(r'.*\btheme-espresso\b.*'))
