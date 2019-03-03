from collector.models.characters import Character
import factory
import datetime
from django.utils import timezone
from collector.utils.fs_fics7 import roll
from collector.models.fics_models import CastRole, CastProfile


class CharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Tastus Fabulus'
  pub_date = timezone.now()

class VeteranGuilderFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Roman Van Dyke'
  castrole = CastRole.objects.filter(value=5).first()
  castprofile = CastProfile.objects.filter(reference='Guilder').first()
  pub_date = timezone.now()

class UnbuildableCharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Rico Unbuildable'
  castrole = CastRole.objects.filter(value=0).first()
  castprofile = CastProfile.objects.filter(reference='Undefined').first()
  pub_date = timezone.now()

class CharacterCheckPAFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  castrole = CastRole.objects.filter(value=roll(8)).first()
  full_name = 'Scholar'+str(castrole.value)+' Noattributes'
  castprofile = CastProfile.objects.filter(reference='Scholar').first()  
  species = 'urthish'
  onsave_reroll_attributes = True
  pub_date = timezone.now()


class CharacterCheckSkillsFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  castrole = CastRole.objects.filter(value=roll(8)).first()
  full_name = 'Arthur'+str(castrole.value)+' Unskilled'
  castprofile = CastProfile.objects.filter(reference='Physical').first()  
  species = 'urthish'
  onsave_reroll_skills = True
  pub_date = timezone.now()
