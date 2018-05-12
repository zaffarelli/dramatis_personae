from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import Character, Skill, Armor, Weapon, BlessingCurse, Talent

class CharacterForm(ModelForm):
  class Meta:
    model = Character
    fields = '__all__'
    exclude = ['pub_date','PA_TOTAL','rid','SA_REC','SA_STA','SA_END', \
    'SA_STU','SA_RES','SA_DMG','SA_TOL','SA_HUM','SA_PAS','SA_WYR', \
    'SA_SPD','SA_RUN','age','SK_TOTAL','TA_TOTAL','BC_TOTAL','challenge', \
    'dm_shortcuts']

SkillFormSet = inlineformset_factory(Character, Skill, fields='__all__', exclude = ('ordo',), extra=5)
TalentFormSet = inlineformset_factory(Character, Talent, fields='__all__', extra=3)
BlessingCurseFormSet = inlineformset_factory(Character, BlessingCurse, fields='__all__', extra=3)
ArmorFormSet = inlineformset_factory(Character, Armor, fields='__all__', extra=3)
WeaponFormSet = inlineformset_factory(Character, Weapon, fields='__all__', extra=3)
