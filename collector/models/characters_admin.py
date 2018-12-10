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

class CharacterAdmin(admin.ModelAdmin):
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
  actions = [cast_to_blank, cast_to_dem]

