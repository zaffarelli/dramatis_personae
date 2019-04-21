'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.contrib import admin

from collector.models.skillrefs import SkillRef, SkillRefAdmin
from collector.models.skills import Skill, SkillAdmin
from collector.models.weapons import Weapon, WeaponAdmin, WeaponRefAdmin, WeaponRef
from collector.models.armors import Armor, ArmorAdmin, ArmorRefAdmin, ArmorRef
from collector.models.shields import Shield, ShieldAdmin, ShieldRefAdmin, ShieldRef
from collector.models.fics_models import Role, RoleAdmin, Profile, ProfileAdmin, Specie, SpecieAdmin
from collector.models.characters import Character
from collector.models.characters_admin import CharacterAdmin
from collector.models.benefices_afflictions import BeneficeAfflictionRef, BeneficeAfflictionRefAdmin
from collector.models.configs import Config, ConfigAdmin


admin.site.register(Role, RoleAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Specie, SpecieAdmin)

admin.site.register(SkillRef, SkillRefAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(Weapon, WeaponAdmin)
admin.site.register(WeaponRef, WeaponRefAdmin)
admin.site.register(Armor, ArmorAdmin)
admin.site.register(ArmorRef, ArmorRefAdmin)
admin.site.register(Shield, ShieldAdmin)
admin.site.register(ShieldRef, ShieldRefAdmin)
admin.site.register(BeneficeAfflictionRef, BeneficeAfflictionRefAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Config, ConfigAdmin)

