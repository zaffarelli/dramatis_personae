import sys

# Run me through python manage.py shell, then:
# exec(open('scripts/dp_showepics.py').read())
from scenarist.models.epics import Epic
from scenarist.models.dramas import Drama
from scenarist.models.events import Event
from scenarist.models.acts import Act

class DPShowEpics:
    def __init__(self):
        print("  This is dP skill lister:")
        print("    1 - Make all stories visible")
        print("    2 - Make all stories exportable to PDF")
        print("    0 - Quit")
        topic = ''
        while topic != '0':
            topic = input('  What do you want to do? [0] ')
            if topic == '1':
                self.all_visible()
            if topic == '2':
                self.all_pdf()

    def bash_format(self, txt):
        new_txt = "\033[1;39m".join(txt.split('µ'))
        new_txt = "\033[0;m".join(new_txt.split('§'))
        return new_txt

    def do_show(self,all):
        for item in all:
            item.visible = True
            item.save()

    def do_pdf(self,all):
        for item in all:
            item.to_pdf = True
            item.save()

    def all_visible(self):
        self.do_show(Epic.objects.all())
        self.do_show(Drama.objects.all())
        self.do_show(Act.objects.all())
        self.do_show(Event.objects.all())
        print(self.bash_format("µDone all_visible !§"))


    def all_pdf(self):
        self.do_pdf(Epic.objects.all())
        self.do_pdf(Drama.objects.all())
        self.do_pdf(Act.objects.all())
        self.do_pdf(Event.objects.all())
        print(self.bash_format("µDone all pdf!§"))


f = DPShowEpics()
