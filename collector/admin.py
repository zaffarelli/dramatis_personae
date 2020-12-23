"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.contrib import admin

from collector.models.skill import SkillRef, SkillRefAdmin
admin.site.register(SkillRef, SkillRefAdmin)

from collector.models.blessing_curse import BlessingCurseRef, BlessingCurseRefAdmin
admin.site.register(BlessingCurseRef, BlessingCurseRefAdmin)

from collector.models.fics_models import Specie, SpecieAdmin
admin.site.register(Specie, SpecieAdmin)

from collector.models.armor import ArmorRef, ArmorRefAdmin
admin.site.register(ArmorRef, ArmorRefAdmin)

# from collector.models.talent import TalentRef, TalentRefAdmin
# admin.site.register(TalentRef, TalentRefAdmin)

from collector.models.weapon import WeaponRef, WeaponRefAdmin
admin.site.register(WeaponRef, WeaponRefAdmin)

from collector.models.shield import ShieldRefAdmin, ShieldRef
admin.site.register(ShieldRef, ShieldRefAdmin)

from collector.models.benefice_affliction import BeneficeAfflictionRef, BeneficeAfflictionRefAdmin
admin.site.register(BeneficeAfflictionRef, BeneficeAfflictionRefAdmin)

from collector.models.tourofduty import TourOfDutyRef
from collector.models.tourofduty_admin import TourOfDutyRefAdmin
admin.site.register(TourOfDutyRef, TourOfDutyRefAdmin)

from collector.models.character_custo import CharacterCusto
from collector.models.character_custo_admin import CharacterCustoAdmin
admin.site.register(CharacterCusto, CharacterCustoAdmin)

from collector.models.character import Character
from collector.models.character_admin import CharacterAdmin
admin.site.register(Character, CharacterAdmin)

from collector.models.loot import Loot, LootAdmin
admin.site.register(Loot, LootAdmin)

from collector.models.gear import Gear, GearAdmin
admin.site.register(Gear, GearAdmin)

from collector.models.config import Config, ConfigAdmin
admin.site.register(Config, ConfigAdmin)

from collector.models.spacecraft import ShipSystem, ShipSystemAdmin
admin.site.register(ShipSystem, ShipSystemAdmin)

from collector.models.spacecraft import ShipRef,ShipRefAdmin
admin.site.register(ShipRef, ShipRefAdmin)

from collector.models.spacecraft import Spaceship, SpaceshipAdmin
admin.site.register(Spaceship, SpaceshipAdmin)

from collector.models.spacecraft import ShipSystemSlot, ShipSystemSlotAdmin
admin.site.register(ShipSystemSlot, ShipSystemSlotAdmin)

from collector.models.spacecraft import ShipSection, ShipSectionAdmin
admin.site.register(ShipSection, ShipSectionAdmin)

from collector.models.system import System, SystemAdmin, OrbitalItem, OrbitalItemAdmin
admin.site.register(System, SystemAdmin)
admin.site.register(OrbitalItem, OrbitalItemAdmin)

from collector.models.ritual import RitualRef, RitualRefAdmin
admin.site.register(RitualRef, RitualRefAdmin)

from collector.models.cyberware import CyberwareRef, CyberwareRefAdmin, Cyberfeature, CyberfeatureAdmin
admin.site.register(Cyberfeature, CyberfeatureAdmin)
admin.site.register(CyberwareRef, CyberwareRefAdmin)

from collector.models.user import Profile, ProfileAdmin
admin.site.register(Profile, ProfileAdmin)

from collector.models.bloke import Bloke, BlokeAdmin
admin.site.register(Bloke, BlokeAdmin)

from collector.models.investigator import Investigator, InvestigatorAdmin
admin.site.register(Investigator, InvestigatorAdmin)