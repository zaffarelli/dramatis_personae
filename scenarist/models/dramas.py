#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.db import models
from django.contrib import admin
from django.urls import reverse

class Drama(models.Model):
  class Meta:
    ordering = ['epic','chapter','date','title']  
  from scenarist.models.epics import Epic
  date = models.CharField(default='', blank=True, max_length=64)
  place = models.CharField(default='', blank=True, max_length=64)
  chapter = models.CharField(default='', blank=True, max_length=64)
  population_count = models.IntegerField(default=0, blank=True)
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
  description = models.TextField(max_length=640,default='',blank=True)
  players = models.TextField(max_length=640,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_public = models.BooleanField(default=True)
  is_editable = models.BooleanField(default=True)
  def __str__(self):
    return '[%s chapter %s] %s (%s / %s)' % (self.epic.title, self.chapter, self.title, self.date, self.place)
  def get_absolute_url(self):
    return reverse('drama-detail', kwargs={'pk': self.pk})
class DramaAdmin(admin.ModelAdmin):
  ordering = ('epic','chapter','date','title',)



