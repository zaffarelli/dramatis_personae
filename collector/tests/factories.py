from collector.models import Character
import factory
import datetime
from django.utils import timezone


class CharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Tastus Fabulus'
  pub_date = timezone.now()

class AutobuildCharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Tastus Autobuildus'
  pub_date = timezone.now()
