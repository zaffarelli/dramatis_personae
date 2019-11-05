from collector.models.characters import Character
from collector.utils.fs_fics7 import skills_randomizer
x = Character.objects.get(pk=77)
x.onsave_reroll_skills=True
skills_randomizer(x)
x.save()
