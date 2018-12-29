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

class Event(StoryModel):
  class Meta:
    ordering = ['chapter','title']

  from scenarist.models.acts import Act
  act = models.ForeignKey(Act, null=True, on_delete=models.CASCADE)
  friends = models.TextField(default='', max_length=640,blank=True)
  foes = models.TextField(default='', max_length=640,blank=True)
  resolution = models.TextField(default='', max_length=640,blank=True)
  challenge = models.PositiveIntegerField(default=1)
  anchor = models.CharField(default='', max_length=256, blank=True)
  estimated_gametime = models.PositiveIntegerField(default=1)

  def get_casting(self):
    """ Bring all avatars rids from all relevant text fields"""    
    casting = super().get_casting()
    casting.append(self.fetch_avatars(self.friends))
    casting.append(self.fetch_avatars(self.foes))
    casting.append(self.fetch_avatars(self.resolution))
    return casting


  def get_absolute_url(self):
    return reverse('event-detail', kwargs={'pk': self.pk})

class EventAdmin(admin.ModelAdmin):
  ordering = ('chapter','title',)



