import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix h1
html = html.replace('<h1>Enhance Your <br>Coffee Experience<br>With Us</h1>', '<h1>Enhance Your Coffee <br>Experience With Us</h1>')

# Fix nav container
if '<nav>' in html and '<div class=\"container\">' not in html.split('</nav>')[0]:
    html = html.replace('<nav>', '<nav>\n    <div class=\"container nav-container\">')
    html = html.replace('</nav>', '    </div>\n  </nav>')

# Fix arrow svg
old_arrow = '''<div class=\"hero-arrow\">
            <svg viewBox=\"0 0 100 100\" fill=\"none\" stroke=\"#1A1A1A\" stroke-width=\"12\" stroke-linecap=\"round\" stroke-linejoin=\"round\" style=\"transform: scaleX(-1) rotate(20deg);\">
              <path d=\"M 10 10 Q 50 80 90 90\" />
              <path d=\"M 70 80 L 90 90 L 85 70\" />
            </svg>
          </div>'''
new_arrow = '''<div class=\"hero-arrow\">
            <svg viewBox=\"0 0 200 100\" fill=\"none\" stroke=\"#1A1A1A\" stroke-width=\"8\" stroke-linecap=\"round\" stroke-linejoin=\"round\">
              <path d=\"M 10 20 Q 80 -30 180 80\" />
              <path d=\"M 150 70 L 180 80 L 160 50\" />
            </svg>
          </div>'''
html = html.replace(old_arrow, new_arrow)

# Fix curved text
old_svg_text = '''<svg viewBox=\"0 0 200 200\">
              <path id=\"curve\" d=\"M 20 100 A 80 80 0 0 1 180 100\" fill=\"transparent\" />
              <text>
                <textPath href=\"#curve\" startOffset=\"50%\" text-anchor=\"middle\">
                  Top selling coffee product
                </textPath>
              </text>
            </svg>'''
new_svg_text = '''<svg viewBox=\"0 0 300 300\">
              <path id=\"curve\" d=\"M 50 150 A 100 100 0 0 1 250 150\" fill=\"transparent\" />
              <text>
                <textPath href=\"#curve\" startOffset=\"50%\" text-anchor=\"middle\">
                  Top selling coffee product
                </textPath>
              </text>
            </svg>'''
html = html.replace(old_svg_text, new_svg_text)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
