#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.db import models
from django.contrib import admin
from django.urls import reverse
import json

class Drama(models.Model):
  class Meta:
    ordering = ['epic','chapter','date','title']  
  from scenarist.models.epics import Epic
  date = models.CharField(default='', blank=True, max_length=64)
  place = models.CharField(default='', blank=True, max_length=64)
  chapter = models.CharField(default='', blank=True, max_length=64)
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
  players = models.TextField(max_length=640,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  friends = models.TextField(default='', max_length=640,blank=True)
  foes = models.TextField(default='', max_length=640,blank=True)
  description = models.TextField(default='', max_length=1280,blank=True)
  resolution = models.TextField(default='', max_length=640,blank=True)  
  def __str__(self):
    return '[%s chapter %s] %s (%s / %s)' % (self.epic.title, self.chapter, self.title, self.date, self.place)
  def get_absolute_url(self):
    return reverse('drama-detail', kwargs={'pk': self.pk})
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)
    
class DramaAdmin(admin.ModelAdmin):
  ordering = ('epic','chapter','date','title',)



