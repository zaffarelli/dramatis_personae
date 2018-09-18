from collector.models.characters import Character
import factory
import datetime
from django.utils import timezone


class CharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Tastus Fabulus'
  pub_date = timezone.now()

class VeteranGuilderFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Roman Van Dyke'
  role = '05'
  profile = 'guilder'
  pub_date = timezone.now()

class UnbuildableCharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Rico Unbuildable'
  role = '00'
  profile = 'undefined'
  pub_date = timezone.now()
