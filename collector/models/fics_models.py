'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
import json
#
# class Role(models.Model):
#   class Meta:
#     ordering = ['value','reference']
#   reference = models.CharField(max_length=64,default=1,blank=True, unique=True)
#   value = models.PositiveIntegerField(default=0)
#   primaries = models.PositiveIntegerField(default=0)
#   maxi = models.PositiveIntegerField(default=10)
#   mini = models.PositiveIntegerField(default=1)
#   skills = models.PositiveIntegerField(default=0)
#   skill_roots = models.PositiveIntegerField(default=2)
#   talents = models.PositiveIntegerField(default=0)
#   ba = models.PositiveIntegerField(default=0)
#   bc = models.PositiveIntegerField(default=0)
#
#   def __str__(self):
#     return '%s (%s)' % (self.reference, self.value)
#
# class Profile(models.Model):
#   class Meta:
#     ordering = ['reference']
#   reference = models.CharField(max_length=64,default=1,blank=True, unique=True)
#   weights = models.CharField(max_length=128, default = '[1,1,1,1,1,1,1,1,1,1,1,1]')
#   groups = models.CharField(max_length=128, default = '[]')
#   favorites = models.CharField(max_length=640, default = '[]')
#   def __str__(self):
#     return '%s' % (self.reference)
#   def set_weights(self,data):
#     self.weights = json.dumps(data)
#   def get_weights(self):
#     return json.loads(self.weights)
#   def set_groups(self,data):
#     self.groups = json.dumps(data)
#   def get_groups(self):
#     #print(self.groups)
#     return json.loads(self.groups)
#   def set_favorites(self,data):
#     self.favorites = json.dumps(data)
#   def get_favorites(self):
#     return json.loads(self.favorites)

class Specie(models.Model):
  class Meta:
    ordering = ['species','race']
    unique_together = (('species', 'race'),)
  species = models.CharField(max_length=64,default=1,blank=True)
  race = models.CharField(max_length=64,default='',blank=True)
  racial_attr_mod = models.CharField(max_length=128, default = '{}')
  racial_skills = models.CharField(max_length=512, default = '{}')
  racial_occult = models.CharField(max_length=128, default = '{}')
  attr_mod_balance = models.IntegerField(default=0)
  skill_balance = models.IntegerField(default=0)
  description = models.TextField(max_length=512, default='',blank=True)
  def __str__(self):
    return '%s %s'%(self.species,self.race)
  def set_racial_skills(self,data):
    self.racial_skills = json.dumps(data)
  def get_racial_skills(self):
    return json.loads(self.racial_skills)
  def set_racial_attr_mod(self,data):
    self.racial_attr_mod = json.dumps(data)
  def get_racial_attr_mod(self):
    return json.loads(self.racial_attr_mod)
  def update_balance(self):
    attr_mods = self.get_racial_attr_mod()
    b = 0
    for am in attr_mods:
      b += attr_mods[am]
    self.attr_mod_balance = b
    #print('PA --> %s:%d'%(self,b))
    skills_mods = self.get_racial_skills()
    b = 0
    for sm in skills_mods:
      b += skills_mods[sm]
    self.skill_balance = b
    #print('Skill --> %s:%d'%(self,b))
    self.save()

class SpecieAdmin(admin.ModelAdmin):
  ordering = ('species','race')
  list_display = ('species','race','racial_attr_mod','attr_mod_balance','racial_skills','skill_balance','description','racial_occult')


class RoleAdmin(admin.ModelAdmin):
  ordering = ('-value',)
  list_display = ('reference','value','primaries','maxi','mini','skill_roots','skills','talents','ba','bc')

class ProfileAdmin(admin.ModelAdmin):
  ordering = ('reference',)
  list_display = ('reference','weights','groups','favorites')
