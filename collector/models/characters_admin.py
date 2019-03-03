from django.contrib import admin
from collector.models.skillsinline import SkillInline
from collector.models.blessingcursesinline import BlessingCurseInline
from collector.models.benefices_afflictions import BeneficeAfflictionInline
from collector.models.talentsinline import TalentInline
from collector.models.weaponsinline import WeaponInline
from collector.models.armorsinline import ArmorInline
from collector.models.shieldsinline import ShieldInline

def cast_to_dem(modeladmin, request, queryset):
  queryset.update(epic=1)
  short_description = "Cast to the Deus Ex Machina epic."

def cast_to_blank(modeladmin, request, queryset):
  queryset.update(epic=2)
  short_description = "Cast to no epic."

def make_invisible(modeladmin, request, queryset):
  queryset.update(visible=False)
  short_description = "Make invisible"

def make_visible(modeladmin, request, queryset):
  queryset.update(visible=True)
  short_description = "Make visible"

class CharacterAdmin(admin.ModelAdmin):
  list_display = ('full_name','castrole','castprofile','species','alliance','PA_TOTAL','SK_TOTAL','BA_TOTAL','BC_TOTAL','TA_TOTAL','OP','visible','epic')
  inlines = [
    SkillInline,
    BlessingCurseInline,
    BeneficeAfflictionInline,
    TalentInline,
    WeaponInline,
    ArmorInline,
    ShieldInline,
  ]  
  ordering = ['epic','full_name',]
  actions = [cast_to_blank, cast_to_dem, make_invisible, make_visible]

  
