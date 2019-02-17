from collector.models.characters import Character
import factory
import datetime
from django.utils import timezone
from collector.utils.fs_fics7 import roll


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

class CharacterCheckPAFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  role = '0'+str(roll(8))
  full_name = 'Scholar'+str(role)+' Noattributes'
  
  profile = 'scholar'
  species = 'urthish'
  onsave_reroll_attributes = True
  pub_date = timezone.now()


class CharacterCheckSkillsFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Arthur Unskilled'
  role = '03'
  profile = 'physical'
  species = 'urthish'
  onsave_reroll_skills = True
  pub_date = timezone.now()
