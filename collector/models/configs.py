from django.db import models
from django.contrib import admin


class Config(models.Model):
  class Meta:
    ordering = ['title', 'epic']  
  from collector.models.epics import Epic
  from collector.models.dramas import Drama
  from collector.models.acts import Act
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
  drama = models.ForeignKey(Drama, null=True, blank=True, on_delete=models.SET_NULL)
  act = models.ForeignKey(Act, null=True, blank=True, on_delete=models.SET_NULL)
  description = models.TextField(max_length=128,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_active = models.BooleanField(default=False)
  def __str__(self):
    return '%s (%s / %s)' % (self.title, self.epic, self.gamemaster)

class ConfigAdmin(admin.ModelAdmin):
  ordering = ('title','epic')


