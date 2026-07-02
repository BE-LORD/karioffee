import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Discover Image
html = re.sub(
    r'<img src="assets/images/discover-coffee-bag.png".*?>',
    '''<div class="discover-cups">
              <img src="assets/images/italian-coffee.png" class="discover-cup discover-cup-1" alt="Cup">
              <img src="assets/images/viennese-coffee.png" class="discover-cup discover-cup-2" alt="Cup">
              <img src="assets/images/new-orleans-coffee.png" class="discover-cup discover-cup-3" alt="Cup">
            </div>''',
    html,
    flags=re.DOTALL
)

# Fix Hero Right Image
html = re.sub(
    r'<img src="assets/images/coffee-cups-stack.png".*?>',
    '''<div class="hero-stacked-cups">
              <img src="assets/images/italian-coffee.png" class="hero-stack hero-stack-1" alt="Cup">
              <img src="assets/images/viennese-coffee.png" class="hero-stack hero-stack-2" alt="Cup">
              <img src="assets/images/new-orleans-coffee.png" class="hero-stack hero-stack-3" alt="Cup">
            </div>''',
    html,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Fix CSS section titles
with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'\.section-title\s*\{\s*font-family:\s*var\(--font-sans\);', '.section-title {\n  font-family: var(--font-serif);', css)

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Images replaced using regex and css fonts fixed")
