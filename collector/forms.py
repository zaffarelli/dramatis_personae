from django.forms import ModelForm
from .models import Character

class PersonaForm(ModelForm):
	class Meta:
		model = Character
		fields = '__all__'
