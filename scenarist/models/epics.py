#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.db import models
from django.contrib import admin

class Epic(models.Model):
  class Meta:
    ordering = ['era','title']
  era = models.IntegerField(default=5017, blank=True)
  population_count = models.IntegerField(default=0, blank=True)
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  description = models.TextField(max_length=640,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_public = models.BooleanField(default=True)
  is_editable = models.BooleanField(default=True)
  def __str__(self):
    return '%s (%s)' % (self.title, self.era)

class EpicAdmin(admin.ModelAdmin):
  ordering = ('era','title',)



