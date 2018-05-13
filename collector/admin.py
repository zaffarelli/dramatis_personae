from django.contrib import admin

# Register your models here.
from .models import  Skill, SkillRef, SkillAdmin, SkillRefAdmin, Weapon, WeaponAdmin, WeaponRefAdmin,  WeaponRef, Armor, ArmorAdmin, ArmorRefAdmin,  ArmorRef, Shield, ShieldAdmin, ShieldRefAdmin,  ShieldRef, Character, CharacterAdmin


admin.site.register(SkillRef, SkillRefAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(WeaponRef, WeaponRefAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(ArmorRef, ArmorRefAdmin)
admin.site.register(Shield, ShieldAdmin)
admin.site.register(ShieldRef, ShieldRefAdmin)
admin.site.register(Character, CharacterAdmin)


