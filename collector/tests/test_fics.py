'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.test import TestCase
from collector.models.characters import Character
from collector.utils.fics_references import EVERYMAN
from collector.utils.fs_fics7 import check_skills, check_primary_attributes
from collector.tests.factories import CharacterCheckSkillsFactory, CharacterCheckPAFactory

class FICSTestSkills(TestCase):
  fixtures = ['skillrefs.xml']

  def test_check_skills_character_build(self):
    c = CharacterCheckSkillsFactory.build()
    self.assertEquals(c.autobuild(),True)
    
  def test_check_skills_character_create(self):
    c = CharacterCheckSkillsFactory.create()
    self.assertEquals(c.rid,'arthur'+str(c.castrole.value)+'_unskilled')

  def test_check_skills_Total(self):
    """ Check skills total according to role """
    c = CharacterCheckSkillsFactory.create()
    sk_pool = c.castrole.skills
    check_skills(c)
    skill_total = 0
    for s in c.skill_set.all():
      if (s.skill_ref.is_root == False):
        skill_total += s.value
    self.assertEqual(skill_total,sk_pool)

class FICSTestPA(TestCase):
  def test_check_PA_character_creation(self):
    c = CharacterCheckPAFactory.create()
    self.assertEquals(c.rid,'scholar'+str(c.castrole.value)+'_noattributes')
       

  def test_check_PA_Total(self):
    """ Total PA matching """
    c = CharacterCheckPAFactory.create()
    total_pa = c.castrole.primaries
    check_primary_attributes(c)
    c_phy = c.PA_STR + c.PA_CON + c.PA_BOD + c.PA_MOV 
    c_spi = c.PA_INT + c.PA_WIL + c.PA_TEM + c.PA_PRE 
    c_com = c.PA_TEC + c.PA_REF + c.PA_AGI + c.PA_AWA
    c_tot = c_phy + c_spi + c_com
    self.assertEquals(c_tot,total_pa)

  def test_check_PA_Global_Weights(self):
    """ Check global weights directive """
    c = CharacterCheckPAFactory.create()
    check_primary_attributes(c)
    c_pa_list = [ c.PA_STR , c.PA_CON , c.PA_BOD , c.PA_MOV , c.PA_INT , c.PA_WIL , c.PA_TEM , c.PA_PRE , c.PA_TEC , c.PA_REF , c.PA_AGI , c.PA_AWA]
    weights = c.castprofile.get_weights()
    w_phy = weights[0:4]
    w_spi = weights[4:8]
    w_com = weights[8:12]
    c_phy = c_pa_list[0:4]
    c_spi = c_pa_list[4:8]
    c_com = c_pa_list[8:12] 
    wt_phy = sum(w_phy)
    wt_spi = sum(w_spi)
    wt_com = sum(w_com)
    ct_phy = sum(c_phy)
    ct_spi = sum(c_spi)
    ct_com = sum(c_com)    
    if (wt_phy + wt_spi) > wt_com:
      self.assertGreater(ct_phy + ct_spi,ct_com)
    if (wt_phy + wt_com) > wt_spi:
      self.assertGreater(ct_phy + ct_com, ct_phy)
    if (wt_com + wt_spi) > wt_phy:
      self.assertGreater(ct_com + ct_spi, ct_phy)

  def test_check_PA_Max_Value(self):
    """ Max value must be preserved """
    c = CharacterCheckPAFactory.create()
    maxi = c.castrole.maxi
    check_primary_attributes(c)
    c_pa_list = [ c.PA_STR , c.PA_CON , c.PA_BOD , c.PA_MOV , c.PA_INT , c.PA_WIL , c.PA_TEM , c.PA_PRE , c.PA_TEC , c.PA_REF , c.PA_AGI , c.PA_AWA]
    m = max(c_pa_list)
    self.assertGreaterEqual(maxi,m)

  def test_check_PA_Min_Value(self):
    """ Max value must be preserved """
    c = CharacterCheckPAFactory.create()
    mini = c.castrole.mini
    check_primary_attributes(c)
    c_pa_list = [ c.PA_STR , c.PA_CON , c.PA_BOD , c.PA_MOV , c.PA_INT , c.PA_WIL , c.PA_TEM , c.PA_PRE , c.PA_TEC , c.PA_REF , c.PA_AGI , c.PA_AWA]
    m = min(c_pa_list)
    self.assertLessEqual(mini,m)

