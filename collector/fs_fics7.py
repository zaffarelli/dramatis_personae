# Fading Suns
# Constants for FICS7

EVERYMAN = {
  "ascorbite": {},
  "etyri": {},
  "gannok": {},
  "hironem": {},
  "kurgan": {},  
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
  "vuldrok": {},  
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
      'attribute':"PA_WIL",
      'label': "WIL + Stoic Mind",  
    },
    "Focus":{
      'attribute':"PA_WIL",
      'label': "WIL + Focus",  
    },    

  }

def check_gm_shortcuts(ch,sk):
  """ Check for Gamemaster shortcuts for the character """
  if sk.skill_ref.reference in SHORTCUTS:
    #print(sk.skill_ref.reference)
    #print(SHORTCUTS)
    #print(SHORTCUTS[sk.skill_ref.reference])
    score = sk.value + getattr(ch,SHORTCUTS[sk.skill_ref.reference]['attribute'])
    newshortcut = "%s: <b>%d</b><br/>"%(SHORTCUTS[sk.skill_ref.reference]['label'],score)
    return newshortcut
  else:
    return ""

