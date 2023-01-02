from django.forms import ModelForm, inlineformset_factory
from scenarist.models.epics import Epic
from scenarist.models.dramas import Drama
from scenarist.models.acts import Act
from scenarist.models.events import Event
from scenarist.models.adventures import Adventure
from scenarist.models.scenes import Scene
from scenarist.models.schemes import Scheme
from scenarist.models.backlogs import Backlog
from scenarist.models.cards import Card, CardLink



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


class BacklogForm(ModelForm):
    class Meta:
        model = Backlog
        fields = '__all__'


class SchemeForm(ModelForm):
    class Meta:
        model = Scheme
        fields = '__all__'


class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        exclude = ['full_id']


class CardLinkForm(ModelForm):
    class Meta:
        model = CardLink
        fields = '__all__'



class SceneForm(ModelForm):
    class Meta:
        model = Scene
        fields = '__all__'


CardLinkFormSet = inlineformset_factory(Card, CardLink, fk_name='cardin', fields='__all__', extra=2, can_delete=True)
