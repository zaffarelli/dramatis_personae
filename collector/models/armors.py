'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.characters import Character
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

class Armor(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.armor_ref.reference)

class ArmorRefAdmin(admin.ModelAdmin):
  ordering = ('category','-stopping_power','reference')  

class ArmorAdmin(admin.ModelAdmin):
  ordering = ('character','armor_ref',)



