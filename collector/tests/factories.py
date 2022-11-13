"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""

from collector.models.character import Character
import factory
from django.utils import timezone
from collector.models.specie import Specie


# Basic Character
class CharacterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character

    full_name = 'John Doe'



class CharacterHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character
    full_name = 'Tastus Fabulus'
    use_history_creation = True



class VeteranGuilderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character

    full_name = 'Roman Van Dyke'
    # role = Role.objects.filter(reference='Veteran').first()
    # profile = Profile.objects.filter(reference='Guilder').first()
    specie = Specie.objects.filter(species='Urthish').first()
    pub_date = timezone.now()


class UnbuildableCharacterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character

    full_name = 'Rico Unbuildable'
    # role = Role.objects.get(pk=1)
    # profile = Profile.objects.get(pk=1)
    specie = Specie.objects.filter(species='Urthish').first()
    pub_date = timezone.now()


class CharacterCheckPAFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character

    pub_date = timezone.now()
    # role = Role.objects.filter(reference='Superior').first()
    # profile = Profile.objects.filter(reference='Scholar').first()
    specie = Specie.objects.filter(species='Urthish', race='Teutonic').first()
    full_name = '%s %s' % (specie.species, specie.race)
    onsave_reroll_attributes = True


class CharacterCheckSkillsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Character

    pub_date = timezone.now()
    # role = Role.objects.filter(reference='Seasoned').first()
    # profile = Profile.objects.filter(reference='Military').first()
    specie = Specie.objects.filter(species='Urthish', race='Kaanic').first()
    full_name = '%s %s' % (specie.species, specie.race)
    onsave_reroll_skills = True
