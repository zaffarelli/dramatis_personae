'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from django.contrib import admin

class ShieldRef(models.Model):
  class Meta:
    ordering = ['cost','reference']  
  reference = models.CharField(max_length=16,default='',blank=True, unique=True)
  protection_min = models.PositiveIntegerField(default=10,blank=True)
  protection_max = models.PositiveIntegerField(default=20,blank=True)
  hits = models.PositiveIntegerField(default=10,blank=True)
  cost = models.PositiveIntegerField(default=500,blank=True)
  is_compatible_with_medium_armor = models.BooleanField(default=False)
  is_compatible_with_hard_armor = models.BooleanField(default=False)
  description = models.TextField(max_length=128,default='', blank=True)
  def __str__(self):
    return '%s' % (self.reference)

class Shield(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  shield_ref = models.ForeignKey(ShieldRef, on_delete=models.CASCADE)
  charges = models.PositiveIntegerField(default=10, blank=True)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.shield_ref.reference)

class ShieldRefAdmin(admin.ModelAdmin):
  ordering = ('reference',)  







