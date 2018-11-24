from django.db import models
from django.contrib import admin

class Epic(models.Model):
  era = models.IntegerField(default=5017, blank=True)
  population_count = models.IntegerField(default=0, blank=True)
  title = models.CharField(default='', max_length=128, blank=True, unique=True)
  description = models.TextField(max_length=128,default='',blank=True)
  gamemaster = models.CharField(default='zaffarelli@gmail.com', max_length=128, blank=True)
  is_public = models.BooleanField(default=True)
  is_editable = models.BooleanField(default=True)
  def __str__(self):
    return '%s (%s)' % (self.title, self.era)

class EpicAdmin(admin.ModelAdmin):
  ordering = ('era','title',)



