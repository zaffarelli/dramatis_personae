'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character
from django.db.models.signals import pre_save
from django.dispatch import receiver

class CharacterCusto(models.Model):
    character = models.OneToOneField(Character,on_delete=models.CASCADE,primary_key=True)
    value = models.IntegerField(default=0)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
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
    comment = models.TextField(default="", blank=True, null=True)

    def recalculate(self):
        self.AP = (self.PA_STR + self.PA_CON + self.PA_BOD+ self.PA_MOV
                      + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE
                      + self.PA_REF + self.PA_TEC + self.PA_AGI + self.PA_AWA)
        for s in self.skillcusto_set.all():
            self.OP += s.value
        self.value = self.AP*3 + self.OP

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

@receiver(pre_save, sender=CharacterCusto, dispatch_uid='update_character_custo')
def update_character_custo(sender, instance, conf=None, **kwargs):
    instance.recalculate()


class CharacterCustoAdmin(admin.ModelAdmin):
    from collector.models.skill_custo_inline import SkillCustoInline
    list_display = ('character','value','AP','OP',)
    exclude = ('value','AP','OP')
    inlines = [
        SkillCustoInline,
    ]
