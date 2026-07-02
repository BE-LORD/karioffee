import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix arrow svg
old_arrow = '''<div class="hero-arrow">
            <svg viewBox="0 0 200 100" fill="none" stroke="#1A1A1A" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
              <path d="M 10 80 Q 80 120 180 20" />
              <path d="M 150 30 L 180 20 L 170 50" />
            </svg>
          </div>'''
new_arrow = '''<div class="hero-arrow">
            <svg viewBox="0 0 200 100" fill="none" stroke="#1A1A1A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <path d="M 10 80 Q 100 20 180 40" />
              <path d="M 160 30 L 180 40 L 165 55" />
            </svg>
          </div>'''
html = html.replace(old_arrow, new_arrow)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
