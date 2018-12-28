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
import time

class Drama(StoryModel):
  class Meta:
    ordering = ['epic','chapter','date','title']
    
  from scenarist.models.epics import Epic
  epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
  players = models.TextField(max_length=640,default='',blank=True)
  resolution = models.TextField(default='', max_length=640,blank=True)
  
  def get_absolute_url(self):
    return reverse('drama-detail', kwargs={'pk': self.pk})

  def get_casting(self):
    """ Bring all avatars rids from all relevant text fields"""    
    casting = super().get_casting()
    casting.append(self.fetch_avatars(self.players))
    casting.append(self.fetch_avatars(self.resolution))
    return casting

  def get_episodes(self):
    from scenarist.models.acts import Act
    episodes = Act.objects.filter(drama=self)
    return episodes
    
class DramaAdmin(admin.ModelAdmin):
  ordering = ('epic','chapter','date','title',)



