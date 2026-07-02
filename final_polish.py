import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Make 19K bolder
css = css.replace('.hero-badge {\n  position: absolute;\n  bottom: 20px;\n  right: -30px;\n  font-size: 48px;\n  line-height: 1.1;\n  font-weight: 500;', '.hero-badge {\n  position: absolute;\n  bottom: 20px;\n  right: -30px;\n  font-size: 48px;\n  line-height: 1.1;\n  font-weight: 800;')

# Make the curved text color lighter so it matches the design (it's greyish brown in design)
css = css.replace('fill: var(--text-primary);', 'fill: var(--text-secondary);')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
