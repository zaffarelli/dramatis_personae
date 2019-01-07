from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import hashlib
import collector.models.skills
from scenarist.models.epics import Epic
from scenarist.models.dramas import Drama
from scenarist.models.acts import Act
from collector.utils import fs_fics7, fics_references
from collector.utils.basic import debug_print
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
  stars = models.CharField(max_length=256, blank=True, default='')
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
  BA_TOTAL = models.IntegerField(default=0)
  weapon_cost = models.IntegerField(default=0)
  armor_cost = models.IntegerField(default=0)
  shield_cost = models.IntegerField(default=0)
  AP = models.IntegerField(default=0)
  OP = models.IntegerField(default=0)
  gm_shortcuts = models.TextField(default='',blank=True)
  age = models.IntegerField(default=0)  
  role = models.CharField(max_length=16,default='00',choices= fics_references.ROLECHOICES)
  profile = models.CharField(max_length=16,default='undefined',choices=fics_references.PROFILECHOICES)
  occult_level = models.PositiveIntegerField(default=0)
  occult_darkside = models.PositiveIntegerField(default=0)
  occult = models.CharField(max_length=50, default='', blank=True)
  challenge = models.TextField(default='',blank=True)  
  ready_for_export =  models.BooleanField(default=False)
  epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
  drama = models.ForeignKey(Drama, null=True, blank=True, on_delete=models.SET_NULL)
  act = models.ForeignKey(Act, null=True, blank=True, on_delete=models.SET_NULL)

  def fix(self,conf=None):
    """ Check / calculate other characteristics """
    self.check_exportable()
    # Age completion
    if conf == None:
      if self.birthdate < 1000:
        self.birthdate = 5017 - self.birthdate
      self.age = 5017 - self.birthdate
    else:
      if self.birthdate < 1000:
        self.birthdate = conf.epic.era - self.birthdate
      self.age = conf.epic.era - self.birthdate      
    # NPC fix
    if self.player == 'none':
      self.player = ''
    # Calculate SA
    fs_fics7.check_primary_attributes(self)
    fs_fics7.check_secondary_attributes(self)
    fs_fics7.check_root_skills(self)
#    fs_fics7.check_everyman_skills(self, Skill, SkillRef)
    fs_fics7.check_everyman_skills(self)
    fs_fics7.check_skills(self)
    gm_shortcuts = ''
    tmp_shortcuts = []
    skills = self.skill_set.all()
    for s in skills:
      sc = fs_fics7.check_gm_shortcuts(self,s)
      if sc != '':
        tmp_shortcuts.append(sc)
    gm_shortcuts = '<br/>'.join(tmp_shortcuts)
    gm_shortcuts += fs_fics7.check_attacks(self)
    if self.player == None:
      gm_shortcuts += fs_fics7.check_nameless_attributes(self)
    self.gm_shortcuts = gm_shortcuts
    self.ready_for_export = self.check_exportable()


  def add_or_update_skill(self,askill,modifier=0):
    """
        Modifier <> 0:
        - Adding a skill at <modifier> value,
        - Updating a skill value to <modifier> value
        <modifier> is 0
        - Increment by 1
    """ 
    from collector.models.skills import Skill    
    found_skill = self.skill_set.all().filter(skill_ref=askill).first()
    if found_skill != None:
      if modifier == 0:
        found_skill.value += 1
      else:
        found_skill.value = modifier
      found_skill.save()
      debug_print('> New value for %s is %d'%(found_skill.skill_ref.reference,found_skill.value))
      debug_print('updated')
      return found_skill
    else:
      skill = Skill()
      skill.character = self
      skill.skill_ref = askill
      if modifier == 0:
        skill.value = 1
      else:
        skill.value = modifier
      skill.save()
      debug_print('> New value for %s is %d'%(skill.skill_ref.reference,skill.value))
      debug_print('added')
      return skill

  def add_missing_root_skills(self):
    """ According to the character specialities, fixing the root skills """
    from collector.models.skills import Skill
    from collector.models.skillrefs import SkillRef
    roots_list = []
    for skill in self.skill_set.all():
      if skill.skill_ref.is_speciality:
        roots_list.append(skill.skill_ref.linked_to)
    for skill in self.skill_set.all():
      if skill.skill_ref.is_root:
        skill.delete()
    print(roots_list)
    for skillref in SkillRef.objects.all():
      if skillref in roots_list:
        self.add_or_update_skill(skillref, roots_list.count(skillref))

  def purgeSkills(self):
    """ Deleting all character skills """
    for skill in self.skill_set.all():
      skill.delete()
    print(self.skill_set.all().count())

    
  def resetTotal(self):
    """ Compute all sums for all stats """
    notes = []
    self.SK_TOTAL = 0
    self.TA_TOTAL = 0
    self.BC_TOTAL = 0
    self.BA_TOTAL = 0
    self.weapon_cost = 0
    self.armor_cost = 0
    self.shield_cost = 0
    self.PA_TOTAL = \
      self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + \
      self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + \
      self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA
    notes.append('PA_TOTAL: %d'%(self.PA_TOTAL))
    # skills
    skills = self.skill_set.all()
    for s in skills:
      if s.skill_ref.is_root == False:         
        self.SK_TOTAL += s.value
    notes.append('SK_TOTAL: %d'%(self.SK_TOTAL))
    # talents
    talents = self.talent_set.all()
    for t in talents:
      self.TA_TOTAL += t.value
    notes.append('TA_TOTAL: %d'%(self.TA_TOTAL))
    # blessings curses
    blessingcurses = self.blessingcurse_set.all()
    for bc in blessingcurses:
      self.BC_TOTAL += bc.value
    notes.append('BC_TOTAL: %d'%(self.BC_TOTAL))
    # benefice afflictions
    beneficeafflictions = self.beneficeaffliction_set.all()    
    for ba in beneficeafflictions:
      self.BA_TOTAL += ba.value + ba.beneficeaffliction_ref.value
    notes.append('BA_TOTAL: %d'%(self.BA_TOTAL))
    # AP    
    self.AP = self.PA_TOTAL
    # Extras as OP
    self.OP = self.PA_TOTAL*3 + self.SK_TOTAL + self.TA_TOTAL + self.BC_TOTAL + self.BA_TOTAL
    # Weapons firebirds
    weapons = self.weapon_set.all()    
    for w in weapons:
      self.weapon_cost += w.weapon_ref.cost
    notes.append('weapon_cost: %d'%(self.weapon_cost))
    # Armors firebirds
    armors = self.armor_set.all()    
    for a in armors:
      self.armor_cost += a.armor_ref.cost
    notes.append('armor_cost: %d'%(self.armor_cost))
    # Shields firebirds
    shields = self.shield_set.all()    
    for s in shields:
      self.shield_cost += s.shield_ref.cost
    notes.append('shield_cost: %d'%(self.shield_cost))
    return ' / '.join(notes)


  def check_exportable(self,conf=None):
    """ Is that avatar finished according to the role and profile? """
    exportable = True
    comment = ''
    self.stars = ''
    for x in range(1,int(self.role)+1):
      self.stars += '<i class="fas fa-star fa-xs"></i>'    
    comment += self.resetTotal()
    roleok = fs_fics7.check_role(self)
    self.challenge = fs_fics7.update_challenge(self)
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
      print('PDF .........: %s.pdf' % (self.rid))
    return proceed      

  def __str__(self):
    return '%s' % self.full_name  

  def update_field(self, key, value):
    """ Field individual validation during sanitize """
    try:
      v = getattr(self, key)
      val = value[0]
      valfix = val
      field_type = self._meta.get_field(str(key)).get_internal_type()
      if field_type == 'ForeignKey':
        related_model = str(self._meta.get_field(str(key)).related_model)
        #print("FOREIGNKEY SITUATION (%s)"%(related_model))
        if related_model == "<class 'scenarist.models.epics.Epic'>":        
          valfix = Epic(pk=val)
          #print("Foreign key is an Epic")
        elif related_model == "<class 'scenarist.models.dramas.Drama'>":
          valfix = Drama(pk=val)
          #print("Foreign key is a Drama")
        elif related_model == "<class 'scenarist.models.acts.Act'>":
          valfix = Act(pk=val)
          #print("Foreign key is an Act")
        else:
          pass
          #print("Foreign key link not found: %s"%(related_model))
      else:
        if type(v)==type(1):
          valfix = int(val)+0        
        elif type(v)==type(False):
          valfix = bool(val)
        else:
          valfix = str(val)
      debug_print(valfix)
      if valfix != v:
        #print("%s --> %s:%s <> %s:%s"%(key,v,type(v),valfix,type(valfix)))
        #print("%s"%(type(self.key)))
        setattr(self, key, valfix)
        return key,valfix
      else:
        return False,False
    except AttributeError:
      #print("DP: There is no such attribute %s in this model"%(key))
      return False, False   

  def sanitize(self,f):
    sane_f = {}
    for key, value in f.items():
      rkey,rvalue = self.update_field(key, value)
      if rkey != False:
        sane_f[rkey] = rvalue
    return sane_f

  def get_rid(self,s):
    x = s.replace(' ','_').replace("'",'').replace('é','e').replace('è','e').replace('ë','e').replace('â','a').replace('ô','o').replace('"','').replace('ï','i').replace('à','a').replace('-','')
    self.rid = x.lower()

  # Auto build character
  def autobuild(self):
    if self.role == '00' and self.profile == 'undefined':
      return False
    else:
      return True

      
@receiver(pre_save, sender=Character, dispatch_uid='update_character')
def update_character(sender, instance, conf=None, **kwargs):
  """ Before saving, fix() and  get_RID() for the character """
  if instance.rid != 'none':
    instance.fix(conf)
  instance.get_rid(instance.full_name)
  instance.alliancehash = hashlib.sha1(bytes(instance.alliance,'utf-8')).hexdigest()
  print('Fix .........: %s' % (instance.full_name))

@receiver(post_save, sender=Character, dispatch_uid='backup_character')
def backup_character(sender, instance, **kwargs):
  """ After saving, create PDF for the character """
  if instance.rid != 'none':
    instance.backup()
      





