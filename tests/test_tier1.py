import os
import urllib.request
import urllib.error
from html.parser import HTMLParser
import pytest
from playwright.sync_api import expect

class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'img' and 'src' in attrs_dict:
            self.assets.append(attrs_dict['src'])
        elif tag == 'link' and 'href' in attrs_dict:
            self.assets.append(attrs_dict['href'])
        elif tag == 'script' and 'src' in attrs_dict:
            self.assets.append(attrs_dict['src'])

def test_key_sections_exist(page):
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    
    sections = {
        "Intro screen": "#liceria-intro",
        "Navbar": "nav.navbar",
        "Hero": "section.hero",
        "Marquee": "section.marquee-section",
        "Products grid": ".product-grid",
        "Discover": "section.discover",
        "Brew stepper": ".stepper-layout",
        "Testimonials": ".testi-deck",
        "Newsletter": "section.newsletter",
        "Footer": "footer.footer"
    }
    
    for name, selector in sections.items():
        assert page.locator(selector).count() > 0, f"Section '{name}' with selector '{selector}' was not found."

def test_header_navigation_links(page):
    page.goto('http://localhost:8000')
    page.wait_for_load_state('networkidle')
    
    nav_links = page.locator('#navLinks a')
    count = nav_links.count()
    assert count > 0, "No navigation links found in #navLinks"
    
    hrefs = [nav_links.nth(i).get_attribute('href') for i in range(count)]
    required_hrefs = ["#home", "#shop", "#about", "#ritual", "#contact"]
    
    for req in required_hrefs:
        assert req in hrefs, f"Required navigation link '{req}' was not found in header navigation."

def test_skip_preloader(page):
    page.goto('http://localhost:8000')
    
    # Check that body has 'lc-lock' class before skip
    body = page.locator('body')
    expect(body).to_have_class(r'.*\blc-lock\b.*')
    
    # Click skip intro button
    skip_btn = page.locator('#lcSkip')
    expect(skip_btn).to_be_visible()
    skip_btn.click()
    
    # Wait for the intro screen to be hidden or removed
    intro = page.locator('#liceria-intro')
    intro.wait_for(state="hidden", timeout=5000)
    
    # Check that 'lc-lock' is removed from body
    expect(body).not_to_have_class(r'.*\blc-lock\b.*')

def test_product_cards_count(page):
    page.goto('http://localhost:8000')
    # Skip preloader first
    page.locator('#lcSkip').click()
    page.locator('#liceria-intro').wait_for(state="hidden")
    
    cards = page.locator('.product-grid .product-card')
    assert cards.count() == 4, f"Expected 4 product cards, but found {cards.count()}."

def test_testimonials_cards_count(page):
    page.goto('http://localhost:8000')
    page.locator('#lcSkip').click()
    page.locator('#liceria-intro').wait_for(state="hidden")
    
    testimonials = page.locator('.testi-deck .testi-card')
    assert testimonials.count() == 3, f"Expected 3 testimonials cards, but found {testimonials.count()}."

def test_static_assets_resolve():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(test_dir)
    index_html_path = os.path.join(project_dir, 'index.html')
    
    with open(index_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    parser = AssetParser()
    parser.feed(html_content)
    
    base_url = 'http://localhost:8000/'
    failed_assets = []
    
    for asset in parser.assets:
        # Ignore empty src/href or placeholders
        if not asset or asset.startswith('#') or asset.startswith('javascript:'):
            continue
            
        # Build absolute URL to test
        if asset.startswith('http://') or asset.startswith('https://'):
            url = asset
        else:
            url = base_url + asset
            
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                if status == 404:
                    failed_assets.append((asset, 404))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                failed_assets.append((asset, 404))
        except Exception as e:
            # If it's an external URL, connection might fail in CODE_ONLY mode,
            # which is not a 404. We only fail on actual 404.
            if not (asset.startswith('http://') or asset.startswith('https://')):
                failed_assets.append((asset, str(e)))
                
    assert len(failed_assets) == 0, f"Some static assets failed to resolve: {failed_assets}"
