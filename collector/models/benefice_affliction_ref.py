'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character


class BeneficeAfflictionRef(models.Model):
    class Meta:
      ordering = ['reference','value',]
    reference = models.CharField(max_length=64)
    value = models.IntegerField(default=0)
    category = models.CharField(max_length=2, default='ot', choices=(
        ('ba','Background'),
        ('co','Community'),
        ('po','Possessions'),
        ('ri','Riches'),
        ('st','Status'),
        ('cm','Combat'),
        ('oc','Occult'),
        ('ta','Talent'),
        ('ot','Other')))
    description = models.TextField(max_length=256, default='', null=True, blank=True)
    source = models.CharField(max_length=32, default='FS2CRB', null=True, blank=True)
    emphasis = models.CharField(max_length=64, default='', null=True, blank=True)
    def __str__(self):
        return '%s %s (%d)' % (self.reference,self.emphasis,self.value)
