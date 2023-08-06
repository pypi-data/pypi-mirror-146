import PIL
from PIL import Image

def diff(img1, img2):
    r = 1
    im1 = img1.load()
    im2 = img2.load()
    out = Image.new('L', (img1.size[0], img1.size[1]), 0)
    for i in range(0, img1.size[0]):
        for j in range(0, img1.size[1]):
            if(im1[i,j] != im2[i,j]):
                r = out.putpixel((i,j), 100)
    return out