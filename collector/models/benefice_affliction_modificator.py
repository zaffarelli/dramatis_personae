'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.tourofduty_ref import TourOfDutyRef
from collector.models.benefice_affliction_ref import BeneficeAfflictionRef

class BeneficeAfflictionModificator(models.Model):
    class Meta: 
        ordering = ['benefice_affliction_ref']
    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    benefice_affliction_ref = models.ForeignKey(BeneficeAfflictionRef, on_delete=models.CASCADE)
    def __str__(self):
        return '%s=%s' % (self.tour_of_duty_ref.reference,self.benefice_affliction_ref.reference)


