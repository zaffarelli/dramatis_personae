from django.db import models
from django.contrib import admin

class Drama(models.Model):
  class Meta:
    ordering = ['epic','chapter','date','title']  
  from collector.models.epics import Epic
  date = models.CharField(default='', blank=True, max_length=64)
  place = models.CharField(default='', blank=True, max_length=64)
  chapter = models.CharField(default='', blank=True, max_length=64)
  population_count = models.IntegerField(default=0, blank=True)
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
  description = models.TextField(max_length=640,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_public = models.BooleanField(default=True)
  is_editable = models.BooleanField(default=True)
  def __str__(self):
    return '[%s chapter %s] %s (%s / %s)' % (self.epic.title, self.chapter, self.title, self.date, self.place)

class DramaAdmin(admin.ModelAdmin):
  ordering = ('epic','chapter','date','title',)



