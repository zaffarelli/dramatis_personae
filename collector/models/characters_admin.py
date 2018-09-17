from django.contrib import admin
from collector.models.skillsinline import SkillInline
from collector.models.blessingcursesinline import BlessingCurseInline
from collector.models.talentsinline import TalentInline
from collector.models.weaponsinline import WeaponInline
from collector.models.armorsinline import ArmorInline

class CharacterAdmin(admin.ModelAdmin):
  inlines = [
    SkillInline,
    BlessingCurseInline,
    TalentInline,
    WeaponInline,
    ArmorInline
  ]  
  ordering = ('full_name',)
