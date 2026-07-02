import os
import re

html_path = r'c:\Users\pr7n8\Downloads\anti coffee\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace missing images with inline SVGs or existing images
bean_svg = '''<svg viewBox="0 0 24 24" fill="#B87B44" stroke="#B87B44" stroke-width="1" style="width:100%; height:100%;"><path d="M10 2c-4 0-7 3-7 7 0 6 9 13 9 13s9-7 9-13c0-4-3-7-7-7a7 7 0 0 0-4 0Z"></path><path d="M14 6c-3 2-6 7-6 10" stroke="white" stroke-width="1.5"></path></svg>'''
content = re.sub(r'<img src="assets/images/coffee-bean-\d+\.png" alt="Bean" class="(.*?)" data-speed="(.*?)">',
                 r'<div class="\1" data-speed="\2" style="width: 60px; height: 60px;">' + bean_svg + r'</div>', content)

content = content.replace('assets/images/newsletter-beans.png', 'assets/images/discover-coffee-bag.png')

# 2. Remove lenis css link
content = re.sub(r'<link rel="stylesheet" href="https://unpkg.com/lenis.*?">', '', content)

# 3. Add id/name to email input
content = content.replace('<input type="email" placeholder="Enter your email address" required>',
                          '<input type="email" id="email" name="email" placeholder="Enter your email address" required>')

# 4. Fix Footer SVGs
# Footer SVG 1 (Facebook/Twitter/etc? - replacing all with standard simple ones to be safe from malformed paths)
new_socials = '''<a href="#" class="hover-target magnetic" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg></a>
            <a href="#" class="hover-target magnetic" aria-label="Twitter"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg></a>
            <a href="#" class="hover-target magnetic" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>
            <a href="#" class="hover-target magnetic" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg></a>'''
            
content = re.sub(r'<div class="socials">.*?</div>', r'<div class="socials">' + new_socials + r'</div>', content, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

css_path = r'c:\Users\pr7n8\Downloads\anti coffee\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace leaf-pattern.png with hero-pattern.png
css_content = css_content.replace("url('../assets/images/leaf-pattern.png')", "url('../assets/images/hero-pattern.png')")

# Add Lenis basic CSS
lenis_css = '''
html.lenis, html.lenis body {
  height: auto;
}
.lenis.lenis-smooth {
  scroll-behavior: auto !important;
}
.lenis.lenis-smooth [data-lenis-prevent] {
  overscroll-behavior: contain;
}
.lenis.lenis-stopped {
  overflow: hidden;
}
.lenis.lenis-smooth iframe {
  pointer-events: none;
}
'''
if 'html.lenis' not in css_content:
    css_content += lenis_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print('Fixed all audit issues.')
