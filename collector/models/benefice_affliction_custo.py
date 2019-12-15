'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character_custo import CharacterCusto
from collector.models.benefice_affliction_ref import BeneficeAfflictionRef

class BeneficeAfflictionCusto(models.Model):
    class Meta:
        ordering = ['character_custo','benefice_affliction_ref']
    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    benefice_affliction_ref = models.ForeignKey(BeneficeAfflictionRef, on_delete=models.CASCADE)
