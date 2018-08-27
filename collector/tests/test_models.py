from django.test import TestCase
from collector.models import Character
import factory
import datetime

class CharacterFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Character

  full_name = 'Tastus Fabulus'
  pub_date = datetime.datetime.now()

class CharacterTest(TestCase):
  def test_character_creation(self):
    c = CharacterFactory.build()
    self.assertTrue(isinstance(c,Character))

  def test_default_rid(self):
    c = CharacterFactory.build()
    self.assertEquals(c.rid,'none')

  def test_rid_after_save(self):
    c = CharacterFactory.create()    
    self.assertEquals(c.rid,'tastus_fabulus')
