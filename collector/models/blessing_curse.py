'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from collector.models.blessing_curse_ref import BlessingCurseRef

class BlessingCurse(models.Model):
  class Meta:
    ordering = ['character','blessing_curse_ref']
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  blessing_curse_ref = models.ForeignKey(BlessingCurseRef, on_delete=models.CASCADE)
  def __str__(self):
    return '%s (%s)' % (self.character.full_name,self.blessing_curse_ref.reference)



