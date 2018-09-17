from django.db import models
from django.contrib import admin

class BeneficeAfflictionRef(models.Model):
  reference = models.CharField(max_length=64)
  value = models.IntegerField(default=0)
  category = models.CharField(max_length=2, default='ot', choices=(('ba',"Background"),('co',"Community"),('po',"Possessions"),('ri',"Riches"),('st',"Status"),('ot',"Other")))
  description = models.TextField(max_length=256, default='', null=True, blank=True)
  source = models.CharField(max_length=32, default='', null=True, blank=True)
  ordering = ('reference',)
  def __str__(self):
    return '%s (%d)' % (self.reference,self.value)

class BeneficeAfflictionRefAdmin(admin.ModelAdmin):
  ordering = ('reference',)

class BeneficeAfflictionRefInline(admin.TabularInline):
  model = BeneficeAfflictionRef

