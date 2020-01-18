'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.contrib import admin

def make_occult(modeladmin, request, queryset):
  queryset.update(category="oc")
  short_description = "Make Occult"

def make_combat(modeladmin, request, queryset):
  queryset.update(category="cm")
  short_description = "Make Combat"

def make_talent(modeladmin, request, queryset):
  queryset.update(category="ta")
  short_description = "Make Talent"

def make_possession(modeladmin, request, queryset):
  queryset.update(category="po")
  short_description = "Make possession"

def make_riches(modeladmin, request, queryset):
  queryset.update(category="ri")
  short_description = "Make riches"

class BeneficeAfflictionRefAdmin(admin.ModelAdmin):
    ordering = ('category','reference','-value')
    list_display = ('reference','emphasis','value','category','description','source')
    actions = [make_occult, make_combat, make_talent, make_riches, make_possession]
