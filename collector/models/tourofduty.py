'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from collector.models.tourofduty_ref import TourOfDutyRef

class TourOfDuty(models.Model):
  class Meta:
    ordering = ['character','tour_of_duty_ref']
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.tour_of_duty_ref.reference)

  def push(self,ch):
    tod = self.tour_of_duty_ref
    ch.PA_STR += tod.PA_STR
    ch.PA_CON += tod.PA_CON
    ch.PA_BOD += tod.PA_BOD
    ch.PA_MOV += tod.PA_MOV
    ch.PA_INT += tod.PA_INT
    ch.PA_WIL += tod.PA_WIL
    ch.PA_TEM += tod.PA_TEM
    ch.PA_PRE += tod.PA_PRE
    ch.PA_REF += tod.PA_REF
    ch.PA_TEC += tod.PA_TEC
    ch.PA_AGI += tod.PA_AGI
    ch.PA_AWA += tod.PA_AWA
    for sm in tod.skillmodificator_set.all():
      ch.add_or_update_skill(sm.skill_ref,sm.value,True)
    for bc in tod.blessingcursemodificator_set.all():
      ch.add_bc(bc.blessing_curse_ref)
    for ba in tod.beneficeafflictionmodificator_set.all():
      ch.add_ba(ba.benefice_affliction_ref)

  def pull(self,ch):
    tod = self.update_tour_of_duty_ref
    ch.PA_STR -= tod.PA_STR
    ch.PA_CON -= tod.PA_CON
    ch.PA_BOD -= tod.PA_BOD
    ch.PA_MOV -= tod.PA_MOV
    ch.PA_INT -= tod.PA_INT
    ch.PA_WIL -= tod.PA_WIL
    ch.PA_TEM -= tod.PA_TEM
    ch.PA_PRE -= tod.PA_PRE
    ch.PA_REF -= tod.PA_REF
    ch.PA_TEC -= tod.PA_TEC
    ch.PA_AGI -= tod.PA_AGI
    ch.PA_AWA -= tod.PA_AWA
    for sm in tod.skillmodificator_set.all():
      ch.remove_update_skill(sm.skill_ref,sm.value,True)
    for bc in tod.blessingcursemodificator_set.all():
      ch.remove_bc(bc.blessing_curse_ref)
    for ba in tod.beneficeafflictionmodificator_set.all():
      ch.remove_ba(ba.benefice_affliction_ref)
