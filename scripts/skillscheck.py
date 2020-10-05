from collector.models.characters import Character
from collector.utils.fs_fics7 import skills_randomizer
x = Character.objects.get(pk=77)
x.on_save_re_roll_skills=True
skills_randomizer(x)
x.save()
