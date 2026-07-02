import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Adjust 19K badge to move it a bit down
css = css.replace('.hero-badge {\n  position: absolute;\n  bottom: 20px;\n  right: -30px;\n  font-size: 48px;\n  line-height: 1.1;\n  font-weight: 800;', '.hero-badge {\n  position: absolute;\n  bottom: 0px;\n  right: -20px;\n  font-size: 48px;\n  line-height: 1.1;\n  font-weight: 800;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
