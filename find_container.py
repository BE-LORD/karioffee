import re
with open('css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if '.container' in line:
        print(f'{i+1}: {line.strip()}')
