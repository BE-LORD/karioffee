from PIL import Image
def make_bg_transparent(image_path):
    img = Image.open(image_path)
    img = img.convert('RGBA')
    datas = img.getdata()
    newData = []
    for item in datas:
        # aggressive white/light removal
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(image_path, 'PNG')

make_bg_transparent('assets/images/coffee-cups-stack.png')
