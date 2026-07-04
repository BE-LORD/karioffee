import os
import sys
from playwright.sync_api import sync_playwright

def main():
    print("Starting Playwright debug...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        errors = []
        page.on("console", lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: errors.append(f"PAGE_ERROR: {err}"))
        
        print("Navigating to http://localhost:8000 ...")
        page.goto('http://localhost:8000')
        page.wait_for_timeout(2000)
        
        try:
            print("Clicking skip button if visible...")
            skip_btn = page.locator('#lcSkip')
            if skip_btn.is_visible():
                skip_btn.click()
                print("Clicked skip button.")
            else:
                print("Skip button not visible.")
        except Exception as e:
            print(f"Error clicking skip: {e}")
            
        print("Waiting for intro to hide...")
        try:
            page.locator('#liceria-intro').wait_for(state="hidden", timeout=10000)
            print("Intro is hidden.")
        except Exception as e:
            print(f"Error waiting for intro hide: {e}")
            
        cards = page.locator('.product-grid .product-card')
        print(f"Product cards count: {cards.count()}")
        for i in range(cards.count()):
            print(f"Card {i}: {cards.nth(i).inner_text()[:60]}...")
            
        print(f"Console errors/warnings: {len(errors)}")
        for err in errors:
            print(err)
            
        browser.close()

if __name__ == "__main__":
    main()
