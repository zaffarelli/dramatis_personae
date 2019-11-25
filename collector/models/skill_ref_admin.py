'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.contrib import admin

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

def change_to_spi(modeladmin, request, queryset):
  queryset.update(group='SPI')
  short_description = "Change skills to the SPI group"  

def change_to_und(modeladmin, request, queryset):
  queryset.update(group='UND')
  short_description = "Change skills to the UND group"  

def change_to_dip(modeladmin, request, queryset):
  queryset.update(group='DIP')
  short_description = "Change skills to the DIP group"

def set_common(modeladmin, request, queryset):
  queryset.update(is_common=True)
  short_description = "Change skills to common"

def set_uncommon(modeladmin, request, queryset):
  queryset.update(is_common=False)
  short_description = "Change skills to uncommon"
    




class SkillRefAdmin(admin.ModelAdmin):
  ordering = ['is_speciality','reference']
  list_display = ('reference','is_root','is_speciality','is_common','group')
  actions = [change_to_awa, change_to_soc, change_to_edu, change_to_fig, change_to_con, change_to_tin, change_to_per, change_to_bod, set_common, set_uncommon]

