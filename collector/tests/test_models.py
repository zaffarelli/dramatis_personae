from unittest import TestCase
from collector.models import Character

class CharacterTest(TestCase):

  def test_character_creation(self):
    c = Character("Testus Fabulous")
    self.assertTrue(isinstance(c,Character))
