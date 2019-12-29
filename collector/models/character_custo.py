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
    summary = models.TextField(default="", blank=True, null=True)
    occult_level = models.PositiveIntegerField(default=0)
    occult_darkside = models.PositiveIntegerField(default=0)
    comment = models.TextField(default="", blank=True, null=True)

    def recalculate(self):
        self.AP = 0
        self.OP = 0
        self.AP += (self.PA_STR + self.PA_CON + self.PA_BOD+ self.PA_MOV
                      + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE
                      + self.PA_REF + self.PA_TEC + self.PA_AGI + self.PA_AWA)
        self.AP += (self.occult_level - self.occult_darkside)
        for s in self.skillcusto_set.all():
            if s.value == 0:
                s.delete()
        for s in self.skillcusto_set.all():
            if s.skill_ref.is_root == False:
                self.OP += s.value
        for bc in self.blessingcursecusto_set.all():
            self.OP += bc.blessing_curse_ref.value
        for ba in self.beneficeafflictioncusto_set.all():
            self.OP += ba.benefice_affliction_ref.value
        self.value = self.AP*3 + self.OP
        #print("RECALCULATE!")
        self.rebuild_summary()

    def rebuild_summary(self):
        self.summary = ""
        self.summary += "Attributes"
        self.summary += "<ul>"
        if self.PA_STR!=0:
            self.summary += "<li>STR %d</li>"%(self.PA_STR)
        if self.PA_CON!=0:
            self.summary += "<li>CON %d</li>"%(self.PA_CON)
        if self.PA_BOD!=0:
            self.summary += "<li>BOD %d</li>"%(self.PA_BOD)
        if self.PA_MOV!=0:
            self.summary += "<li>MOV %d</li>"%(self.PA_MOV)
        if self.PA_INT!=0:
            self.summary += "<li>INT %d</li>"%(self.PA_INT)
        if self.PA_WIL!=0:
            self.summary += "<li>WIL %d</li>"%(self.PA_WIL)
        if self.PA_TEM!=0:
            self.summary += "<li>TEM %d</li>"%(self.PA_TEM)
        if self.PA_PRE!=0:
            self.summary += "<li>PRE %d</li>"%(self.PA_PRE)
        if self.PA_REF!=0:
            self.summary += "<li>REF %d</li>"%(self.PA_REF)
        if self.PA_TEC!=0:
            self.summary += "<li>TEC %d</li>"%(self.PA_TEC)
        if self.PA_AGI!=0:
            self.summary += "<li>AGI %d</li>"%(self.PA_AGI)
        if self.PA_AWA!=0:
            self.summary += "<li>AWA %d</li>"%(self.PA_AWA)
        self.summary += "</ul>"
        self.summary += "Occult"
        self.summary += "<ul>"
        if self.occult_level!=0:
            self.summary += "<li>Lightside %d</li>"%(self.occult_level)
        if self.occult_darkside!=0:
            self.summary += "<li>Darkside  %d</li>"%(self.occult_darkside)
        self.summary += "</ul>"
        self.summary += "Skills"
        self.summary += "<ul>"
        for s in self.skillcusto_set.all():
            if s.skill_ref.is_root == False:
                self.summary += "<li>%s +%d</li>"%(s.skill_ref.reference,s.value)
        self.summary += "</ul>"
        self.summary += "Blessings/Curses"
        self.summary += "<ul>"
        for bc in self.blessingcursecusto_set.all():
            self.summary += "<li>%s +%d</li>"%(bc.blessing_curse_ref.reference,bc.blessing_curse_ref.value)
        self.summary += "</ul>"
        self.summary += "Benefices/Afflictions"
        self.summary += "<ul>"
        for ba in self.beneficeafflictioncusto_set.all():
            self.summary += "<li>%s +%d</li>"%(ba.benefice_affliction_ref.reference,ba.benefice_affliction_ref.value)
        self.summary += "</ul>"

    def push(self,ch):
        ch.PA_STR += self.PA_STR
        ch.PA_CON += self.PA_CON
        ch.PA_BOD += self.PA_BOD
        ch.PA_MOV += self.PA_MOV
        ch.PA_INT += self.PA_INT
        ch.PA_WIL += self.PA_WIL
        ch.PA_TEM += self.PA_TEM
        ch.PA_PRE += self.PA_PRE
        ch.PA_REF += self.PA_REF
        ch.PA_TEC += self.PA_TEC
        ch.PA_AGI += self.PA_AGI
        ch.PA_AWA += self.PA_AWA
        for sm in self.skillcusto_set.all():
            ch.add_or_update_skill(sm.skill_ref,sm.value,True)
        for bc in self.blessingcursecusto_set.all():
            ch.add_bc(bc.blessing_curse_ref)
        for ba in self.beneficeafflictioncusto_set.all():
            ch.add_ba(ba.benefice_affliction_ref)

    def add_or_update_skill(self,skill_ref_id,value):
        ''' Updating customization and avatar '''
        from collector.models.skill_custo import SkillCusto
        from collector.models.skill_ref import SkillRef
        found_in_custo = False
        found_cu = None
        for found_cu in self.skillcusto_set.all():
            if found_cu.skill_ref.id == skill_ref_id:
                found_in_custo = True
                break
        if found_in_custo:
            #if found_cu.value+int(value)>0:
            found_cu.value += int(value)
            found_cu.save()
        else:
            skill_custo = SkillCusto()
            skill_custo.skill_ref = SkillRef.objects.get(pk=skill_ref_id)
            if (int(value)>0):
                skill_custo.value = int(value)
                skill_custo.character_custo = self
                skill_custo.save()

@receiver(pre_save, sender=CharacterCusto, dispatch_uid='update_character_custo')
def update_character_custo(sender, instance, conf=None, **kwargs):
    instance.recalculate()


class CharacterCustoAdmin(admin.ModelAdmin):
    from collector.models.skill_custo_inline import SkillCustoInline
    from collector.models.blessing_curse_custo_inline import BlessingCurseCustoInline
    from collector.models.benefice_affliction_custo_inline import BeneficeAfflictionCustoInline
    list_display = ('character','value','AP','OP',)
    exclude = ('value','AP','OP')
    inlines = [
        SkillCustoInline,
        BlessingCurseCustoInline,
        BeneficeAfflictionCustoInline,
    ]
