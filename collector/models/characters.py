from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import hashlib
import collector.models.skills
from collector.utils import fs_fics7

from collector.utils.basic import write_pdf


class Character(models.Model):
  pagenum = 0
  full_name = models.CharField(max_length=200)
  rid = models.CharField(max_length=200, default='none')
  alliance = models.CharField(max_length=200, blank=True, default='')
  alliancehash = models.CharField(max_length=200, blank=True, default='none')
  player = models.CharField(max_length=200, default='', blank=True)
  species = models.CharField(max_length=200, default='urthish')
  birthdate = models.IntegerField(default=0)
  gender = models.CharField(max_length=30, default='female')
  native_fief = models.CharField(max_length=200, default='none',blank=True)
  caste = models.CharField(max_length=100, default='Freefolk',blank=True)
  rank = models.CharField(max_length=100, default='', blank=True)
  height = models.IntegerField(default=150)
  weight = models.IntegerField(default=50)
  narrative = models.TextField(default='',blank=True)
  entrance = models.CharField(max_length=100,default='',blank=True)
  keyword = models.CharField(max_length=32, blank=True, default='')
  stars = models.CharField(max_length=128, blank=True, default='')
  PA_STR = models.PositiveIntegerField(default=3)
  PA_CON = models.PositiveIntegerField(default=3)
  PA_BOD = models.PositiveIntegerField(default=3)
  PA_MOV = models.PositiveIntegerField(default=3)
  PA_INT = models.PositiveIntegerField(default=3)
  PA_WIL = models.PositiveIntegerField(default=3)
  PA_TEM = models.PositiveIntegerField(default=3)
  PA_PRE = models.PositiveIntegerField(default=3)
  PA_REF = models.PositiveIntegerField(default=3)
  PA_TEC = models.PositiveIntegerField(default=3)
  PA_AGI = models.PositiveIntegerField(default=3)
  PA_AWA = models.PositiveIntegerField(default=3)
  pub_date = models.DateTimeField('Date published', default=datetime.now)
  SA_REC = models.IntegerField(default=0)
  SA_STA = models.IntegerField(default=0)
  SA_END = models.IntegerField(default=0)
  SA_STU = models.IntegerField(default=0)
  SA_RES = models.IntegerField(default=0)
  SA_DMG = models.IntegerField(default=0)
  SA_TOL = models.IntegerField(default=0)
  SA_HUM = models.IntegerField(default=0)
  SA_PAS = models.IntegerField(default=0)
  SA_WYR = models.IntegerField(default=0)
  SA_SPD = models.IntegerField(default=0)
  SA_RUN = models.IntegerField(default=0)
  PA_TOTAL = models.IntegerField(default=0)
  SK_TOTAL = models.IntegerField(default=0)
  TA_TOTAL = models.IntegerField(default=0)
  BC_TOTAL = models.IntegerField(default=0)
  AP = models.IntegerField(default=0)
  OP = models.IntegerField(default=0)
  gm_shortcuts = models.TextField(default='',blank=True)
  age = models.IntegerField(default=0)  
  role = models.CharField(max_length=16,default='00',choices= fs_fics7.ROLECHOICES)
  profile = models.CharField(max_length=16,default='undefined',choices=fs_fics7.PROFILECHOICES)
  occult_level = models.PositiveIntegerField(default=0)
  occult_darkside = models.PositiveIntegerField(default=0)
  occult = models.CharField(max_length=50, default='', blank=True)
  challenge = models.TextField(default='',blank=True)  
  ready_for_export =  models.BooleanField(default=False)

  def fix(self):
    """ Check / calculate other characteristics """
    self.check_exportable()
    # Age completion
    if self.birthdate < 1000:
      self.birthdate = 5017 - self.birthdate
    self.age = 5017 - self.birthdate
    # NPC fix
    if self.player == 'none':
      self.player = ''
    # Calculate SA
    fs_fics7.check_primary_attributes(self)
    fs_fics7.check_secondary_attributes(self)
    fs_fics7.check_root_skills(self)
#    fs_fics7.check_everyman_skills(self, Skill, SkillRef)
    fs_fics7.check_everyman_skills(self)
    gm_shortcuts = ""
    tmp_shortcuts = []
    skills = self.skill_set.all()
    for s in skills:
      sc = fs_fics7.check_gm_shortcuts(self,s)
      if sc != '':
        tmp_shortcuts.append(sc)
    gm_shortcuts = ", ".join(tmp_shortcuts)
    gm_shortcuts += fs_fics7.check_attacks(self)
    if self.player == None:
      gm_shortcuts += fs_fics7.check_nameless_attributes(self)
    self.gm_shortcuts = gm_shortcuts
    self.ready_for_export = self.check_exportable()
  def check_exportable(self):
    """
    Is that avatar finished?
    We check this with the fics rule for extras:
      AP: 60 for player
      SK: 70
      TA: 20
      BC: 10 
    """
    exportable = True
    comment = ''
    self.stars = ""
    for x in range(1,int(self.role)+1):
      self.stars += '<i class="fas fa-star fa-xs"></i>'    
    self.PA_TOTAL = \
      self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + \
      self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + \
      self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA
    self.SK_TOTAL = 0
    self.TA_TOTAL = 0
    self.BC_TOTAL = 0
    skills = self.skill_set.all()
    for s in skills:
      if s.skill_ref.is_root == False:         
        self.SK_TOTAL += s.value
    talents = self.talent_set.all()
    for t in talents:
      self.TA_TOTAL += t.value
    blessingcurses = self.blessingcurse_set.all()
    for bc in blessingcurses:
      self.BC_TOTAL += bc.value
    self.AP = self.PA_TOTAL
    self.OP = self.SK_TOTAL + self.TA_TOTAL + self.BC_TOTAL
    #self.challenge = self.PA_TOTAL*3 + self.SK_TOTAL + self.TA_TOTAL + self.BC_TOTAL
    roleok = fs_fics7.check_role(self)
    if roleok == False:
      exportable = False
    if self.player != '':
      comment += 'Warning: Players avatars are always exportable...\n'
      exportable = True
    if comment != '':
      print(comment)  
    if self.ready_for_export != exportable:
      self.ready_for_export = exportable
      self.rid = 'none'
    return self.ready_for_export
    
  def backup(self):
    """ Transform to PDF if exportable"""
    proceed = self.ready_for_export
    if proceed == True:
      item = self
      context = {'c':item,'filename':'%04d_%s'%(item.pagenum,item.rid),}
      write_pdf('collector/character_pdf.html',context)
    return proceed      

  def __str__(self):
    return '%s' % self.full_name  

  def update_field(self, key, value):
    try:
      v = getattr(self, key)
      val = value[0]
      if type(v)==type(1):
        valfix = int(val)+0        
      elif type(v)==type(False):
        valfix = bool(val)
      else:
        valfix = str(val)
      if valfix != v:
        #print("%s --> %s:%s <> %s:%s"%(key,v,type(v),valfix,type(valfix)))
        setattr(self, key, valfix)
        return key,valfix
      else:
        return False,False
    except AttributeError:
      #print("DP: There is no such attribute %s in this model"%key)
      return False, False   
  # Auto build character
  def autobuild(self):
    if self.role == '00' and self.profile == 'undefined':
      return False
    else:
      return True
@receiver(pre_save, sender=Character, dispatch_uid='update_character')
def update_character(sender, instance, **kwargs):
  if instance.rid != 'none':
    instance.fix()
  #instance.rid = hashlib.sha1(bytes(instance.full_name,'utf-8')).hexdigest()
  instance.rid = fs_fics7.get_rid(instance.full_name)
  instance.alliancehash = hashlib.sha1(bytes(instance.alliance,'utf-8')).hexdigest()
  print("Fix .........: %s" % (instance.full_name))

@receiver(post_save, sender=Character, dispatch_uid='backup_character')
def backup_character(sender, instance, **kwargs):
  if instance.rid != 'none':
    if instance.backup() == True:
      print("PDF .........: %s.pdf" % (instance.rid))





