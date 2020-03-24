'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from collector.utils import fics_references

class TourOfDutyRef(models.Model):
    class Meta:
        ordering = ['category','reference']
        verbose_name = "Tour of Duty Reference"
    reference = models.CharField(max_length=64,default='',blank=True)
    category = models.CharField(max_length=20,choices=fics_references.LIFEPATH_CATEGORY,default='Tour of Duty',blank=True)
    caste = models.CharField(max_length=20,choices=fics_references.LIFEPATH_CASTE,default='Other',blank=True)
    topic = models.CharField(max_length=64,default="",blank=True)
    source = models.CharField(max_length=32, default='FS2CRB', null=True, blank=True)
    is_custom = models.BooleanField(default=False)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
    PA_STR = models.IntegerField(default=0)
    PA_CON = models.IntegerField(default=0)
    PA_BOD = models.IntegerField(default=0)
    PA_MOV = models.IntegerField(default=0)
    PA_INT = models.IntegerField(default=0)
    PA_WIL = models.IntegerField(default=0)
    PA_TEM = models.IntegerField(default=0)
    PA_PRE = models.IntegerField(default=0)
    PA_REF = models.IntegerField(default=0)
    PA_TEC = models.IntegerField(default=0)
    PA_AGI = models.IntegerField(default=0)
    PA_AWA = models.IntegerField(default=0)
    OCC_LVL = models.IntegerField(default=0)
    OCC_DRK = models.IntegerField(default=0)
    WP = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    description = models.TextField(max_length=1024,default='',blank=True)

    def __str__(self):
        return '[%s] %s (%s)(%d)' % (fics_references.LIFEPATH_CATEGORY_SHORT[self.category], self.reference,fics_references.LIFEPATH_CASTE_SHORT[self.caste],self.value)

    def fix(self):
        self.WP = 0
        if self.is_custom:
            self.value = self.AP*3 + self.OP
        else:
            self.AP = self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + self.PA_REF + self.PA_TEC + self.PA_AGI + self.PA_AWA + self.OCC_LVL - self.OCC_DRK
            self.OP = 0
            texts = []
            if self.PA_STR != 0:
              texts.append("STR %+d"%(self.PA_STR))
            if self.PA_CON != 0:
              texts.append("CON %+d"%(self.PA_CON))
            if self.PA_BOD != 0:
              texts.append("BOD %+d"%(self.PA_BOD))
            if self.PA_MOV != 0:
              texts.append("MOV %+d"%(self.PA_MOV))
            if self.PA_INT != 0:
              texts.append("INT %+d"%(self.PA_INT))
            if self.PA_WIL != 0:
              texts.append("WIL %+d"%(self.PA_WIL))
            if self.PA_TEM != 0:
              texts.append("TEM %+d"%(self.PA_TEM))
            if self.PA_PRE != 0:
              texts.append("PRE %+d"%(self.PA_PRE))
            if self.PA_REF != 0:
              texts.append("REF %+d"%(self.PA_REF))
            if self.PA_TEC != 0:
              texts.append("TEC %+d"%(self.PA_TEC))
            if self.PA_AGI != 0:
              texts.append("AGI %+d"%(self.PA_AGI))
            if self.PA_AWA != 0:
              texts.append("AWA %+d"%(self.PA_AWA))
            if self.OCC_LVL != 0:
              texts.append("OCC %+d"%(self.OCC_LVL))
            if self.OCC_DRK != 0:
              texts.append("DRK %+d"%(self.OCC_DRK))
            for s in self.skillmodificator_set.all():
              texts.append("{%s %+d}"%(s.skill_ref.reference,s.value))
              if s.skill_ref.is_wildcard:
                  self.WP += s.value
              self.OP += s.value
            for bc in self.blessingcursemodificator_set.all():
              texts.append("(%s %+d)"%(bc.blessing_curse_ref.reference,bc.blessing_curse_ref.value))
              self.OP += bc.blessing_curse_ref.value
            for ba in self.beneficeafflictionmodificator_set.all():
              texts.append("(%s %+d)"%(ba.benefice_affliction_ref.reference,ba.benefice_affliction_ref.value))
              self.OP += ba.benefice_affliction_ref.value
            self.description = " ".join(texts)
            self.value = self.AP*3 + self.OP

@receiver(pre_save, sender=TourOfDutyRef, dispatch_uid='update_tour_of_duty_ref')
def update_tour_of_duty_ref(sender, instance, **kwargs):
    instance.fix()
