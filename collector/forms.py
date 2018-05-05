from django import forms
from django.forms import ModelForm
from .models import Character, Skill, SkillRef

class CharacterForm(ModelForm):
  class Meta:
    model = Character
    fields = '__all__'
    exclude = ['pub_date','PA_TOTAL','rid','SA_REC','SA_STA','SA_END','SA_STU','SA_RES','SA_DMG','SA_TOL','SA_HUM','SA_PAS','SA_WYR','SA_SPD','SA_RUN','age','SK_TOTAL']
 
class SkillForm(ModelForm):
  class Meta:
    model = Skill
    fields = '__all__'
    exclude = ('ordo',)


