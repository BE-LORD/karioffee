import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Discover image
old_discover = '''<div class="discover-image-container">
            <div class="discover-circle"></div>
            <img src="assets/images/discover-coffee-bag.png" alt="Premium Coffee Bag" class="discover-main-img">
          </div>'''
new_discover = '''<div class="discover-image-container">
            <div class="discover-circle"></div>
            <div class="discover-cups">
              <img src="assets/images/italian-coffee.png" class="discover-cup discover-cup-1" alt="Cup">
              <img src="assets/images/viennese-coffee.png" class="discover-cup discover-cup-2" alt="Cup">
              <img src="assets/images/new-orleans-coffee.png" class="discover-cup discover-cup-3" alt="Cup">
            </div>
          </div>'''
html = html.replace(old_discover, new_discover)

# Replace Hero right image
old_hero = '''<img src="assets/images/coffee-cups-stack.png" alt="Coffee Cups Stack" class="hero-main-cups">'''
new_hero = '''<div class="hero-stacked-cups">
              <img src="assets/images/italian-coffee.png" class="hero-stack hero-stack-1" alt="Cup">
              <img src="assets/images/viennese-coffee.png" class="hero-stack hero-stack-2" alt="Cup">
              <img src="assets/images/new-orleans-coffee.png" class="hero-stack hero-stack-3" alt="Cup">
            </div>'''
html = html.replace(old_hero, new_hero)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# CSS for Discover cups
discover_css = '''
.discover-image-container {
  position: relative;
  width: 100%;
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.discover-circle {
  position: absolute;
  width: 400px;
  height: 400px;
  background: var(--bg-sage);
  border-radius: 50%;
  z-index: 1;
}
.discover-cups {
  position: relative;
  z-index: 2;
  width: 300px;
  height: 400px;
}
.discover-cup {
  position: absolute;
  width: 200px;
  filter: drop-shadow(0 20px 30px rgba(0,0,0,0.15));
}
.discover-cup-1 {
  bottom: 0;
  left: 0;
  transform: rotate(-15deg);
  z-index: 3;
}
.discover-cup-2 {
  bottom: 80px;
  left: 50px;
  transform: rotate(5deg);
  z-index: 2;
}
.discover-cup-3 {
  bottom: 160px;
  left: 100px;
  transform: rotate(20deg);
  z-index: 1;
}
'''
css += discover_css

# CSS for Hero stacked cups
hero_stack_css = '''
.hero-stacked-cups {
  position: relative;
  width: 100%;
  height: 500px;
  z-index: 2;
}
.hero-stack {
  position: absolute;
  width: 180px;
  filter: drop-shadow(0 15px 25px rgba(0,0,0,0.12));
}
.hero-stack-1 {
  bottom: 20px;
  left: 20px;
  transform: rotate(-10deg);
  z-index: 3;
}
.hero-stack-2 {
  bottom: 100px;
  left: 60px;
  transform: rotate(10deg);
  z-index: 2;
}
.hero-stack-3 {
  bottom: 180px;
  left: 100px;
  transform: rotate(25deg);
  z-index: 1;
}
'''
css += hero_stack_css

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
