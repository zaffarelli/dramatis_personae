'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models

class BlessingCurseRef(models.Model):
  class Meta:
    ordering = ['reference']  
  reference = models.CharField(max_length=64,default='',blank=True)
  value = models.IntegerField(default=0)  
  description = models.TextField(max_length=256,default='',blank=True)
  source = models.CharField(max_length=32, default='FS2CRB', null=True, blank=True)
  def __str__(self):
    return '%s (%+d)' % (self.reference,self.value)



