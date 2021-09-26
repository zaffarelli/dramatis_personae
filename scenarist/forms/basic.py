from django import forms
from django.forms import ModelForm

from scenarist.models.epics import Epic
from scenarist.models.dramas import Drama
from scenarist.models.acts import Act
from scenarist.models.events import Event


class EpicForm(ModelForm):
  class Meta:
    model = Epic
    fields = '__all__'


class DramaForm(ModelForm):
  class Meta:
    model = Drama
    fields = '__all__'


class ActForm(ModelForm):
  class Meta:
    model = Act
    fields = '__all__'


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = '__all__'
