"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.test import TestCase
#from cartograph.models.character import Character
#from cartograph.utils.fs_fics7 import check_primary_attributes
from collector.tests.factories import CharacterCheckSkillsFactory, CharacterCheckPAFactory

class FICSTestSkills(TestCase):
  fixtures = ['skill_ref.xml', 'specie.xml']

  # def test_check_skills_character_build(self):
  #   c = CharacterCheckSkillsFactory.build()
  #   self.assertEquals(c.autobuild(),True)
  #
  # def test_check_skills_character_create(self):
  #   c = CharacterCheckSkillsFactory.create()
  #   self.assertEquals(c.rid, 'seasoned_military_urthish_kaanic')


class FICSTestPA(TestCase):
  fixtures = ['skill_ref.xml', 'species.xml' ]

  # def test_check_PA_character_creation(self):
  #   c = CharacterCheckPAFactory.create()
  #   self.assertEquals(c.rid,'superior_scholar_urthish_teutonic')


  # def test_check_PA_Total(self):
  #   # Total PA matching
  #   c = CharacterCheckPAFactory.create()
  #   total_pa = c.role.primaries
  #   check_primary_attributes(c)
  #   c_phy = c.PA_STR + c.PA_CON + c.PA_BOD + c.PA_MOV
  #   c_spi = c.PA_INT + c.PA_WIL + c.PA_TEM + c.PA_PRE
  #   c_com = c.PA_TEC + c.PA_REF + c.PA_AGI + c.PA_AWA
  #   c_tot = c_phy + c_spi + c_com
  #   self.assertEquals(c_tot,total_pa)

  # def test_check_PA_Global_Weights(self):
  #   # Check global weights directive
  #   c = CharacterCheckPAFactory.create()
  #   check_primary_attributes(c)
  #   c_pa_list = [ c.PA_STR , c.PA_CON , c.PA_BOD , c.PA_MOV , c.PA_INT , c.PA_WIL , c.PA_TEM , c.PA_PRE , c.PA_TEC , c.PA_REF , c.PA_AGI , c.PA_AWA]
  #   weights = c.profile.get_weights()
  #   w_phy = weights[0:4]
  #   w_spi = weights[4:8]
  #   w_com = weights[8:12]
  #   c_phy = c_pa_list[0:4]
  #   c_spi = c_pa_list[4:8]
  #   c_com = c_pa_list[8:12]
  #   wt_phy = sum(w_phy)
  #   wt_spi = sum(w_spi)
  #   wt_com = sum(w_com)
  #   ct_phy = sum(c_phy)
  #   ct_spi = sum(c_spi)
  #   ct_com = sum(c_com)
  #   if (wt_phy + wt_spi) > wt_com:
  #     self.assertGreater(ct_phy + ct_spi,ct_com)
  #   if (wt_phy + wt_com) > wt_spi:
  #     self.assertGreater(ct_phy + ct_com, ct_phy)
  #   if (wt_com + wt_spi) > wt_phy:
  #     self.assertGreater(ct_com + ct_spi, ct_phy)
  #
  # def test_check_PA_Max_Value(self):
  #   # Max value must be preserved
  #   c = CharacterCheckPAFactory.create()
  #   maxi = c.role.maxi
  #   check_primary_attributes(c)
  #   c_pa_list = [ c.PA_STR , c.PA_CON , c.PA_BOD , c.PA_MOV , c.PA_INT , c.PA_WIL , c.PA_TEM , c.PA_PRE , c.PA_TEC , c.PA_REF , c.PA_AGI , c.PA_AWA]
  #   m = max(c_pa_list)
  #   self.assertGreaterEqual(maxi,m)
  #
  # def test_check_PA_Min_Value(self):
  #   # Max value must be preserved
  #   c = CharacterCheckPAFactory.create()
  #   mini = c.role.mini
  #   check_primary_attributes(c)
  #   c_pa_list = [ c.PA_STR , c.PA_CON , c.PA_BOD , c.PA_MOV , c.PA_INT , c.PA_WIL , c.PA_TEM , c.PA_PRE , c.PA_TEC , c.PA_REF , c.PA_AGI , c.PA_AWA]
  #   m = min(c_pa_list)
  #   self.assertLessEqual(mini,m)
