#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.db import models
from django.contrib import admin

class Act(models.Model):
  class Meta:
    ordering = ['date','title']
  from scenarist.models.dramas import Drama
  title = models.CharField(max_length=128)
  date = models.CharField(max_length=64)
  place = models.CharField(max_length=64)
  drama = models.ForeignKey(Drama, null=True, on_delete=models.CASCADE)
  friends = models.TextField(default='', max_length=640,blank=True)
  foes = models.TextField(default='', max_length=640,blank=True)
  description = models.TextField(default='', max_length=1280,blank=True)
  resolution = models.TextField(default='', max_length=640,blank=True)
  def __str__(self):
    return '[%s](%s) %s'%(self.date,self.place,self.title)

class ActAdmin(admin.ModelAdmin):
  ordering = ('date','title',)
