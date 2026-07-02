import re

# ==========================================
# FIX HTML
# ==========================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Navigation
html = html.replace('<span class="nav-logo-sub">premium coffee</span>', '<span class="nav-logo-sub" style="font-family: var(--font-script); font-size: 18px; text-transform: lowercase; letter-spacing: 0;">coffeehouse</span>')

# 2. Hero Section
# Remove hardcoded checkmarks (if any, wait they are not in HTML, maybe CSS? No, they aren't there)
# Fix arrow SVG
old_arrow = '''<div class="hero-arrow">
            <svg viewBox="0 0 200 100" fill="none" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <path d="M 10 80 Q 100 20 180 40" />
              <path d="M 160 30 L 180 40 L 165 55" />
            </svg>
          </div>'''
new_arrow = '''<div class="hero-arrow">
            <svg viewBox="0 0 200 100" fill="none" stroke="#1A1A1A" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
              <path d="M 0 50 Q 80 0 180 50" />
              <path d="M 160 30 L 180 50 L 150 60" />
            </svg>
          </div>'''
html = html.replace(old_arrow, new_arrow)

# 3. Explore Recent Products
# Fix subtitle
html = html.replace('Our collection of premium coffee products is carefully curated to offer you the best brewing experience, from single-origin beans to expertly blended varieties that bring out unique flavors in every cup.', 'Our dedicated team creates unique espresso drinks, house specialties, and smoothies to fit every taste.')
# Remove 'Made By: '
html = html.replace('Made By: Italian', 'Italian')
html = html.replace('Made By: Viennese', 'Viennese')
html = html.replace('Made By: New Orleans', 'New Orleans')
html = html.replace('Made By: Moroccan', 'Moroccan')

# 4. Discover the Best Coffee
html = html.replace('helps build your stamina', 'helps build your mood')
html = html.replace('taste you have ever tasted', 'taste more than others you have ever tasted')
html = html.replace('<p>Somi Brans is a coffee shop that provides you with quality coffee that helps boost your productivity and, it is perfectly safe to be drunk at anytime of the day.</p>', '')
html = html.replace('Get It More', 'Get It Now')

# 5. Coffee Made Easy
html = html.replace('Coffee packs are specially packed for easy to create anytime or anyplace making it on the go.', 'Coffee packs are specially packed for easy to create anytime or anyplace to maintain freshness.')
html = html.replace('Coffee sacks are specially packed of 100% eco-friendly material ensuring sustainability.', 'Coffee sacks are specially packed of 100% eco-friendly material ensuring sustainability to maintain freshness.')

# 6. Testimonials
html = html.replace("As a coffee lover, I've tried several brands, but none can ever compare to Somi brand and this company. I love their blends and the smoothness of each cup I have been drinking for years at this coffee shop. The quality is exceptional. It's like starting every morning on the right track with a perfectly crafted cup of coffee.", "As a coffee lover, I've tried several brands, but none can ever compare to Somi brand and this company. I love their blends and the smoothness of each cup I have been drinking for years at this coffee shop. The quality is exceptional.")

# 7. Newsletter
html = html.replace('Subscribe to our newsletter and get 25% discount code.', 'Subscribe to our newsletter and get %25 OFF discount code.')

# 8. Footer
html = html.replace('Crafted with passion, brewed to perfection. Every cup, a new adventure.', 'Experience premium coffee delivered to your doorstep. Follow us to enhance your daily brewing joy on demand.')

# JS Bug Fix: update hero-stat-value to stat-number with data attributes
html = html.replace('<div class="hero-stat-value">+1000</div>', '<div class="stat-number hero-stat-value" data-target="1000" data-prefix="+">0</div>')
html = html.replace('<div class="hero-stat-value">+7400</div>', '<div class="stat-number hero-stat-value" data-target="7400" data-prefix="+">0</div>')
html = html.replace('<div class="hero-stat-value">+2000</div>', '<div class="stat-number hero-stat-value" data-target="2000" data-prefix="+">0</div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# ==========================================
# FIX CSS
# ==========================================
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Navigation
css = css.replace('.navbar {\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  z-index: 1000;\n  background: rgba(255, 255, 255, 0.95);\n  backdrop-filter: blur(10px);\n  -webkit-backdrop-filter: blur(10px);\n  border-bottom: 1px solid var(--border-light);\n  transition: box-shadow var(--transition-normal);\n}', '.navbar {\n  position: fixed;\n  top: 0;\n  left: 0;\n  right: 0;\n  z-index: 1000;\n  background: transparent;\n  transition: all var(--transition-normal);\n}\n.navbar.scrolled { background: #fff; box-shadow: 0 2px 20px rgba(0,0,0,0.08); }')
css = css.replace('.nav-icons button {\n  width: 40px;\n  height: 40px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-radius: var(--radius-full);\n  transition: background var(--transition-fast);\n  color: var(--text-primary);\n}', '.nav-icons button {\n  width: 40px;\n  height: 40px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  border-radius: var(--radius-full);\n  border: 1px solid var(--border-light);\n  transition: background var(--transition-fast);\n  color: var(--text-primary);\n}')

# 2. Hero Section
css = css.replace('.hero-content h1 {\n  font-family: var(--font-sans);', '.hero-content h1 {\n  font-family: var(--font-serif);')
css = css.replace('.hero-arrow {\n  position: absolute;\n  left: 170px;\n  top: 10px;\n}', '.hero-arrow {\n  position: absolute;\n  left: 160px;\n  top: 5px;\n}')
css = css.replace('justify-content: center;\n}', 'justify-content: center;\n  background: radial-gradient(circle at 30% 70%, #f1e9df 0%, #f9f6f3 100%);\n}')
css = css.replace('padding: 10px 24px;', 'padding: 12px 32px;') # Wider button

# 3. Explore Recent Products
css = css.replace('.section-title {\n  font-family: var(--font-serif);', '.section-title {\n  font-family: var(--font-sans);')
css = css.replace('.product-card-image {\n  background: var(--bg-warm-light);\n  padding: 24px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 220px;\n  position: relative;\n  overflow: hidden;\n}', '.product-card-image {\n  background: #fff;\n  padding: 24px;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 220px;\n  position: relative;\n  overflow: hidden;\n  margin: 10px;\n  border-radius: var(--radius-md);\n}')
# Inner backgrounds for products
css = css.replace('.product-card:nth-child(1) .product-card-image { background: #f6f4e6; }', '.product-card:nth-child(1) .product-card-image { background: #f6f4e6; }') # Already there, but need to be inside margin
# Flex row for origin and price
css = css.replace('.product-price {\n  font-size: 14px;\n  font-weight: 600;\n  color: var(--text-primary);\n  margin-bottom: 16px;\n}', '.product-price {\n  font-size: 14px;\n  font-weight: 600;\n  color: var(--text-primary);\n}')
css = css.replace('.product-body-top {', '.product-body-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }') # We'll wrap in HTML later if needed, actually let's just make product-name inline-block
css = css.replace('.product-name {\n  font-family: var(--font-sans);\n  font-size: 13px;\n  color: var(--text-secondary);\n  margin-bottom: 2px;\n}', '.product-name {\n  font-family: var(--font-sans);\n  font-size: 14px;\n  font-weight: 600;\n  color: var(--text-primary);\n}')

# 4. Discover the Best Coffee
css = css.replace('.btn-let-more {\n  display: inline-block;\n  background: var(--accent-green);', '.btn-let-more {\n  display: inline-block;\n  background: var(--accent-brown);')

# 5. Fix Invisible Sections (Scroll animation override to ensure visibility)
css = css.replace('.animate-on-scroll {\n  opacity: 0;\n  transform: translateY(30px);', '.animate-on-scroll {\n  opacity: 1;\n  transform: none;')

# 7. Newsletter pill shape
css = css.replace('border-radius: var(--radius-xl) 0 0 var(--radius-xl);', 'border-radius: 50px 0 0 50px;')
css = css.replace('border-radius: 0 var(--radius-xl) var(--radius-xl) 0;', 'border-radius: 0 50px 50px 0;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
