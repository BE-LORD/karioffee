import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Logo color
css = css.replace('.nav-logo {\n  font-family: var(--font-script);\n  font-size: 32px;\n  color: var(--text-primary);', '.nav-logo {\n  font-family: var(--font-script);\n  font-size: 32px;\n  color: var(--accent-brown);')

# 2. Nav links
css = css.replace('.nav-links a {\n  text-decoration: none;\n  color: var(--text-primary);\n  font-weight: 500;\n  font-size: 14px;', '.nav-links a {\n  text-decoration: none;\n  color: var(--text-primary);\n  font-weight: 400;\n  font-size: 13px;')

# 3. Arrow position
css = css.replace('.hero-arrow {\n  position: absolute;\n  left: 140px;\n  top: 10px;\n}', '.hero-arrow {\n  position: absolute;\n  left: 170px;\n  top: -30px;\n}')

# 4. Cup tilt
css = css.replace('.hero-main-cup {\n  width: 250px;\n  height: auto;\n  position: relative;\n  z-index: 2;\n  transform: rotate(10deg);', '.hero-main-cup {\n  width: 250px;\n  height: auto;\n  position: relative;\n  z-index: 2;\n  transform: rotate(-15deg);')

# 5. 19K Badge
css = css.replace('.hero-badge {\n  position: absolute;\n  bottom: 50px;\n  right: 0px;\n  font-size: 64px;\n  line-height: 1.1;\n  font-weight: 500;', '.hero-badge {\n  position: absolute;\n  bottom: 80px;\n  right: 50px;\n  font-size: 20px;\n  line-height: 1.1;\n  font-weight: 500;')

# 6. Curved Text
css = css.replace('.hero-curved-text {\n  position: absolute;\n  top: -40px;\n  right: -40px;\n  width: 300px;\n  height: 300px;\n  z-index: 3;\n  transform: rotate(20deg);\n}', '.hero-curved-text {\n  position: absolute;\n  top: -10px;\n  right: 10px;\n  width: 240px;\n  height: 240px;\n  z-index: 3;\n  transform: rotate(20deg);\n}')

# 7. Background Pattern
css = css.replace("background: url('../assets/images/hero-pattern.png') center/cover, var(--bg-warm);", "background: url('../assets/images/hero-pattern.png') center/30px, var(--bg-warm);")

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
