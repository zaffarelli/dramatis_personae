'''
╔╦╗╔═╗  ╔═╗┌─┐┌─┐┌┐┌┌─┐┬─┐┬┌─┐┌┬┐
 ║║╠═╝  ╚═╗│  ├┤ │││├─┤├┬┘│└─┐ │ 
═╩╝╩    ╚═╝└─┘└─┘┘└┘┴ ┴┴└─┴└─┘ ┴ 
'''
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel
import json

class Epic(StoryModel):
  class Meta:
    ordering = ['era','title']
    
  era = models.IntegerField(default=5017, blank=True)
  shortcut = models.CharField(default='xx', max_length=32, blank=True)
  population_count = models.IntegerField(default=0, blank=True)

  def get_absolute_url(self):
    return reverse('epic-detail', kwargs={'pk': self.pk})   

  def __str__(self):
    return '%s (%s)' % (self.title, self.era)

  def get_episodes(self):
    from scenarist.models.dramas import Drama
    episodes = Drama.objects.filter(epic=self)
    return episodes

class EpicAdmin(admin.ModelAdmin):
  ordering = ('era','title',)



