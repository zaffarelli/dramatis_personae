from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import hashlib
#from collector import fs_fics7
#from .utils import write_pdf


MAX_CHAR = 10
RELEASE = 0.7

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
