'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character
from collector.models.benefice_affliction_ref import BeneficeAfflictionRef

class BeneficeAffliction(models.Model):
    class Meta:
        ordering = ['benefice_affliction_ref']
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    benefice_affliction_ref = models.ForeignKey(BeneficeAfflictionRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    description = models.TextField(max_length=256, default='', null=True, blank=True)
    def __str__(self):
        return '%s=%s' % (self.character.full_name,self.benefice_affliction_ref.reference)



