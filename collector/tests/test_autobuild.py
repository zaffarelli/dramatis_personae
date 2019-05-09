'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.test import TestCase
from collector.models.characters import Character
from collector.tests.factories import UnbuildableCharacterFactory, VeteranGuilderFactory

class AutobuildTest(TestCase):
  fixtures = ['skillrefs.xml','species.xml','roles.xml','profiles.xml']
  
  def test_autobuild_character_creation(self):
    c = VeteranGuilderFactory.build()
    self.assertEquals(c.autobuild(),True)

  def test_unbuildable_character_creation(self):
    c = UnbuildableCharacterFactory.build()
    self.assertEquals(c.autobuild(),True)



