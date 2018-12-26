#  __                           _     _   
# / _\ ___ ___ _ __   __ _ _ __(_)___| |_ 
# \ \ / __/ _ \ '_ \ / _` | '__| / __| __|
# _\ \ (_|  __/ | | | (_| | |  | \__ \ |_ 
# \__/\___\___|_| |_|\__,_|_|  |_|___/\__|
#                                        
from django.db import models
from django.contrib import admin
from django.urls import reverse
from scenarist.models.story_models import StoryModel
import json

class Epic(StoryModel):
  class Meta:
    ordering = ['era','title']
    
  era = models.IntegerField(default=5017, blank=True)
  population_count = models.IntegerField(default=0, blank=True)

  def get_absolute_url(self):
    return reverse('epic-detail', kwargs={'pk': self.pk})   

  def __str__(self):
    return '%s (%s)' % (self.title, self.era)

class EpicAdmin(admin.ModelAdmin):
  ordering = ('era','title',)



