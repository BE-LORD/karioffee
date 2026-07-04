"""Optimize all site images: resize to display size x2 (retina) and recompress.
Originals are backed up to assets/images/_originals/ the first time."""
import os
import shutil
from PIL import Image

IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'images')
BACKUP = os.path.join(IMG_DIR, '_originals')
os.makedirs(BACKUP, exist_ok=True)

# max width each image actually needs (2x its largest rendered size)
TARGETS = {
    'avatar-1.png': 96, 'avatar-2.png': 96, 'avatar-3.png': 96, 'avatar-4.png': 96,
    'avatar-a.png': 96, 'avatar-b.png': 96, 'avatar-c.png': 96, 'avatar-d.png': 96,
    'avatar-testimonial.png': 160,
    'hero-coffee-cup.png': 1100,
    'coffee-cups-stack.png': 1000,
    'coffee-easy-cup.png': 900,
    'discover-coffee-bag.png': 500,
    'newsletter-latte.png': 500,
    'italian-coffee.png': 640,
    'moroccan-coffee.png': 640,
    'new-orleans-coffee.png': 640,
    'viennese-coffee.png': 640,
    'hero-pattern.png': 800,
}

total_before = total_after = 0
for name, max_w in TARGETS.items():
    path = os.path.join(IMG_DIR, name)
    if not os.path.exists(path):
        print(f'SKIP (missing): {name}')
        continue
    before = os.path.getsize(path)
    total_before += before

    bak = os.path.join(BACKUP, name)
    if not os.path.exists(bak):
        shutil.copy2(path, bak)

    img = Image.open(path)
    if img.width > max_w:
        h = round(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)
    # quantize with alpha preserved for big savings, keep quality high
    if img.mode == 'RGBA':
        img = img.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG).convert('RGBA')
    img.save(path, optimize=True)
    after = os.path.getsize(path)
    total_after += after
    print(f'{name}: {before/1024:.0f}KB -> {after/1024:.0f}KB')

print(f'\nTOTAL: {total_before/1024/1024:.1f}MB -> {total_after/1024/1024:.1f}MB')
