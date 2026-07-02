import os
import re

html_path = r'c:\Users\pr7n8\Downloads\anti coffee\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace missing images with inline SVGs or existing images
# 1. coffee-bean
bean_svg = '''<svg viewBox="0 0 24 24" fill="#B87B44" stroke="#B87B44" stroke-width="1"><path d="M10 2c-4 0-7 3-7 7 0 6 9 13 9 13s9-7 9-13c0-4-3-7-7-7a7 7 0 0 0-4 0Z"></path><path d="M14 6c-3 2-6 7-6 10" stroke="white" stroke-width="1.5"></path></svg>'''
content = re.sub(r'<img src="assets/images/coffee-bean-(\d+)\.png" alt="Bean" class="(.*?)" data-speed="(.*?)">',
                 r'<div class="\2" data-speed="\3" style="width: \10px; height: \10px;">' + bean_svg + r'</div>', content)

# 2. newsletter-beans (missing) -> Use discover-coffee-bag.png instead
content = content.replace('assets/images/newsletter-beans.png', 'assets/images/discover-coffee-bag.png')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

css_path = r'c:\Users\pr7n8\Downloads\anti coffee\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

# Replace leaf-pattern.png with hero-pattern.png
css_content = css_content.replace("url('../assets/images/leaf-pattern.png')", "url('../assets/images/hero-pattern.png')")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_content)

print('Replaced missing images in HTML and CSS.')
