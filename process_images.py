from PIL import Image
import colorsys

def make_white_transparent(image_path):
    img = Image.open(image_path)
    img = img.convert('RGBA')
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] > 245 and item[1] > 245 and item[2] > 245:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(image_path, 'PNG')

def create_avatars(base_path):
    img = Image.open(base_path).convert('RGBA')
    for i, hue_offset in enumerate([0, 0.3, 0.6, 0.8]):
        out = []
        for r, g, b, a in img.getdata():
            h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
            r_n, g_n, b_n = colorsys.hsv_to_rgb((h + hue_offset)%1.0, s, v)
            out.append((int(r_n*255), int(g_n*255), int(b_n*255), a))
        new_img = Image.new('RGBA', img.size)
        new_img.putdata(out)
        new_img.save(f'assets/images/avatar-{i+1}.png', 'PNG')

make_white_transparent('assets/images/hero-coffee-cup.png')
make_white_transparent('assets/images/coffee-cups-stack.png')
create_avatars('assets/images/avatar-testimonial.png')
