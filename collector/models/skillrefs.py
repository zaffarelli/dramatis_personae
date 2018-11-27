from django.db import models
from django.contrib import admin

class SkillRef(models.Model):
  class Meta:
    ordering = ['reference']
  reference = models.CharField(max_length=200, unique=True)
  is_root = models.BooleanField(default=False)
  is_speciality = models.BooleanField(default=False)
  category = models.CharField(default="un",max_length=2, choices=(('no',"Uncategorized"),('co',"Combat"),('di',"Diplomacy"),('sp',"Spirituality"),('te',"Technical")))
  linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
  
  def __str__(self):
    return '%s %s %s [%s]' % (self.reference,"(R)" if self.is_root else "","(S)" if self.is_speciality else "", self.linked_to.reference if self.linked_to else "-"  )

class SkillRefAdmin(admin.ModelAdmin):
  ordering = ('reference',)
