import sys

# Run me through python manage.py shell, then:
# exec(open('scripts/dp_skillslist.py').read())
class DPSkillsList:
    def __init__(self):
        print("  This is dP skill lister:")
        print("    1 - List of the skills for the characters sheet")
        print("    0 - Quit")
        topic = ''
        while topic != '0':
            topic = input('  What do you want to do? [0] ')
            if topic == '1':
                self.all_skills_list()

    def bash_format(self,txt):
        new_txt = "\033[1;39m".join(txt.split('µ'))
        new_txt = "\033[0;m".join(new_txt.split('§'))
        return new_txt

    def all_skills_list(self):
        from collector.models.skill import SkillRef
        all = SkillRef.objects.filter(is_speciality=False).order_by('reference')
        found = []
        for s in all:
            found.append(self.bash_format("µ%s§ %s"%(s.reference,"(R)" if s.is_root else " ")))
        print("%s"%("\n".join(found)))
        print(str(len(found))+" entries")

f = DPSkillsList()
