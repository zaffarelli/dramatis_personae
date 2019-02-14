from django.test import TestCase
from collector.models.characters import Character
from collector.utils.fs_fics7 import check_skills
from collector.tests.factories import CharacterCheckSkillsFactory


class FICSTest(TestCase):
  def test__check_PA_character_creation(self):
    pass

  def test__check_skills_character_build(self):
    c = CharacterCheckSkillsFactory.build()
    self.assertEquals(c.autobuild(),True)
    
  def test__check_skills_character_create(self):
    c = CharacterCheckSkillsFactory.create()
    self.assertEquals(c.rid,'arthur_unskilled')


