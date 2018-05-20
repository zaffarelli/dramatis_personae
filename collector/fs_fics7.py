# Fading Suns
# Fusion Interlock Custom System v7
# This file contains the core business function of the app

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
      'attribute':'PA_WIL',
      'label': 'WIL + Stoic Mind',  
    },
    'Focus':{
      'attribute':'PA_WIL',
      'label': 'WIL + Focus',  
    },    

  }

def check_gm_shortcuts(ch,sk):
  """ Check for Gamemaster shortcuts for the character """
  if sk.skill_ref.reference in SHORTCUTS:
    #print(sk.skill_ref.reference)
    #print(SHORTCUTS)
    #print(SHORTCUTS[sk.skill_ref.reference])
    score = sk.value + getattr(ch,SHORTCUTS[sk.skill_ref.reference]['attribute'])
    newshortcut = '%s: <b>%d</b><br/>'%(SHORTCUTS[sk.skill_ref.reference]['label'],score)
    return newshortcut  
  else:
    return ""
    #score = getattr(ch,SHORTCUTS[sk.skill_ref.reference]['attribute']) -2
    #newshortcut = "%s: <b>%d</b> (-2)<br/>"%(SHORTCUTS[sk.skill_ref.reference]['label'],score)
    #return newshortcut

ATTACK_ROLLS = {
  'MELEE': {
    'attribute': 'PA_REF',
    'skill': 'Melee',
  },
}

def get_ranged_attacks(ch):
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
  return ranged_attack

def get_rid(s):
  x = s.replace(' ','_').replace("'",'').replace('é','e').replace('è','e').replace('ë','e').replace('â','a').replace('ô','o').replace('"','').replace('ï','i')
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
