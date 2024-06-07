from PIL import Image

img = Image.open("watermarks/rotated_Copyright-35.png")
rgba = img.convert("RGBA")
img_data = rgba.getdata()

transparent_data = []
for item in img_data:
    if item[0] == 255 and item[1] == 255 and item[2] == 255:
        transparent_data.append((255, 255, 255, 0))
    else:
        transparent_data.append((item[0], item[1], item[2], 35))

rgba.putdata(transparent_data)
rgba.save("Copyright_watermark-35.png", "PNG")
#
# trp_img = Image.open("Copyright-35.png")
# rotated_trp_img = trp_img.rotate(20)
# rotated_trp_img.save("rotated_Copyright-35.png", "PNG")