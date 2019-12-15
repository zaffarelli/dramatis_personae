'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.contrib import admin
from collector.models.skill_inline import SkillInline
from collector.models.tourofduty_inline import TourOfDutyInline
from collector.models.blessing_curse_inline import BlessingCurseInline
from collector.models.benefice_affliction_inline import BeneficeAfflictionInline
from collector.models.talent_inline import TalentInline
from collector.models.weapon_inline import WeaponInline
from collector.models.armor_inline import ArmorInline
from collector.models.shield_inline import ShieldInline
from scenarist.models.epics import Epic

def cast_to_dem(modeladmin, request, queryset):
  e = Epic.objects.filter(shortcut="DEM").first()
  queryset.update(epic=e)
  short_description = "Cast to the Deus Ex Machina epic."

def cast_to_blank(modeladmin, request, queryset):
  e = Epic.objects.filter(shortcut="BLK").first()
  queryset.update(epic=e)
  short_description = "Cast to no epic."

def cast_to_antu(modeladmin, request, queryset):
  e = Epic.objects.filter(shortcut="ANTU").first()
  queryset.update(epic=e)
  short_description = "Cast to Abusus Non Tollit Usum"

def make_invisible(modeladmin, request, queryset):
  queryset.update(is_visible=False)
  short_description = "Make invisible"

def make_visible(modeladmin, request, queryset):
  queryset.update(is_visible=True)
  short_description = "Make visible"

def make_public(modeladmin, request, queryset):
  queryset.update(is_public=True)
  short_description = "Make public"

def make_private(modeladmin, request, queryset):
  queryset.update(is_public=False)
  short_description = "Make private"

def make_partial(modeladmin, request, queryset):
  queryset.update(is_partial=True)
  short_description = "Make partial"

def make_complete(modeladmin, request, queryset):
  queryset.update(is_partial=False)
  short_description = "Make complete"

def make_teutonic(modeladmin, request, queryset):
  queryset.update(specie=1)
  short_description = "Make teutonic"

def make_kaanic(modeladmin, request, queryset):
  queryset.update(specie=25)
  short_description = "Make kaanic"

def make_castillan(modeladmin, request, queryset):
  queryset.update(specie=22)
  short_description = "Make castillan"

def make_enquist(modeladmin, request, queryset):
  queryset.update(specie=23)
  short_description = "Make enquist"

class CharacterAdmin(admin.ModelAdmin):
  list_display = ('full_name','specie','role','profile','alliance','use_history_creation','PA_TOTAL','SK_TOTAL','BA_TOTAL','BC_TOTAL','TA_TOTAL','OP','is_public','is_partial','use_only_entrance','is_visible','epic')
  inlines = [
    SkillInline,
    BlessingCurseInline,
    BeneficeAfflictionInline,
    TalentInline,
    WeaponInline,
    ArmorInline,
    ShieldInline,
    TourOfDutyInline,
  ]  
  ordering = ['epic','full_name',]
  actions = [cast_to_blank, cast_to_dem, cast_to_antu, make_invisible, make_visible, make_teutonic, make_kaanic, make_castillan, make_enquist, make_public, make_private, make_partial, make_complete]
  exclude = ['SA_REC','SA_STA','SA_END','SA_STU','SA_RES','SA_DMG','SA_TOL','SA_HUM','SA_PAS','SA_WYR','SA_SPD','SA_RUN','PA_TOTAL','SK_TOTAL','TA_TOTAL','BC_TOTAL','BA_TOTAL']