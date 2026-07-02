import pytest
from playwright.sync_api import expect

def test_z_indexes(page):
    page.goto('http://localhost:8000')
    
    # Check intro screen z-index before skip
    intro = page.locator('#liceria-intro')
    expect(intro).to_be_attached()
    intro_z = intro.evaluate("el => window.getComputedStyle(el).zIndex")
    assert intro_z == "10000", f"Expected #liceria-intro z-index to be 10000, but got {intro_z}"
    
    # Check other z-indexes
    cursor = page.locator('.cursor')
    cursor_follower = page.locator('.cursor-follower')
    nav_mobile_btn = page.locator('.nav-mobile-btn')
    navbar = page.locator('nav.navbar')
    bg3d = page.locator('#bg3dCanvas')
    
    assert cursor.evaluate("el => window.getComputedStyle(el).zIndex") == "9999"
    assert cursor_follower.evaluate("el => window.getComputedStyle(el).zIndex") == "9998"
    assert nav_mobile_btn.evaluate("el => window.getComputedStyle(el).zIndex") == "1001"
    assert navbar.evaluate("el => window.getComputedStyle(el).zIndex") == "1000"
    assert bg3d.evaluate("el => window.getComputedStyle(el).zIndex") == "-1"

def test_viewport_375(page):
    page.set_viewport_size({"width": 375, "height": 800})
    page.goto('http://localhost:8000')
    page.locator('#lcSkip').click()
    page.locator('#liceria-intro').wait_for(state="hidden")
    
    # .nav-icons should be hidden
    nav_icons = page.locator('.nav-icons')
    is_nav_icons_hidden = nav_icons.evaluate("el => window.getComputedStyle(el).display == 'none' || window.getComputedStyle(el).visibility == 'hidden'")
    assert is_nav_icons_hidden, "Expected .nav-icons to be hidden at 375px"
    
    # .nav-mobile-btn should be visible
    nav_mobile_btn = page.locator('.nav-mobile-btn')
    is_mobile_btn_visible = nav_mobile_btn.evaluate("el => window.getComputedStyle(el).display != 'none' && window.getComputedStyle(el).visibility != 'hidden'")
    assert is_mobile_btn_visible, "Expected .nav-mobile-btn to be visible at 375px"
    
    # Custom cursors should be hidden
    cursor = page.locator('.cursor')
    cursor_follower = page.locator('.cursor-follower')
    cursor_hidden = cursor.evaluate("el => window.getComputedStyle(el).display == 'none' || window.getComputedStyle(el).opacity == '0'")
    follower_hidden = cursor_follower.evaluate("el => window.getComputedStyle(el).display == 'none' || window.getComputedStyle(el).opacity == '0'")
    assert cursor_hidden and follower_hidden, "Expected custom cursors to be hidden at 375px"
    
    # Stacked layout: check product cards y-positions
    cards = page.locator('.product-grid .product-card')
    count = cards.count()
    if count >= 2:
        y0 = cards.nth(0).bounding_box()['y']
        y1 = cards.nth(1).bounding_box()['y']
        assert y1 > y0, "Expected stacked vertical layout for product cards at 375px"

def test_viewport_768(page):
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto('http://localhost:8000')
    page.locator('#lcSkip').click()
    page.locator('#liceria-intro').wait_for(state="hidden")
    
    # .product-grid is 2 columns
    # Verify by getting the number of columns in gridTemplateColumns
    grid_cols = page.locator('.product-grid').evaluate("el => window.getComputedStyle(el).gridTemplateColumns")
    cols_count = len(grid_cols.strip().split())
    assert cols_count == 2, f"Expected 2 columns for .product-grid at 768px, but got '{grid_cols}' (count={cols_count})"
    
    # .footer-grid is 3 columns
    footer_cols = page.locator('.footer-grid').evaluate("el => window.getComputedStyle(el).gridTemplateColumns")
    footer_cols_count = len(footer_cols.strip().split())
    assert footer_cols_count == 3, f"Expected 3 columns for .footer-grid at 768px, but got '{footer_cols}' (count={footer_cols_count})"

def test_viewport_1440(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto('http://localhost:8000')
    page.locator('#lcSkip').click()
    page.locator('#liceria-intro').wait_for(state="hidden")
    
    # .nav-icons should be visible
    nav_icons = page.locator('.nav-icons')
    is_nav_icons_visible = nav_icons.evaluate("el => window.getComputedStyle(el).display != 'none' && window.getComputedStyle(el).visibility != 'hidden'")
    assert is_nav_icons_visible, "Expected .nav-icons to be visible at 1440px"
    
    # .nav-mobile-btn should be hidden
    nav_mobile_btn = page.locator('.nav-mobile-btn')
    is_mobile_btn_hidden = nav_mobile_btn.evaluate("el => window.getComputedStyle(el).display == 'none' || window.getComputedStyle(el).visibility == 'hidden'")
    assert is_mobile_btn_hidden, "Expected .nav-mobile-btn to be hidden at 1440px"
    
    # Custom cursors should be visible
    cursor = page.locator('.cursor')
    cursor_follower = page.locator('.cursor-follower')
    cursor_visible = cursor.evaluate("el => window.getComputedStyle(el).display != 'none'")
    follower_visible = cursor_follower.evaluate("el => window.getComputedStyle(el).display != 'none'")
    assert cursor_visible and follower_visible, "Expected custom cursors to be visible at 1440px"
    
    # product grid is 4 columns
    grid_cols = page.locator('.product-grid').evaluate("el => window.getComputedStyle(el).gridTemplateColumns")
    cols_count = len(grid_cols.strip().split())
    assert cols_count == 4, f"Expected 4 columns for .product-grid at 1440px, but got '{grid_cols}'"
    
    # footer grid is 6 columns
    footer_cols = page.locator('.footer-grid').evaluate("el => window.getComputedStyle(el).gridTemplateColumns")
    footer_cols_count = len(footer_cols.strip().split())
    assert footer_cols_count == 6, f"Expected 6 columns for .footer-grid at 1440px, but got '{footer_cols}'"

def test_console_logs(page):
    errors = []
    page.on("console", lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ["error", "warning"] else None)
    page.on("pageerror", lambda err: errors.append(f"PAGE_ERROR: {err}"))
    
    page.goto('http://localhost:8000')
    page.locator('#lcSkip').click()
    page.locator('#liceria-intro').wait_for(state="hidden")
    page.wait_for_timeout(2000)
    
    assert len(errors) == 0, f"Detected console errors/warnings: {errors}"
