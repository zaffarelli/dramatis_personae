'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django import forms
from django.forms import ModelForm, inlineformset_factory
from collector.models.character import Character
from collector.models.tourofduty import TourOfDutyRef, TourOfDuty
from collector.models.skill import Skill, SkillModificator
from collector.models.armor import Armor
from collector.models.weapon import Weapon
from collector.models.shield import Shield
from collector.models.blessing_curse import BlessingCurse, BlessingCurseModificator
from collector.models.benefice_affliction import BeneficeAffliction, BeneficeAfflictionModificator
from collector.models.talent import Talent
from collector.models.spacecraft import ShipRef,ShipSection, ShipSystemSlot
from collector.models.system import System, OrbitalItem
from collector.models.bloke import Bloke

class CharacterForm(ModelForm):
    class Meta:
        model = Character
        fields = '__all__'
        exclude = ['pub_date','PA_TOTAL','rid','SA_REC','SA_STA','SA_END','SA_STU',
               'SA_RES','SA_DMG','SA_TOL','SA_HUM','SA_PAS','SA_WYR', 'SA_SPD',
               'SA_RUN','age','SK_TOTAL','TA_TOTAL','BC_TOTAL','BA_TOTAL','challenge',
               'gm_shortcuts','alliancehash','OP','AP','stars','weapon_cost',
               'armor_cost','shield_cost','score', 'lifepath_total', 'OCC_LVL',
               'OCC_DRK', 'PA_STR','PA_BOD', 'PA_CON', 'PA_MOV', 'PA_INT',
               'PA_WIL', 'PA_TEM', 'PA_PRE', 'PA_TEC', 'PA_REF', 'PA_AGI',
               'PA_AWA', 'OCC_LVL', 'OCC_DRK','spotlight',
               'onsave_reroll_attributes', 'onsave_reroll_skills', 'importance', 'fights', 'victories', 'victory_rating', 'fencing_league' ]

class TourOfDutyRefForm(ModelForm):
    class Meta:
        model = TourOfDutyRef
        fields = '__all__'
        exclude = ['OP','AP','value','description']

class ShipRefForm(ModelForm):
     class Meta:
         model = ShipRef
         fields = '__all__'
         exclude = ['dim_length','dim_width','dim_height','size_rating']



# Character
SkillFormSet = inlineformset_factory(Character, Skill, fields='__all__', extra=10, can_delete = True)
TalentFormSet = inlineformset_factory(Character, Talent, fields='__all__',extra=3, can_delete = True)
BlessingCurseFormSet = inlineformset_factory(Character, BlessingCurse, fields='__all__', extra=3, can_delete = True)
BeneficeAfflictionFormSet = inlineformset_factory(Character, BeneficeAffliction, fields='__all__', extra=3, can_delete = True)
ArmorFormSet = inlineformset_factory(Character, Armor, fields='__all__', extra=3, can_delete = True)
WeaponFormSet = inlineformset_factory(Character, Weapon, fields='__all__', extra=3, can_delete = True)
ShieldFormSet = inlineformset_factory(Character, Shield, fields='__all__', extra=3, can_delete = True)
TourOfDutyFormSet = inlineformset_factory(Character,TourOfDuty, fields='__all__', extra=9, can_delete = True)
BlokeFormSet = inlineformset_factory(Character,Bloke, fk_name='player', fields='__all__', extra=3, can_delete = True)

# Tour of duty
SkillModificatorFormSet = inlineformset_factory(TourOfDutyRef, SkillModificator, fields='__all__', extra=5, can_delete = True)
BlessingCurseModificatorFormSet = inlineformset_factory(TourOfDutyRef, BlessingCurseModificator, fields='__all__', extra=3, can_delete = True)
BeneficeAfflictionModificatorFormSet = inlineformset_factory(TourOfDutyRef, BeneficeAfflictionModificator, fields='__all__', extra=3, can_delete = True)

# ShipRef
ShipSectionFormSet = inlineformset_factory(ShipRef,ShipSection, fields='__all__',extra=1, can_delete = True)

# ShipSection
ShipSystemSlotFormSet = inlineformset_factory(ShipSection,ShipSystemSlot, fields='__all__',extra=1, can_delete = True)

# System
OrbitalItemFormSet = inlineformset_factory(System,OrbitalItem, fields='__all__',extra=1, can_delete = True)
