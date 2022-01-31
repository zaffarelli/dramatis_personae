from PIL import Image
import os
import glob

path = '../dp_media/images'
for filename in glob.glob(os.path.join(path, 'f_*.jpg')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        im = Image.open(filename)
        width, height = im.size
        new_size = (300, 400)
        if width > new_size[0]:
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)
            print(f'Updated: {filename}')

