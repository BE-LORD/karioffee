import os

html_path = r'c:\Users\pr7n8\Downloads\anti coffee\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'assets/images/hero-cup.png': 'assets/images/hero-coffee-cup.png',
    'assets/images/product-1.png': 'assets/images/italian-coffee.png',
    'assets/images/product-2.png': 'assets/images/viennese-coffee.png',
    'assets/images/product-3.png': 'assets/images/new-orleans-coffee.png',
    'assets/images/product-4.png': 'assets/images/moroccan-coffee.png',
    'assets/images/stacked-cups.png': 'assets/images/coffee-cups-stack.png',
    'assets/images/pink-cup.png': 'assets/images/coffee-easy-cup.png',
    'assets/images/latte-art.png': 'assets/images/newsletter-latte.png'
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html with correct image paths.')
