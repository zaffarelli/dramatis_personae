"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django import forms
from django.forms import ModelForm, inlineformset_factory
from collector.models.investigator import Investigator
from collector.models.coc7_occupation import Coc7Occupation
from collector.models.coc7_skill import Coc7Skill, Coc7SkillModificator


class InvestigatorForm(ModelForm):
    class Meta:
        model = Investigator
        # fields = '__all__'
        fields = ['full_name','occupation','age','narrative','gender']
        # exclude = ['pub_date', 'rid', 'need_pdf', 'need_fix','age','importance','nationality','C_FOR','C_CON', 'C_TAI', 'C_CHANCE', 'C_DEX','C_']

Coc7SkillFormSet = inlineformset_factory(Investigator, Coc7Skill, fields='__all__', extra=5, can_delete=True)

class OccupationForm(ModelForm):
    class Meta:
        model = Coc7Occupation
        fields = '__all__'

Coc7SkillModificatorFormSet = inlineformset_factory(Coc7Occupation, Coc7SkillModificator, fields='__all__', extra=5, can_delete=True)

