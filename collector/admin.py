from django.contrib import admin

# Register your models here.
from .models import Character, SkillRef, Skill, CharacterAdmin, SkillAdmin, SkillRefAdmin,WeaponAdmin, WeaponRefAdmin, Weapon, WeaponRef, ArmorAdmin, ArmorRefAdmin, Armor, ArmorRef


admin.site.register(SkillRef, SkillRefAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(WeaponRef, WeaponRefAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(ArmorRef, ArmorRefAdmin)
admin.site.register(Character, CharacterAdmin)


