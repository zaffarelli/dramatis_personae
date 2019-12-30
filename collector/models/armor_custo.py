'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character_custo import CharacterCusto
from collector.models.armor_ref import ArmorRef

class ArmorCusto(models.Model):
  class Meta:
    ordering = ['character_custo','armor_ref']
  character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
  armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)
