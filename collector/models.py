from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
import hashlib
import math
from collector import fs_fics7



###### Characters
class Character(models.Model):  
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
  gm_shortcuts = models.TextField(default='',blank=True)
  age = models.IntegerField(default=0)
  occult_level = models.PositiveIntegerField(default=0)
  occult_darkside = models.PositiveIntegerField(default=0)
  occult = models.CharField(max_length=50, default='', blank=True)
  challenge = models.TextField(default='',blank=True)  
  ready_for_export =  models.BooleanField(default=False)
  def fix(self):
    # Rules revision 166    
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
#    if not self.skill_set.count == 0:
#      skills = self.skill_set.order_by("-value","skill_ref__reference")
#      prev = None
#      for s in skills:
#        if prev is None:
#          prev = s
#          print("%s"%prev.skill_ref.reference)
#        cur = s
#        print("%s %s"%(cur,prev))
#        if cur.skill_ref == prev.skill_ref:
#          cur.delete()
#          this_skill = Skill.objects.filter(id=s.id).delete()
#        else:
#          prev = cur
    skills = self.skill_set.all()
    # Everyman
    print("%s is a(n) %s"%(self.full_name,self.species))
    for every in fs_fics7.EVERYMAN[self.species]:
      every_found = False
      for s in skills:
        if s.skill_ref.reference == every:
          every_found = True
          if s.value < 2:          
            print("Value fixed for %s"%s.skill_ref.reference)
            this_skill = Skill.objects.get(id=s.id)
            this_skill.value = 2
            this_skill.save()
          break
      if not every_found:
        print("Not found: %s... Added!"%every)
        this_skill_ref = SkillRef.objects.get(reference=every)
        this_skill = Skill()
        this_skill.character=self
        this_skill.skill_ref=this_skill_ref
        this_skill.value = 2
        this_skill.save()
    skills = self.skill_set.all()
    gm_shortcuts = ""
    for s in skills:
      if s.skill_ref.is_root == False:
         gm_shortcuts += fs_fics7.check_gm_shortcuts(self,s)
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
    self.ready_for_export = False
    self.gm_shortcuts = gm_shortcuts
    if self.player != '':
      self.ready_for_export = True
    if self.SK_TOTAL >= self.PA_TOTAL:
      self.ready_for_export = True
  def __str__(self):
    return '%s' % self.full_name  

@receiver(pre_save, sender=Character, dispatch_uid="update_character")
def update_character(sender, instance, **kwargs):
  if instance.rid != 'none':
    instance.fix()
  instance.rid = hashlib.sha1(bytes(instance.full_name,'utf-8')).hexdigest()
  instance.alliancehash = hashlib.sha1(bytes(instance.alliance,'utf-8')).hexdigest()
  print("%s --> %s" % (instance.full_name,instance.rid))

###### Weapons
class WeaponRef(models.Model):
  reference = models.CharField(max_length=64,default='',blank=True, unique=True)
  category = models.CharField(max_length=5,choices=(('MELEE',"Melee weapon"),('P',"Pistol/revolver"),('RIF',"Rifle"),('SMG',"Submachinegun"),('SHG',"Shotgun"),('HVY',"Heavy weapon"),('EX',"Exotic weapon")),default='RIF',blank=True)
  weapon_accuracy = models.IntegerField(default=0,blank=True)
  conceilable = models.CharField(max_length=1,choices=(('P',"Pocket"),('J',"Jacket"),('L',"Long coat"),('N',"Can't be hidden")),default='J',blank=True)
  availability = models.CharField(max_length=1,choices=(('E',"Excellent"),('C',"Common"),('P',"Poor"),('R',"Rare")),default='C',blank=True)
  damage_class = models.CharField(max_length=16,default='',blank=True)
  caliber = models.CharField(max_length=16,default='',blank=True)
  str_min = models.PositiveIntegerField(default=0,blank=True)
  rof = models.PositiveIntegerField(default=0,blank=True)
  clip = models.PositiveIntegerField(default=0,blank=True)
  rng = models.PositiveIntegerField(default=0,blank=True)
  rel = models.CharField(max_length=2,choices=(('VR',"Very reliable"),('ST',"Standard"),('UR',"Unreliable")),default='ST',blank=True)
  cost = models.PositiveIntegerField(default=0,blank=True)
  description = models.TextField(max_length=256,default='',blank=True)
  def __str__(self):
    return '%s (%s/%s/%s/%s£)' % (self.reference, self.category, self.damage_class, self.caliber, self.cost)

class Weapon(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  weapon_ref = models.ForeignKey(WeaponRef, on_delete=models.CASCADE)
  ammoes = models.PositiveIntegerField(default=0,blank=True)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.weapon_ref.reference)

class WeaponRefAdmin(admin.ModelAdmin):
  ordering = ('category','reference',)  

class WeaponAdmin(admin.ModelAdmin):
  ordering = ('character','weapon_ref',)

class WeaponInline(admin.TabularInline):
  model = Weapon


###### Armors
class ArmorRef(models.Model):
  reference = models.CharField(max_length=64,default='',blank=True, unique=True)
  category = models.CharField(max_length=6,choices=(('Soft',"Soft Armor"),('Medium',"Medium Armor"),('Hard',"Hard Armor")),default='Soft',blank=True)
  head = models.BooleanField(default=False)
  torso = models.BooleanField(default=True)
  left_arm = models.BooleanField(default=True)
  right_arm = models.BooleanField(default=True)
  left_leg = models.BooleanField(default=False)
  right_leg = models.BooleanField(default=False)
  stopping_power = models.PositiveIntegerField(default=2, blank=True)
  cost = models.PositiveIntegerField(default=2, blank=True)
  encumbrance = models.PositiveIntegerField(default=0, blank=True)
  description = models.TextField(max_length=128,default='', blank=True)
  def __str__(self):
    return '%s (%s, SP:%s)' % (self.reference, self.category, self.stopping_power)

class Armor(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.armor_ref.reference)

class ArmorRefAdmin(admin.ModelAdmin):
  ordering = ('category','-stopping_power','reference')  

class ArmorAdmin(admin.ModelAdmin):
  ordering = ('character','armor_ref',)

class ArmorInline(admin.TabularInline):
  model = Armor

###### Energy Shield
class ShieldRef(models.Model):
  reference = models.CharField(max_length=16,default='',blank=True, unique=True)
  protection_min = models.PositiveIntegerField(default=10,blank=True)
  protection_max = models.PositiveIntegerField(default=20,blank=True)
  hits = models.PositiveIntegerField(default=10,blank=True)
  cost = models.PositiveIntegerField(default=500,blank=True)
  is_compatible_with_medium_armor = models.BooleanField(default=False)
  is_compatible_with_hard_armor = models.BooleanField(default=False)
  description = models.TextField(max_length=128,default='', blank=True)
  def __str__(self):
    return '%s' % (self.reference)

class Shield(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  shield_ref = models.ForeignKey(ShieldRef, on_delete=models.CASCADE)
  charges = models.PositiveIntegerField(default=10, blank=True)
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.shield_ref.reference)

class ShieldRefAdmin(admin.ModelAdmin):
  ordering = ('reference',)  

class ShieldAdmin(admin.ModelAdmin):
  ordering = ('character','shield_ref',)

class ShieldInline(admin.TabularInline):
  model = Shield



###### Skills
class SkillRef(models.Model):
  reference = models.CharField(max_length=200, unique=True)
  is_root = models.BooleanField(default=False)
  is_speciality = models.BooleanField(default=False)
  linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
  ordering = ('reference',)
  def __str__(self):
    return '%s %s %s' % (self.reference,"(R)" if self.is_root else "","(S)" if self.is_speciality else "")

class Skill(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
  value = models.PositiveIntegerField(default=0)
  #ordo = models.CharField(max_length=200, blank=True)
  ordering = ('skill_ref.reference')  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.skill_ref.reference)
  def fix(self):
    pass
@receiver(pre_save, sender=Skill, dispatch_uid="update_skill")
def update_skill(sender, instance, **kwargs):
  instance.fix()

class SkillInline(admin.TabularInline):
  model = Skill
  extras = 10
  ordering = ('skill_ref',)
  #exclude = ('ordo',)

class SkillRefAdmin(admin.ModelAdmin):
  ordering = ('reference',)
  #exclude = ('linked_to',)

class SkillAdmin(admin.ModelAdmin):
  ordering = ('character','skill_ref',)


###### Blessings/Curses
class BlessingCurse(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  name = models.CharField(max_length=64,default='',blank=True)
  description = models.TextField(max_length=128,default='',blank=True)
  value = models.IntegerField(default=0)  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.name)

class BlessingCurseInline(admin.TabularInline):
  model = BlessingCurse

###### Talents
class Talent(models.Model):
  character = models.ForeignKey(Character, on_delete=models.CASCADE)
  name = models.CharField(max_length=64,default='',blank=True)
  description = models.TextField(max_length=512,default='',blank=True)
  value = models.IntegerField(default=0)  
  def __str__(self):
    return '%s=%s' % (self.character.full_name,self.name)

class TalentInline(admin.TabularInline):
  model = Talent

###### Character Admin
class CharacterAdmin(admin.ModelAdmin):
  inlines = [
    SkillInline,
    BlessingCurseInline,
    TalentInline,
    WeaponInline,
    ArmorInline
  ]  
  ordering = ('full_name',)


