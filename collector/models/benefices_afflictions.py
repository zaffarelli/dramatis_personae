from django.db import models
from django.contrib import admin
from collector.models.characters import Character

class BeneficeAfflictionRef(models.Model):
  class Meta:
    ordering = ['reference']  
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

class BeneficeAffliction(models.Model):
  class Meta:
    ordering = ['beneficeaffliction_ref']
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  beneficeaffliction_ref = models.ForeignKey(BeneficeAfflictionRef, on_delete=models.CASCADE)
  value = models.IntegerField(default=0)
  description = models.TextField(max_length=256, default='', null=True, blank=True)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.name)

  
