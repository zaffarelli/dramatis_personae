from django.forms import ModelForm, inlineformset_factory
from scenarist.models.cards import Card, CardLink









class CardForm(ModelForm):
    class Meta:
        model = Card
        fields = '__all__'
        exclude = ['full_id']


class CardLinkForm(ModelForm):
    class Meta:
        model = CardLink
        fields = '__all__'





CardLinkFormSet = inlineformset_factory(Card, CardLink, fk_name='cardin', fields='__all__', extra=2, can_delete=True)
