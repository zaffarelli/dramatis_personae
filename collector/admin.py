'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.contrib import admin

from collector.models.skill_ref import SkillRef
from collector.models.skill_ref_admin import SkillRefAdmin
admin.site.register(SkillRef, SkillRefAdmin)

from collector.models.blessing_curse_ref import BlessingCurseRef
from collector.models.blessing_curse_ref_admin import BlessingCurseRefAdmin
admin.site.register(BlessingCurseRef, BlessingCurseRefAdmin)

from collector.models.fics_models import Role, RoleAdmin, Profile, ProfileAdmin, Specie, SpecieAdmin
admin.site.register(Role, RoleAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Specie, SpecieAdmin)

from collector.models.armor_ref_admin import ArmorRefAdmin
from collector.models.armor_ref import ArmorRef
admin.site.register(ArmorRef, ArmorRefAdmin)

from collector.models.talent import TalentRef, TalentRefAdmin
admin.site.register(TalentRef, TalentRefAdmin)


from collector.models.weapon import Weapon, WeaponRefAdmin, WeaponRef
admin.site.register(WeaponRef, WeaponRefAdmin)

from collector.models.shield import Shield, ShieldRefAdmin, ShieldRef
admin.site.register(ShieldRef, ShieldRefAdmin)

from collector.models.benefice_affliction_ref import BeneficeAfflictionRef
from collector.models.benefice_affliction_ref_admin import BeneficeAfflictionRefAdmin
admin.site.register(BeneficeAfflictionRef, BeneficeAfflictionRefAdmin)

from collector.models.tourofduty_ref import TourOfDutyRef
from collector.models.tourofduty_ref_admin import TourOfDutyRefAdmin
admin.site.register(TourOfDutyRef, TourOfDutyRefAdmin)

from collector.models.character_custo import CharacterCusto, CharacterCustoAdmin
admin.site.register(CharacterCusto, CharacterCustoAdmin)

from collector.models.character import Character
from collector.models.character_admin import CharacterAdmin
admin.site.register(Character, CharacterAdmin)

from collector.models.config import Config, ConfigAdmin
admin.site.register(Config, ConfigAdmin)
