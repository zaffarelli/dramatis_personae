'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.test import TestCase
from collector.models.character import Character
from collector.tests.factories import UnbuildableCharacterFactory, VeteranGuilderFactory

class AutobuildTest(TestCase):
  fixtures = ['skill_ref.xml','specie.xml']

  def test_autobuild_character_creation(self):
    c = VeteranGuilderFactory.build()
    self.assertEquals(c.autobuild(),True)

  def test_unbuildable_character_creation(self):
    c = UnbuildableCharacterFactory.build()
    self.assertEquals(c.autobuild(),True)
