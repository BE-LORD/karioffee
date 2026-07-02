import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Navbar
css = css.replace('.logo {', '.logo {\n  color: var(--accent-brown);')
css = css.replace('font-size: 11px;\n  letter-spacing: 4px;', 'font-size: 8px;\n  letter-spacing: 2px;')
css = css.replace('.nav-links a {\n  text-decoration: none;\n  color: var(--text-primary);\n  font-weight: 500;\n  font-size: 15px;\n  transition: color 0.3s ease;\n}', '.nav-links a {\n  text-decoration: none;\n  color: var(--text-primary);\n  font-weight: 500;\n  font-size: 14px;\n  margin: 0 10px;\n  transition: color 0.3s ease;\n}')
css = css.replace('.nav-icons {\n  display: flex;\n  align-items: center;\n  gap: 24px;\n}', '.nav-icons {\n  display: flex;\n  align-items: center;\n  gap: 15px;\n}')

# Add nav-container style if needed
css += "\n.nav-container { display: flex; align-items: center; justify-content: space-between; width: 100%; }\n"

# 2. Left Text Area
css = css.replace('font-size: 56px;', 'font-size: 44px;')
css = re.sub(r'(.hero-content p {[^}]+font-size: )14px;', r'\g<1>13px;', css)
css = css.replace('.btn-discover {\n  display: inline-block;\n  background: var(--accent-brown);\n  color: var(--text-white);\n  font-size: 14px;\n  font-weight: 600;\n  padding: 12px 32px;\n  border-radius: var(--radius-xl);', '.btn-discover {\n  display: inline-block;\n  background: var(--accent-brown);\n  color: var(--text-white);\n  font-size: 13px;\n  font-weight: 600;\n  padding: 10px 24px;\n  border-radius: 50px;')
css = css.replace('.hero-avatars img {\n  width: 36px;\n  height: 36px;', '.hero-avatars img {\n  width: 28px;\n  height: 28px;\n  background: transparent;')
css = css.replace('.avatar-badge {\n  width: 36px;\n  height: 36px;\n  border-radius: var(--radius-full);\n  background: #2980b9;\n  color: #ffffff;\n  font-size: 11px;', '.avatar-badge {\n  width: 28px;\n  height: 28px;\n  border-radius: var(--radius-full);\n  background: #9bb7c7;\n  color: #ffffff;\n  font-size: 9px;')

css = css.replace('.hero-users {\n  display: flex;\n  align-items: center;\n  gap: 12px;\n  margin-top: 32px;\n}', '.hero-users {\n  display: flex;\n  align-items: center;\n  gap: 12px;\n  margin-top: 32px;\n  position: relative;\n}')
css = css.replace('.hero-arrow {\n  display: flex;\n  align-items: center;\n  margin-left: 8px;\n}', '.hero-arrow {\n  position: absolute;\n  left: 140px;\n  top: 10px;\n}')
css = css.replace('.hero-arrow svg {\n  width: 80px;\n  height: 80px;', '.hero-arrow svg {\n  width: 120px;\n  height: 60px;')

# 3. Center Area
css = css.replace('.hero-main-cup {\n  width: 250px;\n  height: auto;\n  position: relative;\n  z-index: 2;\n  transform: rotate(-10deg);', '.hero-main-cup {\n  width: 250px;\n  height: auto;\n  position: relative;\n  z-index: 2;\n  transform: rotate(10deg);')
css = css.replace('.hero-badge {\n  position: absolute;\n  bottom: 100px;\n  right: 120px;', '.hero-badge {\n  position: absolute;\n  bottom: 50px;\n  right: 0px;')
css = css.replace('.hero-curved-text {\n  position: absolute;\n  top: -10px;\n  right: 10px;\n  width: 220px;\n  height: 220px;', '.hero-curved-text {\n  position: absolute;\n  top: -40px;\n  right: -40px;\n  width: 300px;\n  height: 300px;')

# 4. Right Area
css = css.replace('.hero-small-cups img {\n  width: 180px;', '.hero-small-cups img {\n  width: 280px;')
css = css.replace('.hero-stats {\n  display: flex;\n  gap: 40px;\n  align-items: center;\n}', '.hero-stats {\n  display: flex;\n  gap: 20px;\n  align-items: center;\n}')
css = css.replace('.stat-number {\n  display: block;\n  font-size: 36px;', '.stat-number {\n  display: block;\n  font-size: 28px;')
css = css.replace('.stat-label {\n  font-size: 13px;', '.stat-label {\n  font-size: 11px;')

# 5. Background Pattern
css = css.replace('background-size: 150px;', 'background-size: 60px;')

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
