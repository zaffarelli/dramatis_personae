import sys

# Run me through python manage.py shell, then:
# exec(open('scripts/dp_finder.py').read())
class DPToDCheck:
    def __init__(self):
        print("  This is dP tod check script. Here is a list of actions...")
        print("    1 - Check tours of duty")
        print("    0 - Quit")
        topic = ''
        while topic != '0':
            topic = input('  What do you want to do? [0] ')
            if topic == '1':
                self.perform()

    def bash_format(self,txt):
        new_txt = "\033[1;39m".join(txt.split('µ'))
        new_txt = "\033[0;m".join(new_txt.split('§'))
        return new_txt

    def perform(self):
        from collector.models.character import Character
        PA = ['PA_STR','PA_CON','PA_BOD','PA_MOV','PA_PRE','PA_WIL','PA_TEM','PA_INT','PA_REF','PA_AGI','PA_TEC','PA_AWA']
        all = Character.objects.all()
        for c in all:
            found = []

            for p in PA:
                x = getattr(c,p)
                if x>=10:
                    found.append(self.bash_format("   - has value µ%d§ for attribute µ%s§."%(x,p)))
            for s in c.skill_set.all():
                if s.value >= 10:
                    found.append(self.bash_format("   - has value µ%d§ for skill µ%s§."%(s.value,s.skill_ref.reference)))
            if len(found)>0:
                print(self.bash_format("µ%s§..."%(c.rid)))
                print("%s"%("\n".join(found)))


f = DPToDCheck()
