from PIL import Image
import os
import glob

path = '../dp_media/images'
for filename in glob.glob(os.path.join(path, 'f_*.jpg')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        im = Image.open(filename)
        width, height = im.size
        print(filename, im.size)

# Setting the points for cropped image
# left = 4
# top = height / 5
# right = 154
# bottom = 3 * height / 5
#
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((left, top, right, bottom))
# newsize = (300, 300)
# im1 = im1.resize(newsize)
# # Shows the image in image viewer
# im1.show()

