'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character_custo import CharacterCusto
from collector.models.weapon import WeaponRef

class WeaponCusto(models.Model):
  class Meta:
    ordering = ['character_custo','weapon_ref']
  character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
  weapon_ref = models.ForeignKey(WeaponRef, on_delete=models.CASCADE)
