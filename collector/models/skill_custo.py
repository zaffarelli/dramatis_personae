'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.skill_ref import SkillRef
from collector.models.character_custo import CharacterCusto

class SkillCusto(models.Model):
  class Meta:
    ordering = ['character_custo','skill_ref']
  character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
  skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
  value = models.IntegerField(default=0)
