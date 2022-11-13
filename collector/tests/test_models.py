"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""

from django.test import TestCase
from collector.models.character import Character
from collector.tests.factories import CharacterFactory, CharacterHistoryFactory


class CharacterTest(TestCase):
    fixtures = ['skill_ref.xml', 'specie.xml']

    def test_character_creation(self):
        c = CharacterFactory.build()
        self.assertTrue(isinstance(c, Character))

    def test_default_rid(self):
        c = CharacterFactory.create()
        c.full_name = 'John Doe'
        c.need_fix = True
        c.save()
        self.assertEquals(c.rid, 'john_doe')

    # def test_rid_after_save(self):
    #     c = CharacterFactory.create()
    #     self.assertEquals(c.rid, 'tastus_fabulus')
    #
    # def test_blank_challenge_value(self):
    #     c = CharacterFactory.create()
    #     self.assertEquals(c.challenge_value, 0)
    #
    # def test_fix_challenge_value(self):
    #     c = CharacterFactory.create()
    #     c.fix()
    #     self.assertEquals(c.challenge_value, 36)
    #
    # def test_fix_challenge_value_history(self):
    #     c = CharacterHistoryFactory.create()
    #     c.fix()
    #     self.assertEquals(c.challenge_value, 0)
