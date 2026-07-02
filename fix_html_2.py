import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix heading line breaks
html = html.replace('<h1>Enhance Your Coffee <br>Experience With Us</h1>', '<h1>Enhance Your Coffee<br>Experience With</h1>')
html = html.replace('<h1>Enhance Your Coffee<br>Experience With</h1>', '<h1>Enhance Your Coffee<br>Experience With</h1>') # Just to be sure

# Fix avatars
old_avatars = '''<img src="assets/images/avatar-a.png" alt="Happy customer 1" style="z-index: 1;">
            <img src="assets/images/avatar-b.png" alt="Happy customer 2" style="z-index: 2;">
            <img src="assets/images/avatar-c.png" alt="Happy customer 3" style="z-index: 3;">
            <img src="assets/images/avatar-a.png" alt="Happy customer 4" style="z-index: 4; transform: scaleX(-1);">'''
new_avatars = '''<img src="assets/images/avatar-1.png" alt="Happy customer 1" style="z-index: 1;">
            <img src="assets/images/avatar-2.png" alt="Happy customer 2" style="z-index: 2;">
            <img src="assets/images/avatar-3.png" alt="Happy customer 3" style="z-index: 3;">
            <img src="assets/images/avatar-4.png" alt="Happy customer 4" style="z-index: 4;">'''
html = html.replace(old_avatars, new_avatars)

# Fix Arrow (swoops UPWARDS to the cup)
old_arrow = '''<div class="hero-arrow">
            <svg viewBox="0 0 200 100" fill="none" stroke="#1A1A1A" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M 10 20 Q 80 -30 180 80" />
              <path d="M 150 70 L 180 80 L 160 50" />
            </svg>
          </div>'''
new_arrow = '''<div class="hero-arrow">
            <svg viewBox="0 0 200 100" fill="none" stroke="#1A1A1A" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">
              <path d="M 10 80 Q 80 120 180 20" />
              <path d="M 150 30 L 180 20 L 170 50" />
            </svg>
          </div>'''
html = html.replace(old_arrow, new_arrow)

# Fix curved text
old_svg_text = '''<svg viewBox="0 0 300 300">
              <path id="curve" d="M 50 150 A 100 100 0 0 1 250 150" fill="transparent" />
              <text>
                <textPath href="#curve" startOffset="50%" text-anchor="middle">
                  Top selling coffee product
                </textPath>
              </text>
            </svg>'''
new_svg_text = '''<svg viewBox="0 0 240 240">
              <path id="curve" d="M 20 120 A 100 100 0 0 1 220 120" fill="transparent" />
              <text>
                <textPath href="#curve" startOffset="50%" text-anchor="middle">
                  Top selling coffee product
                </textPath>
              </text>
            </svg>'''
html = html.replace(old_svg_text, new_svg_text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
