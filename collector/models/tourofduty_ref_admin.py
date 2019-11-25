'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.contrib import admin
from collector.models.skill_modificator_inline import SkillModificatorInline
from collector.models.blessing_curse_modificator_inline import BlessingCurseModificatorInline
from collector.models.benefice_affliction_modificator_inline import BeneficeAfflictionModificatorInline


def set_apprenticeship(modeladmin, request, queryset):
  queryset.update(category="Apprenticeship")
  short_description = "Set to Apprenticeship"

def set_racial(modeladmin, request, queryset):
  queryset.update(category="Racial")
  short_description = "Set to Racial"

def set_early_career(modeladmin, request, queryset):
  queryset.update(category="Early Career")
  short_description = "Set to Early Career"

def set_upbringing(modeladmin, request, queryset):
  queryset.update(category="Upbringing")
  short_description = "Set to Upbringing"


def refix(modeladmin, request, queryset):
  for tour_of_duty_ref in queryset:
    tour_of_duty_ref.fix()
    tour_of_duty_ref.save()
  short_description = "Do fix"

class TourOfDutyRefAdmin(admin.ModelAdmin):
  ordering = ['caste','category','reference','-value']
  list_display = ('reference','category','caste','source','AP','OP','value','description')
  exclude = ['OP','AP','value','description']
  actions = [ refix, set_upbringing, set_early_career, set_racial, set_apprenticeship ]
  inlines = [
    SkillModificatorInline,
    BlessingCurseModificatorInline,
    BeneficeAfflictionModificatorInline,    
  ]
