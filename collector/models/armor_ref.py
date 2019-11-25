'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from django.contrib import admin

class ArmorRef(models.Model):
  class Meta:
    ordering = ['reference']
  reference = models.CharField(max_length=64,default='',blank=True, unique=True)
  category = models.CharField(max_length=6,choices=(('Soft',"Soft Armor"),('Medium',"Medium Armor"),('Hard',"Hard Armor")),default='Soft',blank=True)
  head = models.BooleanField(default=False)
  torso = models.BooleanField(default=True)
  left_arm = models.BooleanField(default=True)
  right_arm = models.BooleanField(default=True)
  left_leg = models.BooleanField(default=False)
  right_leg = models.BooleanField(default=False)
  stopping_power = models.PositiveIntegerField(default=2, blank=True)
  cost = models.PositiveIntegerField(default=2, blank=True)
  encumbrance = models.PositiveIntegerField(default=0, blank=True)
  description = models.TextField(max_length=128,default='', blank=True)
  def __str__(self):
    return '%s (%s, SP:%s)' % (self.reference, self.category, self.stopping_power)
