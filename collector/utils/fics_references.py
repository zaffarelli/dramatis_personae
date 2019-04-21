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

MAX_CHAR = 9
RELEASE = '1.2.0 BPE'
DEBUG_ALL = False


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
