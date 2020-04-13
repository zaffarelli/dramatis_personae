import sys

# Run me through python manage.py shell, then:
# exec(open('scripts/dp_finder.py').read())
class DPFinder:
    def __init__(self):
        print("  This is dP finder script. Here is a list of actions...")
        print("    1 - Search for a skill among the avatars")
        print("    2 - Search for a benefice/affliction among the avatars")
        print("    3 - Search for a blessing/curse among the avatars")
        print("    0 - Quit")
        topic = ''
        while topic != '0':
            topic = input('  What do you want to do? [0] ')
            if topic == '1':
                self.skill_search()
            elif topic == '2':
                self.ba_search()
            elif topic == '3':
                self.bc_search()

    def bash_format(self,txt):
        new_txt = "\033[1;39m".join(txt.split('µ'))
        new_txt = "\033[0;m".join(new_txt.split('§'))
        return new_txt

    def skill_search(self):
        from collector.models.character import Character
        from collector.models.skill_ref import SkillRef
        skill_name = input('  Type the skill you want to search: ')
        x = SkillRef.objects.filter(reference=skill_name).first()
        if x:
            found = []
            all = Character.objects.all()
            for c in all:
                for s in c.skill_set.all():
                    if s.skill_ref == x:
                        found.append(self.bash_format("µ%s§ (%+d)"%(c.rid,s.value)))
            print(self.bash_format("The µ%s§ skill was found amongst µ%d§ of the %d avatars in dP. Here are the details:"%(skill_name,len(found),len(all))))
            print("%s"%(", ".join(found)))

    def ba_search(self):
        pass

    def bc_search(self):
        pass

f = DPFinder()
