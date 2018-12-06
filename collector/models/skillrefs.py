from django.db import models
from django.contrib import admin

class SkillRef(models.Model):
  class Meta:
    ordering = ['group','reference']
  reference = models.CharField(max_length=200, unique=True)
  is_root = models.BooleanField(default=False)
  is_speciality = models.BooleanField(default=False)
  category = models.CharField(default="un",max_length=2, choices=(('no',"Uncategorized"),('co',"Combat"),('di',"Diplomacy"),('sp',"Spirituality"),('te',"Technical")))
  group = models.CharField(default="EDU",max_length=3, choices=(('EDU',"Education"),('FIG',"Combat"),('AWA',"Awareness"),('BOD',"Physical"),('TIN',"Tinkering"),('PER',"Performance"),('SOC',"Social"),('CON',"Control")))
  linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
  
  def __str__(self):
    return '%s %s %s %s [%s]' % (self.reference,self.group,"(R)" if self.is_root else "","(S)" if self.is_speciality else "", self.linked_to.reference if self.linked_to else "-"  )

def change_to_awa(modeladmin, request, queryset):
  queryset.update(group='AWA')
  short_description = "Change skills to the AWA group"

def change_to_bod(modeladmin, request, queryset):
  queryset.update(group='BOD')
  short_description = "Change skills to the BOD group"

def change_to_edu(modeladmin, request, queryset):
  queryset.update(group='EDU')
  short_description = "Change skills to the EDU group"

def change_to_per(modeladmin, request, queryset):
  queryset.update(group='PER')
  short_description = "Change skills to the PER group"

def change_to_fig(modeladmin, request, queryset):
  queryset.update(group='FIG')
  short_description = "Change skills to the FIG group"

def change_to_con(modeladmin, request, queryset):
  queryset.update(group='CON')
  short_description = "Change skills to the CON group"

def change_to_soc(modeladmin, request, queryset):
  queryset.update(group='SOC')
  short_description = "Change skills to the SOC group"

def change_to_tin(modeladmin, request, queryset):
  queryset.update(group='TIN')
  short_description = "Change skills to the TIN group"  
  
class SkillRefAdmin(admin.ModelAdmin):
  ordering = ['reference']
  actions = [change_to_awa, change_to_soc, change_to_edu, change_to_fig, change_to_con, change_to_tin, change_to_per, change_to_bod]



