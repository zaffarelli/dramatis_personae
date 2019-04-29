'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django import forms
from django.forms import ModelForm, inlineformset_factory
from collector.models.characters import Character
from collector.models.skills import Skill
from collector.models.armors import Armor
from collector.models.weapons import Weapon
from collector.models.shields import Shield
from collector.models.blessings_curses import BlessingCurse
from collector.models.benefices_afflictions import BeneficeAffliction
from collector.models.talents import Talent

class CharacterForm(ModelForm):
  class Meta:
    model = Character
    fields = '__all__'
    exclude = ['pub_date','PA_TOTAL','rid','SA_REC','SA_STA','SA_END', \
    'SA_STU','SA_RES','SA_DMG','SA_TOL','SA_HUM','SA_PAS','SA_WYR', \
    'SA_SPD','SA_RUN','age','SK_TOTAL','TA_TOTAL','BC_TOTAL','BA_TOTAL','challenge', \
    'gm_shortcuts','alliancehash','OP','AP','stars','weapon_cost','armor_cost','shield_cost','score']

SkillFormSet = inlineformset_factory(Character, Skill, fields='__all__', extra=5, can_delete = True)
TalentFormSet = inlineformset_factory(Character, Talent, fields='__all__',extra=3, can_delete = True)
BlessingCurseFormSet = inlineformset_factory(Character, BlessingCurse, fields='__all__', extra=3, can_delete = True)
BeneficeAfflictionFormSet = inlineformset_factory(Character, BeneficeAffliction, fields='__all__', extra=3, can_delete = True)
ArmorFormSet = inlineformset_factory(Character, Armor, fields='__all__', extra=3, can_delete = True)
WeaponFormSet = inlineformset_factory(Character, Weapon, fields='__all__', extra=3, can_delete = True)
ShieldFormSet = inlineformset_factory(Character, Shield, fields='__all__', extra=3, can_delete = True)
