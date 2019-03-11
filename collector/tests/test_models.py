'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.test import TestCase
from collector.models.characters import Character
from collector.tests.factories import CharacterFactory

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
