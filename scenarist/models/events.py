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

class Event(StoryModel):
  class Meta:
    ordering = ['date','title']

  from scenarist.models.acts import Act
  act = models.ForeignKey(Act, null=True, on_delete=models.CASCADE)
  friends = models.TextField(default='', max_length=640,blank=True)
  foes = models.TextField(default='', max_length=640,blank=True)
  resolution = models.TextField(default='', max_length=640,blank=True)
  challenge = models.PositiveIntegerField(default=1)

  def get_absolute_url(self):
    return reverse('event-detail', kwargs={'pk': self.pk})

class EventAdmin(admin.ModelAdmin):
  ordering = ('title',)



