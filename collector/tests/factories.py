'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from collector.models.characters import Character
import factory
import datetime
from django.utils import timezone
from collector.utils.fs_fics7 import roll
from collector.models.fics_models import CastRole, CastProfile, CastEveryman


class CharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Tastus Fabulus'
  pub_date = timezone.now()

class VeteranGuilderFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Roman Van Dyke'
  role = Role.objects.filter(value=5).first()
  profile = Profile.objects.filter(reference='Guilder').first()
  pub_date = timezone.now()

class UnbuildableCharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  full_name = 'Rico Unbuildable'
  role = Role.objects.get(pk=1)
  profile = Profile.objects.get(pk=1)
  pub_date = timezone.now()

class CharacterCheckPAFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  castrole = Role.objects.filter(value=roll(8)).first()
  full_name = 'Scholar'+str(castrole.value)+' Noattributes'
  profile = Profile.objects.filter(reference='Scholar').first()  
  species = Specie.objects.get(pk=1)
  onsave_reroll_attributes = True
  pub_date = timezone.now()


class CharacterCheckSkillsFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character
  castrole = CastRole.objects.filter(value=roll(8)).first()
  full_name = 'Arthur'+str(castrole.value)+' Unskilled'
  castprofile = CastProfile.objects.filter(reference='Military').first()  
  castspecies = CastEveryman.objects.get(pk=1)
  onsave_reroll_skills = True
  pub_date = timezone.now()
