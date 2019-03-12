'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import hashlib
#from collector import fs_fics7
#from .utils import write_pdf

"""
  (from Fading Suns CoreRulebook p91-92)
  Base AP..................: 60 AP -> 180 OP
  Base Skill OP............: 30 OP
  Everyman Skill OP .......: 20 OP
  Blessing/Curses..........: 10 OP
  Extra OP.................: 40 OP
  TOTAL ...................: 280 OP
"""

MAX_CHAR = 8
RELEASE = '0.9.11'
DEBUG_ALL = False

"""
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
  ('diplomat',"Diplomat"),
  ('bully','Bully'),
  ('undefined','Undefined'),
)
"""

GROUPCHOICES=(
  ('AWA',"Awareness"),
  ('BOD',"Physical"),
  ('CON',"Control"),
  ('DIP',"Diplomacy"),
  ('EDU',"Education"),
  ('FIG',"Combat"),
  ('PER',"Performance"),
  ('SOC',"Social"),
  ('SPI',"Spirituality"),
  ('TIN',"Tinkering"),
  ('UND',"Underworld"),
)
"""
CATEGORYCHOICES=(
  ('no',"Uncategorized"),
  ('co',"Combat"),
  ('di',"Diplomacy"),
  ('sp',"Spirituality"),
  ('te',"Technical"),
  ('ac',"Action"),
)

CUSTOMGROUPS=(
  ('all','No group at all'),
  ('pil','Pilot'),
  ('sci','Science'),
  ('fig','Fight'),
)
"""

"""
Groups: AWA BOD CON EDU FIG PER SOC TIN
                    SPI         UND
                    DIP
"""

"""
PROFILES = {
  'physical': {
    'weights':[3,3,3,3,1,1,1,1,1,1,1,1],
    'groups':['FIG','BOD','UND','CON'],
  },
  'spiritual': {
    'weights':[1,1,1,1,3,3,3,3,1,1,1,1],
    'groups':['SOC','AWA','SPI','PER'],
  },
  'tech': {
    'weights':[1,1,1,1,1,1,1,1,3,3,3,3],
    'groups':['TIN','CON','AWA','EDU'],
  },  
  'courtisan': {
    'weights':[2,2,2,2,2,2,2,2,1,1,1,1],
    'groups':['FIG','SOC','PER','DIP'],
  },
  'scholar': {
    'weights':[1,1,1,1,3,3,3,3,3,3,3,3],
    'groups':['EDU','SOC','DIP','AWA'],
  },
  'guilder': {
    'weights':[2,2,2,2,1,1,1,1,2,2,2,2],
    'groups':['FIG','TIN','CON','UND']
  },    
  'standard': {
    'weights':[1,1,1,1,1,1,1,1,1,1,1,1],
    'groups':[]
  },
  'diplomat': {
    'weights':[1,1,1,1,3,3,3,3,1,1,1,1],
    'groups':['SOC','PER', 'AWA', 'DIP']
  },
  'bully': {
    'weights':[2,2,2,2,1,1,1,1,2,2,2,2],
    'groups':['UND','FIG', 'AWA', 'CON']
  },        
}
"""
"""
ROLES = {
  '08': {
    'primaries': 76,
    'maxi': 12,
    'mini': 4,
    'skills':150,
    'talents':0,
    'ba':15,
    'bc':0,
  },
  '07': {
    'primaries': 72,
    'maxi': 11,
    'mini': 4,
    'skills':130,
    'talents':0,
    'ba':10,
    'bc':0,
  },  
  '06': {
    'primaries': 68,
    'maxi': 10,
    'mini': 4,
    'skills':110,
    'talents':0,
    'ba':10,
    'bc':0,
  },
  '05': {
    'primaries': 66,
    'maxi': 10,
    'mini': 4,
    'skills':100,
    'talents':0,
    'ba':7,
    'bc':0,
  },
  '04': {
    'primaries': 60,
    'maxi': 9,
    'mini': 3,
    'skills':90,
    'talents':0,
    'ba':5,
    'bc':0,
  },
  '03': {
    'primaries': 54,
    'maxi': 9,
    'mini': 3,
    'skills':80,
    'talents':0,
    'ba':2,
    'bc':0,
  },
  '02': {
    'primaries': 50,
    'maxi': 8,
    'mini': 3,
    'skills':70,
    'talents':0,
    'ba':0,
    'bc':0,
  },
  '01': {
    'primaries': 48,
    'maxi': 8,
    'mini': 2,
    'skills':60,
    'talents':0,
    'ba':0,
    'bc':0,
  },
}
"""

"""

EVERYMAN = {
  "ascorbite": {
    'Athletics':2,
    'Alchemy':2,
    'Dodge':2,
    'Linguistics (Ascorbite)':2,
    'Observe':2,
    'Shadowing':2,
    'Stealth':2,
    'Stoic Mind':2,
  },
  "etyri": {
    'Acrobatics':2,
    'Athletics':2,
    'Focus':2,
    'Observe':2,
    'Linguistics (Etyri)':2,
    'Melee':2,
    'Navigation':2,
    'Persuasion':2,    
    'Teaching':2,  
  },  
  "gannok": {
    'Acrobatics':2,
    'Dodge':2,
    'Knavery':2,
    'Linguistics (Gannok)':2,
    'Stoic Body':2,
    'Tinkering':2,
  },    
  "hironem": {
    'Athletics':2,
    'Dogma (Sas Kanasu)':2,
    'Lore (Naaram)':2,
    'Linguistics (Salsu)':2,
    'Observe':2,
    'Stoic Mind':2,
  },
  "kurgan": {
    'Academia':2,
    'Dogma (Kurgan El-Diin)':2,
    'Fight':2,
    'Focus':2,
    'Observe':2,
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
    'Linguistics (Obuni)':2,
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
    "Linguistics (Ba'amon carvings)":1,
    'Linguistics (Ukari)':1,
    'Observe':2,
    'Stealth':2,
    'Teaching':2,
  },
  "urthish": {
    'Academia':2,
    'Athletics':2,
    'Fight':2,
    'Focus':2,
    'Local Expert (Veneto Province)':1,
    'Local Expert (Miret)':1,
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
    'Linguistics (Vorox)':2,
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
    'Linguistics (Vuldrok)':2,
    'Persuasion':2,
    'Teaching':2,  
    'Warfare':2,  
  },  
}
"""
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
      'rationale': "Notice something",
    },
    "Empathy":{
      'attribute':"PA_TEM",
      'label': "AWA + Empathy",
      'rationale': "Discern emotions",
    },
    "Dodge":{
      'attribute':"PA_AGI",
      'label': "AGI + Dodge",
      'rationale': "Avoid being hit",
    },
    "Shoot":{
      'attribute':"PA_REF",
      'label': "REF + Shoot",
      'rationale': "Fire a ranged weapon",
    },    
    "Melee":{
      'attribute':"PA_REF",
      'label': "REF + Melee",
      'rationale': "Fencing",
    },
    "Persuasion":{
      'attribute':"PA_PRE",
      'label': "PRE + Persuasion",
      'rationale': "Convince someone with arguments",
    },
    "Seduction":{
      'attribute':"PA_PRE",
      'label': "PRE + Seduction",
      'rationale': "Charm others",
    },
    "Leadership":{
      'attribute':"PA_PRE",
      'label': "PRE + Leadership",
      'rationale': "Give orders to subsidiaries",
    },

    "Stoic Mind":{
      'attribute':'PA_WIL',
      'label': 'WIL + Stoic Mind',
      'rationale': "Iron will",
    },
    "Focus":{
      'attribute':'PA_WIL',
      'label': 'WIL + Focus',
      'rationale': "Keep focused on a task",  
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
