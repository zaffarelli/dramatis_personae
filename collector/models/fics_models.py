from django.db import models
from collector.models.characters import Character
from django.contrib import admin

class Role(models.Model):
  class Meta:
    ordering = ['reference']
  reference = models.CharField(max_length=64,default='new_role',blank=True, unique=True)
  value = models.PositiveIntegerField(default=0)
  primaries = models.PositiveIntegerField(default=0)
  maxi = models.PositiveIntegerField(default=10)
  skills = models.PositiveIntegerField(default=0)
  talents = models.PositiveIntegerField(default=0)
  ba = models.PositiveIntegerField(default=0)
  bc = models.PositiveIntegerField(default=0)
  
  def __str__(self):
    return '%s (%s)' % (self.reference, self.value)

class Profile(models.Model):
  class Meta:
    ordering = ['reference']
  reference = models.CharField(max_length=64,default='new_role',blank=True, unique=True)
  weights = models.CharField(max_length=128, default = '[1,1,1,1,1,1,1,1,1,1,1,1]')
  groups = models.CharField(max_length=128, default = '[]')
  def __str__(self):
    return '%s (%s)' % (self.reference, self.value)
  def set_weights(self,data):
    self.weights = json.dumps(data)
  def get_weights(self):
    return json.loads(self.weights)
  def set_groups(self,data):
    self.groups = json.dumps(data)
  def get_groups(self):
    return json.loads(self.groups)
    
class RoleAdmin(admin.ModelAdmin):
  ordering = ('value',)

class ProfileAdmin(admin.ModelAdmin):
  ordering = ('reference',)


