import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("DISCOVER IMAGE:")
match1 = re.search(r'<div class="discover-image-container">.*?</div>\s*</div>', html, re.DOTALL)
if match1:
    print(match1.group(0))

print("\nHERO IMAGE:")
match2 = re.search(r'<div class="hero-image-container">.*?</div>\s*</div>', html, re.DOTALL)
if match2:
    print(match2.group(0))
