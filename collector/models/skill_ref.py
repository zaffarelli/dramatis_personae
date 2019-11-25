'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.utils import fics_references

class SkillRef(models.Model):
  class Meta:
    ordering = ['is_speciality','reference']
    verbose_name = "Skill Reference"    
  reference = models.CharField(max_length=200, unique=True)
  is_root = models.BooleanField(default=False)
  is_speciality = models.BooleanField(default=False)
  is_common = models.BooleanField(default=True)
  #refcode = models.CharField(max_length=16, default='none')
  group = models.CharField(default="EDU",max_length=3, choices=fics_references.GROUPCHOICES)
  linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
  
  
  def __str__(self):
    return '%s %s %s %s [%s]' % (self.reference,self.group,"(R)" if self.is_root else "","(S)" if self.is_speciality else "", self.linked_to.reference if self.linked_to else "-"  )

