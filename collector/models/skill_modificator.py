'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.skill_ref import SkillRef
from collector.models.tourofduty_ref import TourOfDutyRef
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

class SkillModificator(models.Model): 
  class Meta:
    ordering = ['skill_ref']
  tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
  skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
  value = models.IntegerField(default=0)
  def __str__(self):
    return '%s %s' % (self.tour_of_duty_ref.reference,self.skill_ref.reference)
  def fix(self):
    pass
@receiver(pre_save, sender=SkillModificator, dispatch_uid='update_skill_modificator')
def update_skill_modificator(sender, instance, **kwargs):
  instance.fix()
