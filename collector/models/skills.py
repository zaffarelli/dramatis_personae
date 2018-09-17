from django.db import models
from django.contrib import admin
from collector.models.characters import Character
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

class SkillRef(models.Model):
  reference = models.CharField(max_length=200, unique=True)
  is_root = models.BooleanField(default=False)
  is_speciality = models.BooleanField(default=False)
  category = models.CharField(default="un",max_length=2, choices=(('no',"Uncategorized"),('co',"Combat"),('di',"Diplomacy"),('sp',"Spirituality"),('te',"Technical")))
  linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
  ordering = ('reference',)
  def __str__(self):
    return '%s %s %s [%s]' % (self.reference,"(R)" if self.is_root else "","(S)" if self.is_speciality else "", self.linked_to.reference if self.linked_to else "-"  )

class Skill(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
  value = models.PositiveIntegerField(default=0)
  ordering = ('skill_ref.reference')  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.skill_ref.reference)
  def fix(self):
    pass


@receiver(pre_save, sender=Skill, dispatch_uid='update_skill')
def update_skill(sender, instance, **kwargs):
  instance.fix()



class SkillRefAdmin(admin.ModelAdmin):
  ordering = ('reference',)

class SkillAdmin(admin.ModelAdmin):
  ordering = ('character','skill_ref',)


