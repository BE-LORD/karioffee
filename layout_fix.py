import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Remove min-height: 100vh from .hero and fix padding
css = re.sub(r'min-height:\s*100vh;', '', css)
css = re.sub(r'\.hero \{\s*background:[^}]+padding:[^;]+;', lambda m: m.group(0).replace(m.group(0).split('padding:')[1], ' 120px 0 60px;'), css)

# 2. Hero Grid adjustments
css = css.replace('grid-template-columns: 1.2fr auto 1fr;', 'grid-template-columns: 1fr 340px 1fr;')

# 3. Center Area Adjustments
css = css.replace('width: 420px;\n  height: 420px;', 'width: 340px;\n  height: 340px;')
css = css.replace('width: 250px;\n  height: auto;\n  position: relative;\n  z-index: 2;\n  transform: rotate(-15deg);', 'width: 300px;\n  height: auto;\n  position: relative;\n  z-index: 2;\n  transform: rotate(-10deg); margin-top: -20px;')

# 19K Badge Position
css = css.replace('.hero-badge {\n  position: absolute;\n  bottom: 80px;\n  right: 50px;\n  font-size: 20px;', '.hero-badge {\n  position: absolute;\n  bottom: 20px;\n  right: -30px;\n  font-size: 48px;')

# Curved text
css = css.replace('.hero-curved-text {\n  position: absolute;\n  top: -10px;\n  right: 10px;\n  width: 240px;\n  height: 240px;', '.hero-curved-text {\n  position: absolute;\n  top: -30px;\n  right: -30px;\n  width: 400px;\n  height: 400px;')

# 4. Right Area Adjustments
css = css.replace('.hero-right-area {\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: flex-end;\n  padding-right: 20px;\n  gap: 40px;\n  margin-top: -80px;\n}', '.hero-right-area {\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n  align-items: flex-end;\n  height: 340px;\n  padding-top: 20px;\n}')
css = css.replace('.hero-small-cups img {\n  width: 280px;', '.hero-small-cups img {\n  width: 220px;')

# 5. Left Area Adjustments
css = css.replace('font-size: 44px;', 'font-size: 48px;')
css = css.replace('left: 170px;\n  top: -30px;', 'left: 170px;\n  top: 10px;')

# Background pattern
css = css.replace('center/30px', 'center/400px')
css = css.replace('background-blend-mode: multiply;', '') # It makes the background too dark/dirty sometimes

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
