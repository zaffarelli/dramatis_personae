'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.characters import Character
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

class Talent(models.Model):
  class Meta:
    ordering = ['name']
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  name = models.CharField(max_length=64,default='',blank=True)
  attributes_list = models.CharField(max_length=128,default='',blank=True)
  skills_list = models.CharField(max_length=128,default='',blank=True)
  description = models.TextField(max_length=1024,default='',blank=True)
  AP = models.IntegerField(default=0)
  OP = models.IntegerField(default=0)
  value = models.IntegerField(default=0)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.name)
  def fix(self):
    self.value = self.AP*3 + self.OP
@receiver(pre_save, sender=Talent, dispatch_uid='update_talent')
def update_talent(sender, instance, **kwargs):
  instance.fix()
  
