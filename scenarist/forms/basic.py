from django import forms
from django.forms import ModelForm
from scenarist.models.epics import Epic
from scenarist.models.dramas import Drama
from scenarist.models.acts import Act
from scenarist.models.events import Event
from scenarist.models.adventures import Adventure
from scenarist.models.scenes import Scene
from scenarist.models.schemes import Scheme
from scenarist.models.backlogs import Backlog
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


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


class AdventureForm(ModelForm):
    class Meta:
        model = Adventure
        fields = '__all__'
        widgets = {
            'dt': DateTimePickerInput(options={
                "format": "YYYY-MM-DD HH:mm:ss",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            })
        }
class BacklogForm(ModelForm):
    class Meta:
        model = Backlog
        fields = '__all__'


class SchemeForm(ModelForm):
    class Meta:
        model = Scheme
        fields = '__all__'
        widgets = {
            'dt': DateTimePickerInput(options={
                "format": "YYYY-MM-DD HH:mm:ss",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            })
        }

class SceneForm(ModelForm):
    class Meta:
        model = Scene
        fields = '__all__'
        widgets = {
            'dt': DateTimePickerInput(options={
                "format": "YYYY-MM-DD HH:mm:ss",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
            })
        }