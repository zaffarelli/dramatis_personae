from django.db import models
from django.contrib import admin

class Event(models.Model):
  class Meta:
    ordering = ['date','title']
  from scenarist.models.acts import Act
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  date = models.CharField(default='', max_length=128, blank=True)
  population_count = models.IntegerField(default=0, blank=True)
  antagonists = models.TextField(max_length=640,default='',blank=True)
  protagonists = models.TextField(max_length=640,default='',blank=True)
  description = models.TextField(max_length=640,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  act = models.ForeignKey(Act, null=True, on_delete=models.CASCADE)
  def __str__(self):
    return '%s' % (self.title)

class EventAdmin(admin.ModelAdmin):
  ordering = ('title',)



