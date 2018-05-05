from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
import hashlib
import math

class Character(models.Model):
  full_name = models.CharField(max_length=200)
  rid = models.CharField(max_length=200, default='')
  alliance = models.CharField(max_length=200, default='none')
  player = models.CharField(max_length=200, default='', blank=True)
  species = models.CharField(max_length=200, default='urthish')
  birthdate = models.IntegerField(default=0)
  gender = models.CharField(max_length=30, default='male')
  native_fief = models.CharField(max_length=200, default='none',blank=True)
  caste = models.CharField(max_length=100, default='Freefolk',blank=True)
  rank = models.CharField(max_length=100, default='none', blank=True)
  height = models.IntegerField(default=150)
  weight = models.IntegerField(default=50)
  narrative = models.TextField(default='',blank=True)
  entrance = models.CharField(max_length=100,default='',blank=True)
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
  age = models.IntegerField(default=0)
  occult_level = models.PositiveIntegerField(default=0)
  occult_darkside = models.PositiveIntegerField(default=0)
  occult = models.CharField(max_length=50, default='', blank=True)
  challenge = models.TextField(default='',blank=True)

  def fix(self):
    # Rules revision 166
    self.rid = hashlib.sha1(bytes(self.full_name,'utf-8')).hexdigest()
    self.SA_REC = self.PA_STR + self.PA_CON
    self.SA_STA = math.ceil(self.PA_BOD / 2) - 1
    self.SA_END = (self.PA_BOD + self.PA_STR) * 5
    self.SA_STU = self.PA_CON + self.PA_BOD
    self.SA_RES = self.PA_WIL + self.PA_PRE
    self.SA_DMG = math.ceil(self.PA_STR / 2) - 2
    self.SA_TOL = self.PA_TEM + self.PA_WIL
    self.SA_HUM = (self.PA_TEM + self.PA_WIL) * 5
    self.SA_PAS = self.PA_TEM + self.PA_AWA
    self.SA_WYR = self.PA_INT + self.PA_REF
    self.SA_SPD = math.ceil(self.PA_REF / 2)
    self.SA_RUN = self.PA_MOV *2
    # Primary attributes total
    self.PA_TOTAL = \
      self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + \
      self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + \
      self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA
    # Age completion
    if self.birthdate < 1000:
      self.birthdate = 5017 - self.birthdate
    self.age = 5017 - self.birthdate

    if self.player == 'none':
      self.player = ''

    # Skills total
    self.SK_TOTAL = 0
    skills = self.skill_set.all()
    for s in skills:
      if s.skill_ref.is_root == False:
        self.SK_TOTAL += s.value
    # With talents
    self.TA_TOTAL = 0
    talents = self.talent_set.all()
    for t in talents:
      self.TA_TOTAL += t.value
    # With blessingcurses
    self.BC_TOTAL = 0
    blessingcurses = self.blessingcurse_set.all()
    for bc in blessingcurses:
      self.BC_TOTAL += bc.value

    self.challenge = self.PA_TOTAL*3 + self.SK_TOTAL + self.TA_TOTAL + self.BC_TOTAL
      
  def __str__(self):
    return '%s' % self.full_name



@receiver(pre_save, sender=Character, dispatch_uid="update_character")
def update_character(sender, instance, **kwargs):
  instance.fix()
  print("%s --> %s" % (instance.full_name,instance.rid))


class SkillRef(models.Model):
  reference = models.CharField(max_length=200)
  is_root = models.BooleanField(default=False)
  is_speciality = models.BooleanField(default=False)
  linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
  ordering = ('reference',)
  def __str__(self):
    return '%s %s %s' % (self.reference,"(R)" if self.is_root else "","(S)" if self.is_speciality else "")

class BlessingCurse(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  name = models.CharField(max_length=64,default='',blank=True)
  description = models.TextField(max_length=128,default='',blank=True)
  value = models.IntegerField(default=0)  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.name)

class Talent(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  name = models.CharField(max_length=64,default='',blank=True)
  description = models.TextField(max_length=512,default='',blank=True)
  value = models.IntegerField(default=0)  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.name)
      
class Skill(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
  value = models.PositiveIntegerField(default=0)
  ordo = models.CharField(max_length=200, blank=True)
  ordering = ('skill_ref.reference')  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.skill_ref.reference)
  def fix(self):
    self.ordo = self.skill_ref.reference

 

@receiver(pre_save, sender=Skill, dispatch_uid="update_skill")
def update_skill(sender, instance, **kwargs):
  instance.fix()


class SkillInline(admin.TabularInline):
  model = Skill
  extras = 10
  ordering = ('ordo',)
  exclude = ('ordo',)

class BlessingCurseInline(admin.TabularInline):
  model = BlessingCurse

class TalentInline(admin.TabularInline):
  model = Talent

class SkillRefAdmin(admin.ModelAdmin):
  ordering = ('reference',)
  #exclude = ('linked_to',)

class SkillAdmin(admin.ModelAdmin):
  ordering = ('character','skill_ref',)


class CharacterAdmin(admin.ModelAdmin):
  inlines = [
    SkillInline,
    BlessingCurseInline,
    TalentInline
  ]  
  ordering = ('full_name',)


