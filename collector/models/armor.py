'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from collector.models.armor_ref import ArmorRef
from django.contrib import admin

class Armor(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.armor_ref.reference)





