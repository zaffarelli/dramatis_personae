from django.db import models
from django.contrib import admin

class Act(models.Model):
  from collector.models.epics import Epic
  title = models.CharField(max_length=128)
  date = models.CharField(max_length=64)
  place = models.CharField(max_length=64)
  friends = models.TextField(default='', max_length=128,blank=True)
  epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
  foes = models.TextField(default='', max_length=128,blank=True)
  narrative = models.TextField(default='', max_length=512,blank=True)
  resolution = models.TextField(default='', max_length=512,blank=True)
  def __str__(self):
    return '[%s](%s) %s'%(self.date,self.place,self.title)

class ActAdmin(admin.ModelAdmin):
  ordering = ('title','date',)