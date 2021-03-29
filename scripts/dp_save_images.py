import sys
import shutil
import os
'''
 Run me through python manage.py shell, then:
 python.manage.py shell < ./scripts/dp_save_images.py
 exec(open('scripts/dp_save_images.py').read())
'''

class DPGetImages:
    def __init__(self):
        print("  This is dP image saver.")
        print("    1 - Get all characters images.")
        print("    0 - Quit")
        topic = ''
        while topic != '0':
            topic = input('  What do you want to do? [0] ')
            if topic == '1':
                self.get_images()
            else:
                exit()

    def bash_format(self,txt):
        new_txt = "\033[1;39m".join(txt.split('µ'))
        new_txt = "\033[0;m".join(new_txt.split('§'))
        return new_txt

    def get_images(self):
        from collector.models.character import Character
        all = Character.objects.all()
        found = []
        for c in all:
            image_file_name = f'f_{c.rid}.jpg'
            src = "./dp_media/images/"+image_file_name
            dst = "./backup/images/" + image_file_name
            try:
                f = open(src)
            except:
                f = None
            if f:
                print(self.bash_format("OK: µ%s§ for %s."%(image_file_name,c.full_name)))
                found.append(image_file_name)
                shutil.copyfile(src, dst)
            else:
                print(self.bash_format("        Error: µ%s§ was not found." % (image_file_name)))
        print(str(len(found))+" entries")

f = DPGetImages()
