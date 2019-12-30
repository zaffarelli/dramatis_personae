'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character_custo import CharacterCusto
from collector.models.shield import ShieldRef

class ShieldCusto(models.Model):
  class Meta:
    ordering = ['character_custo','shield_ref']
  character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
  shield_ref = models.ForeignKey(ShieldRef, on_delete=models.CASCADE)
