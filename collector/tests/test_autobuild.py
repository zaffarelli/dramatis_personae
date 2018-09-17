from django.test import TestCase
from collector.models import Character
from collector.tests.factories import AutobuildCharacterFactory


class AutobuildTest(TestCase):
  def test_autobuild_character_creation(self):
    c = AutobuildCharacterFactory.build()
    self.assertTrue(isinstance(c,Character))




