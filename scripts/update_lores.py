from collector.models.skill import SkillRef
from cartograph.models.system import System

all = System.objects.all()

lore_link = SkillRef.objects.get(reference='Lore')

for system in all:
    relevant_lore = f'Lore ({system.name} System)'
    found_lores = SkillRef.objects.filter(reference=relevant_lore)
    if len(found_lores)>0:
        for lore in found_lores:
            print(f'{system.name} --> Found match {lore.reference} ')
    else:
        print(f'Error ->Nothing matching to {relevant_lore}')
        s = SkillRef()
        s.reference = relevant_lore
        s.is_root = False
        s.is_speciality = True
        s.is_common = (system.sector == 'Empire')
        s.is_wildcard = False
        s.linked_to = lore_link
        s.grouping = 'System'
        s.group = 'EDU'
        s.save()
        print(f'{system.name} --> Created {s} ')