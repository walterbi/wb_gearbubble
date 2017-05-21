from PIL import Image

image = Image.open("/Users/pwnux90/MEGA/workplace/jokerface/gearbubble/img/Happy Pill Pugs dog mom dad gift mug.png")

imageSize = image.size
print imageSize
imageBox = image.getbbox()

imageComponents = image.split()

rgbImage = Image.new("RGB", imageSize, (0,0,0))
rgbImage.paste(image, mask=imageComponents[3])
croppedBox = rgbImage.getbbox()

if imageBox != croppedBox:
    cropped=image.crop(croppedBox)
    cropped.show()