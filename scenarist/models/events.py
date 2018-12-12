#   _________                                .__          __   
#  /   _____/ ____  ____   ____ _____ _______|__| _______/  |_ 
#  \_____  \_/ ___\/ __ \ /    \\__  \\_  __ \  |/  ___/\   __\
#  /        \  \__\  ___/|   |  \/ __ \|  | \/  |\___ \  |  |  
# /_______  /\___  >___  >___|  (____  /__|  |__/____  > |__|  
#         \/     \/    \/     \/     \/              \/        
from django.db import models
from django.contrib import admin

class Event(models.Model):
  class Meta:
    ordering = ['date','title']
  from scenarist.models.acts import Act
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  date = models.CharField(default='', max_length=128, blank=True)
  act = models.ForeignKey(Act, null=True, on_delete=models.CASCADE)
  friends = models.TextField(default='', max_length=640,blank=True)
  foes = models.TextField(default='', max_length=640,blank=True)
  description = models.TextField(default='', max_length=1280,blank=True)
  resolution = models.TextField(default='', max_length=640,blank=True)
  challenge = models.PositiveIntegerField(default=1)
  def __str__(self):
    return '%s' % (self.title)

class EventAdmin(admin.ModelAdmin):
  ordering = ('title',)



