from django.db import models

class Act(models.Model):
  title = models.CharField(max_length=128)
  date = models.CharField(max_length=64)
  place = models.CharField(max_length=64)
  friends = models.TextField(default='', max_length=128,blank=True)
  foes = models.TextField(default='', max_length=128,blank=True)
  narrative = models.TextField(default='', max_length=512,blank=True)
  resolution = models.TextField(default='', max_length=512,blank=True)
  def __str__(self):
    return '[%s](%s) %s'%(self.date,self.place,self.title)
