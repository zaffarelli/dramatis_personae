from django.db import models
from django.contrib import admin

class Drama(models.Model):
  class Meta:
    ordering = ['epic','date','title']  
  from collector.models.epics import Epic
  date = models.CharField(max_length=64)
  place = models.CharField(max_length=64)
  population_count = models.IntegerField(default=0, blank=True)
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  epic = models.ForeignKey(Epic, null=True, on_delete=models.CASCADE)
  description = models.TextField(max_length=128,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_public = models.BooleanField(default=True)
  is_editable = models.BooleanField(default=True)
  def __str__(self):
    return '%s (%s / %s)' % (self.title, self.date, self.place)

class DramaAdmin(admin.ModelAdmin):
  ordering = ('epic','date','title',)



