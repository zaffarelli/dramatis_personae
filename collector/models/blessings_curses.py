from django.db import models
from collector.models.characters import Character

class BlessingCurse(models.Model):
  class Meta:
    ordering = ['name']
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  name = models.CharField(max_length=64,default='',blank=True)
  description = models.TextField(max_length=128,default='',blank=True)
  value = models.IntegerField(default=0)  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.name)



