from django.db import models
from django.contrib import admin
from collector.models.characters import *
from collector.models.skillrefs import *
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

class Skill(models.Model):
  class Meta:
    ordering = ['skill_ref',]  
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
  value = models.PositiveIntegerField(default=0)
  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.skill_ref.reference)
  def fix(self):
    pass

@receiver(pre_save, sender=Skill, dispatch_uid='update_skill')
def update_skill(sender, instance, **kwargs):
  instance.fix()

class SkillAdmin(admin.ModelAdmin):
  ordering = ('character','skill_ref',)


