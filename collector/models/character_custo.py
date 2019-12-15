'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models


class CharacterCusto(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    PA_STR = models.PositiveIntegerField(default=0)
    PA_CON = models.PositiveIntegerField(default=0)
    PA_BOD = models.PositiveIntegerField(default=0)
    PA_MOV = models.PositiveIntegerField(default=0)
    PA_INT = models.PositiveIntegerField(default=0)
    PA_WIL = models.PositiveIntegerField(default=0)
    PA_TEM = models.PositiveIntegerField(default=0)
    PA_PRE = models.PositiveIntegerField(default=0)
    PA_REF = models.PositiveIntegerField(default=0)
    PA_TEC = models.PositiveIntegerField(default=0)
    PA_AGI = models.PositiveIntegerField(default=0)
    PA_AWA = models.PositiveIntegerField(default=0)
    occult_level = models.PositiveIntegerField(default=0)
    occult_darkside = models.PositiveIntegerField(default=0)

    def add_or_update_skill(self,skill_ref_id,value):
        ''' Updating customization and avatar '''
        from collector.models.skill_custo import SkillCusto
        from collector.models.skill_ref import SkillRef
        found_in_character = False
        found_in_custo = False
        found_ch = None
        found_cu = None
        for found_ch in self.character.skills_set.all():
            if found_ch.skill_ref == skill_ref.id:
                found_in_character = True
                for found_cu in self.skillcusto_set.all():
                    if found_cu.skill_ref.id == skill_ref.id:
                        found_in_custo = True
                        break
                break
        if found_ch:
            found_ch.value += value
            found_ch.save()
        else:
            skill = Skill()
            skill.character = self.character
            skill.skill_ref = SkillRef.objects.get(pk=skill_ref.id)
            skill.value = value
            skill.save()
        if found_in_custo:
            found_cu.value += value
            found_cu.save()
        else:
            skill_custo = SkillCusto()
            skill_custo.skill_ref = SkillRef.objects.get(pk=skill_ref.id)
            skill_custo.value = value
            skill_custo.character = self.character
            skill_custo.save()
