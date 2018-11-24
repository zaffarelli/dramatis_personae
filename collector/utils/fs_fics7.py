# Fading Suns
# Fusion Interlock Custom System v7
# This file contains the core business function of the app
import math
from random import randint
import os

from collector.models.skillrefs import SkillRef


MAX_CHAR = 10
RELEASE = 0.6

'''
  (from Fading Suns CoreRulebook p91-92)
  Base AP..................: 60 AP -> 180 OP
  Base Skill OP............: 30 OP
  Everyman Skill OP .......: 20 OP
  Blessing/Curses..........: 10 OP
  Extra OP.................: 40 OP
  TOTAL ...................: 280 OP

'''

#choices=(('standard',"Standard"),('villain',"Villain"),('player',"Player"),('henchman',"Henchman"),('boss',"Boss"),('support',"Support"),('auto',"Autochton"))

ROLECHOICES = (
  ('08','Legend'),
  ('07','Champion'),
  ('06','Elite'),
  ('05','Veteran'),
  ('04','Seasoned'),
  ('03','Superior'),
  ('02','Standard'),
  ('01','Inferior'),
  ('00','Undefined'),
)

PROFILECHOICES = (
  ('tech',"Tech"),
  ('physical',"Physical"),
  ('spiritual',"Spiritual"),
  ('standard',"Standard"),
  ('courtisan',"Courtisan"),
  ('scholar',"Scholar"),
  ('guilder',"Guilder"),
  ('undefined','Undefined'),
)

PROFILES = {
  'physical': {
    'weights':[2,2,2,2,1,1,1,1,1,1,1,1],
  },
  'spiritual': {
    'weights':[1,1,1,1,2,2,2,2,1,1,1,1],
  },
  'tech': {
    'weights':[1,1,1,1,1,1,1,1,2,2,2,2],
  },  
  'courtisan': {
    'weights':[2,2,2,2,2,2,2,2,1,1,1,1],
  },
  'scholar': {
    'weights':[1,1,1,1,2,2,2,2,2,2,2,2],
  },
  'guilder': {
    'weights':[2,2,2,2,1,1,1,1,2,2,2,2],
  },    
  'standard': {
    'weights':[1,1,1,1,1,1,1,1,1,1,1,1],
  },    
}


ROLES = {
  '08': {
    'primaries': 90,
    'maxi': 11,
    'skills':110,
    'talents':40,
    'bc':20,
  },
  '07': {
    'primaries': 84,
    'maxi': 10,
    'skills':100,
    'talents':30,
    'bc':15,
  },  
  '06': {
    'primaries': 78,
    'maxi': 10,
    'skills':90,
    'talents':25,
    'bc':10,
  },
  '05': {
    'primaries': 72,
    'maxi': 9,
    'skills':80,
    'talents':20,
    'bc':10,
  },
  '04': {
    'primaries': 66,
    'maxi': 8,
    'skills':70,
    'talents':15,
    'bc':10,
  },
  '03': {
    'primaries': 60,
    'maxi': 8,
    'skills':60,
    'talents':10,
    'bc':5,
  },
  '02': {
    'primaries': 54,
    'maxi': 7,
    'skills':50,
    'talents':5,
    'bc':0,
  },
  '01': {
    'primaries': 48,
    'maxi': 7,
    'skills':40,
    'talents':5,
    'bc':0,
  },
}


EVERYMAN = {
  "ascorbite": {},
  "etyri": {},
  "gannok": {},
  "hironem": {},
  "kurgan": {
    'Academia':2,
    'Dogma':1,
    'Dogma (Kurgan El-Diin)':2,
    'Fight':2,
    'Focus':2,
    'Observe':2,
    'Linguistics':1,
    'Linguistics (Kurgan)':2,
    'Persuasion':2,
    'Seduction':2,
    'Teaching':2,  
  },  
  "obuni": {
    'Academia':2,
    'Arts':2,
    'Dogma':2,
    'Fight':2,
    'Focus':2,
    'Observe':2,
    'Persuasion':2,
    'Teaching':2,
  },
  "oro'ym": {},
  "ukari": {
    'Athletics':2,
    'Empathy':2,
    'Fight':2,
    'Focus':2,
    'Melee':2,
    'Linguistics':2,
    "Linguistics (Ba'amon carvings)":2,
    'Linguistics (Ukari)':2,
    'Observe':2,
    'Stealth':2,
    'Teaching':2,
  },
  "urthish": {
    'Academia':2,
    'Athletics':2,
    'Fight':2,
    'Focus':2,
    'Local Expert':2,
#    'Local Expert (Veneto Province)':1,
#    'Local Expert (Miret)':1,
    'Observe':2,
    'Persuasion':2,
    'Teaching':2,
  },
  "symbiot": {},
  "vau": {},
  "vorox": {
    'Acrobatics':2,
    'Athletics':2,
    'Alchemy':2,
    'Athletics':2,
    'Fight':2,
    'Impress':2,
    'Surveillance':2,
    'Survival':2,
  },
  "vuldrok": {
    'Academia':2,
    'Dogma':1,
    'Dogma (Vuldrok Erdgheist)':2,
    'Fight':2,
    'Focus':2,
    'Observe':2,
    'Linguistics':1,
    'Linguistics (Vuldrok)':2,
    'Persuasion':2,
    'Teaching':2,  
    'Warfare':2,  
  },  
}

RACIAL_ATTRIBUTES = {
  "ascorbite": {},
  "etyri": {},
  "gannok": {},
  "hironem": {},
  "kurgan": {},  
  "obuni": {
    'PA_REF':1,
    'PA_AGI':1,
    'PA_STR':-1,
    'PA_BOD':-1,
    'PA_CON':-1,
    'occult_level':1
  },
  "oro'ym": {},
  "ukari": {
    'PA_REF':1,
    'PA_AGI':1,
    'PA_STR':-1,
    'PA_BOD':-1,
    'PA_CON':-1,
    'PA_TEC':1,
    'occult_level':1,
    'occult_darkside':1,
  },  
  "urthish": {},
  "symbiot": {},
  "vau": {},
  "vorox": {
    'PA_STR': 2,
    'PA_CON': 2,
    'PA_BOD': 4,
    'PA_INT':-1,
    'PA_TEC':-2,
    'PA_TEM': 1,
  },
  "vuldrok": {},  
}

SHORTCUTS = {
    "Observe":{
      'attribute':"PA_AWA",
      'label': "AWA + Observe",  
    },
    "Empathy":{
      'attribute':"PA_TEM",
      'label': "AWA + Empathy",  
    },
    "Dodge":{
      'attribute':"PA_AGI",
      'label': "AGI + Dodge",  
    },
    "Shoot":{
      'attribute':"PA_REF",
      'label': "REF + Shoot",  
    },    
    "Melee":{
      'attribute':"PA_REF",
      'label': "REF + Melee",  
    },
    "Persuasion":{
      'attribute':"PA_PRE",
      'label': "PRE + Persuasion",  
    },
    "Seduction":{
      'attribute':"PA_PRE",
      'label': "PRE + Seduction",  
    },
    "Leadership":{
      'attribute':"PA_PRE",
      'label': "PRE + Leadership",  
    },

    "Stoic Mind":{
      'attribute':'PA_WIL',
      'label': 'WIL + Stoic Mind',  
    },
    'Focus':{
      'attribute':'PA_WIL',
      'label': 'WIL + Focus',  
    },    

  }


ATTACK_ROLLS = {
  'MELEE': {
    'attribute': 'PA_REF',
    'skill': 'Melee',
  },
  'P': {
    'attribute': 'PA_REF',
    'skill': 'Shoot',
  },
  'RIF': {
    'attribute': 'PA_REF',
    'skill': 'Shoot',
  },
  'SMG': {
    'attribute': 'PA_REF',
    'skill': 'Shoot',
  },
  'HVY': {
    'attribute': 'PA_REF',
    'skill': 'Heavy Weapons',
  },  
}


def check_secondary_attributes(ch):
  ch.SA_REC = ch.PA_STR + ch.PA_CON
  ch.SA_STA = math.ceil(ch.PA_BOD / 2) - 1
  ch.SA_END = (ch.PA_BOD + ch.PA_STR) * 5
  ch.SA_STU = ch.PA_CON + ch.PA_BOD
  ch.SA_RES = ch.PA_WIL + ch.PA_PRE
  ch.SA_DMG = math.ceil(ch.PA_STR / 2) - 2
  ch.SA_TOL = ch.PA_TEM + ch.PA_WIL
  ch.SA_HUM = (ch.PA_TEM + ch.PA_WIL) * 5
  ch.SA_PAS = ch.PA_TEM + ch.PA_AWA
  ch.SA_WYR = ch.PA_INT + ch.PA_REF
  ch.SA_SPD = math.ceil(ch.PA_REF / 2)
  ch.SA_RUN = ch.PA_MOV *2


def check_everyman_skills(ch):
  from collector.models.skills import Skill
  skills = ch.skill_set.all()
  for every in EVERYMAN[ch.species]:
    every_found = False
    for s in skills:
      if s.skill_ref.reference == every:
        every_found = True
        val = int(EVERYMAN[ch.species][every])
        if s.value < val:          
          print("Value fixed for %s (%s)"%(s.skill_ref.reference,val))
          this_skill = Skill.objects.get(id=s.id)
          this_skill.value = value
          this_skill.save()
        break
    if not every_found:
      print("Not found: %s... Added!"%every)
      val = int(EVERYMAN[ch.species][every])
      this_skill_ref = SkillRef.objects.get(reference=every)
      this_skill = Skill()
      this_skill.character=ch
      this_skill.skill_ref=this_skill_ref
      this_skill.value = val
      this_skill.save()


def check_gm_shortcuts(ch,sk):
  """ Check for Gamemaster shortcuts for the character """
  if sk.skill_ref.reference in SHORTCUTS:
    score = sk.value + getattr(ch,SHORTCUTS[sk.skill_ref.reference]['attribute'])
    newshortcut = '%s: <b>%d</b>'%(SHORTCUTS[sk.skill_ref.reference]['label'],score)
    return newshortcut  
  else:
    return ""


def check_nameless_attributes(ch):
  res = ''
  PA_PHY = (ch.PA_STR + ch.PA_CON + ch.PA_BOD + ch.PA_MOV) // 4
  PA_SPI = (ch.PA_INT + ch.PA_WIL + ch.PA_TEM + ch.PA_PRE) // 4
  PA_COM = (ch.PA_TEC + ch.PA_REF + ch.PA_AGI + ch.PA_AWA) // 4
  res = '<h2>Nameless</h2>Physical:<b>%s</b> Spirit:<b>%s</b> Combat:<b>%s</b>' % (PA_PHY,PA_SPI,PA_COM)
  return res

def check_attacks(ch):
  """ Attacks shortcuts depending on the avatar and his/her weapons and skills """
  ranged_attack = '<h2>Weapons</h2>'
  for w in ch.weapon_set.all():
    if w.weapon_ref.category in {'P','RIF','SMG'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Shoot').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg)
      ranged_attack += '%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></br>'%(w.weapon_ref.reference,score,x[0],x[1])
    if w.weapon_ref.category in {'HVY'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Heavy Weapons').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg)
      ranged_attack += '%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></br>'%(w.weapon_ref.reference,score,x[0],x[1])
    if w.weapon_ref.category in {'MELEE'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Melee').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg) 
      ranged_attack += '%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d (+str:%d)</b></br>'%(w.weapon_ref.reference,score,x[0],x[1], ch.SA_DMG)
  tmpstr = filter(None,ranged_attack.split('</br>'))
  ranged_attack = '<br/>'.join(tmpstr) 
  return ranged_attack

def get_rid(s):
  x = s.replace(' ','_').replace("'",'').replace('é','e').replace('è','e').replace('ë','e').replace('â','a').replace('ô','o').replace('"','').replace('ï','i').replace('à','a').replace('-','')
  return x.lower()

def minmax_from_dc(sdc):
  if sdc == '':
    return (0,0)
  s = sdc.lower()
  dmin,dmax,dbonus = 0,0,0
  split_bonus = s.split('+')
  split_scope = split_bonus[0].split('d')
  if split_bonus.count == 2:
    dbonus = int(split_bonus[1])
  dmin = int(split_scope[0])+dbonus
  dmax = dmin*int(split_scope[1])+dbonus
  return (dmin,dmax)

def sanitize(character,f):
  sane_f = {}
  for key, value in f.items():
    rkey,rvalue = character.update_field(key, value)
    if rkey != False:
      sane_f[rkey] = rvalue
  return sane_f


def check_root_skills(ch):
  exportable = True
  skills = ch.skill_set.all()
  for root in skills:
    if root.skill_ref.is_root:
      cnt = 0
      for spec in skills:
        if spec.skill_ref.is_speciality:
          if spec.skill_ref.linked_to == root.skill_ref:
            cnt += 1
      if cnt >= root.value:
        if cnt > root.value:
          root.value = cnt
          print('Fixing root value for %s...'%root.skill_ref.reference)
        #else:         
          #print('OK for %s'%root.skill_ref.reference)
      else:
        print('Warning: Missing %d specialties for %s\n'% (root.value-cnt,root.skill_ref.reference))
        exportable = False
  return exportable

def roll(maxi):
  """ A more random 1 to maxi dice roller  """
  randbyte = int.from_bytes(os.urandom(1),byteorder='big',signed=False)
  x = int(randbyte / 256 * (maxi-1)) +1
  return x

def choose_pa(weights):
  #x = randint(1,sum(weights))
  x = roll(sum(weights))
  cum = 0
  idx = 0
  while idx < 12:
    cum += weights[idx]
    if x < cum:
      return idx
    idx += 1
  return -1

def check_primary_attributes(ch):
  pool = ROLES[ch.role]['primaries']
  maxi = ROLES[ch.role]['maxi']
  weights = PROFILES[ch.profile]['weights']
  ch.challenge = '(<i class="fas fa-th-large"></i>%02d <i class="fas fa-th-list"></i>%02d <i class="fas fa-th"></i>%02d <i class="fas fa-outdent"></i>%02d)'%(ROLES[ch.role]['primaries'],ROLES[ch.role]['skills'], ROLES[ch.role]['talents'],ROLES[ch.role]['bc'])
  #print('%s: %s [ %d / %d ]'%(ch.full_name,ch.role,pool,maxi))  
  pas = [2,2,2,2,2,2,2,2,2,2,2,2]
  current =  ch.PA_STR+ch.PA_CON+ch.PA_BOD+ch.PA_MOV+ch.PA_INT+ch.PA_WIL+ch.PA_TEM+ch.PA_PRE+ch.PA_TEC+ch.PA_REF+ch.PA_AGI+ch.PA_AWA
  #print('Current PA TOTAL: %d'%(current))
  if (current < pool or ch.keyword =='rebuild') and ch.player == '':
    pool = pool-24
    #print('Error: Primary Attributes invalid. Fixing that\n')
    while pool>0:      
      chosen_pa = choose_pa(weights)
      idx = chosen_pa
      if pas[idx] < maxi:
        pas[idx] += 1
        pool -= 1
      #else:
        #print('Invalid : already too high!!!')
    #print(pas)
    ch.PA_STR = pas[0]
    ch.PA_CON = pas[1]
    ch.PA_BOD = pas[2]
    ch.PA_MOV = pas[3]
    
    ch.PA_INT = pas[4]
    ch.PA_WIL = pas[5]
    ch.PA_TEM = pas[6]
    ch.PA_PRE = pas[7]
    
    ch.PA_TEC = pas[8]
    ch.PA_REF = pas[9]
    ch.PA_AGI = pas[10]
    ch.PA_AWA = pas[11]
    if ch.keyword == 'rebuild':
      ch.keyword = 'rebuilt'



def check_role(ch):
  pa_pool = ROLES[ch.role]['primaries']
  sk_pool = ROLES[ch.role]['skills']
  ta_pool = ROLES[ch.role]['talents']
  bc_pool = ROLES[ch.role]['bc']
  status = True
  if ch.PA_TOTAL < pa_pool or ch.SK_TOTAL < sk_pool or ch.TA_TOTAL < ta_pool or ch.BC_TOTAL < bc_pool:
    status = False 
  return status
