'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character_custo import CharacterCusto
from collector.models.blessing_curse_ref import BlessingCurseRef

class BlessingCurseCusto(models.Model):
  class Meta:
    ordering = ['character_custo','blessing_curse_ref']
  character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
  blessing_curse_ref = models.ForeignKey(BlessingCurseRef, on_delete=models.CASCADE)
