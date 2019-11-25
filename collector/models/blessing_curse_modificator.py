'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.tourofduty_ref import TourOfDutyRef
from collector.models.blessing_curse_ref import BlessingCurseRef

class BlessingCurseModificator(models.Model):
  class Meta:
    ordering = ['tour_of_duty_ref','blessing_curse_ref']
  tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
  blessing_curse_ref = models.ForeignKey(BlessingCurseRef, on_delete=models.CASCADE)
  def __str__(self):
    return '%s (%s)' % (self.tour_of_duty_ref.reference,self.blessing_curse_ref.reference)



