'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
 Fading Suns
 Fusion Interlock Custom System v7
 This file contains the core business function of the app
'''
import math
from random import randint
import os
import yaml
import json
from collector.models.skill_ref import SkillRef
from collector.utils.fics_references import *
import logging

logger = logging.getLogger(__name__)


def check_secondary_attributes(ch):
  """ Compute all secondary attributes (we check nothing in fact)
  """
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

def fetch_everyman_sum(ch):
  """ Get the sum of everyman skills for the character specie """  
  total = 0
  all_every = ch.specie.get_racial_skills()
  for every in all_every:
    total += all_every[every]
  logger.debug('> Everyman total for [%s] as [%s] is [%d].'%(ch.full_name,ch.specie,total))
  return total
    
def check_everyman_skills(ch):
  """ Check and fix everyman values for the skills"""
  from collector.models.skills import Skill
  skills = ch.skill_set.all()
  all_every = ch.specie.get_racial_skills()
  val_total = 0
  for every in all_every:
    every_found = False
    for s in skills:
      if s.skill_ref.reference == every:
        every_found = True
        val = all_every[every]
        #if s.value < val:          
        logger.debug('Everyman: Value fixed for %s (%s)'%(s.skill_ref.reference,val))
        this_skill = Skill.objects.get(id=s.id)
        this_skill.value += val
        val_total += val
        this_skill.save()
        break
    if not every_found:
      val = all_every[every]
      logger.debug('Everyman: Not found: %s... Added value %d!'%(every,val))
      this_skill_ref = SkillRef.objects.get(reference=every)
      this_skill = Skill()
      this_skill.character=ch
      this_skill.skill_ref=this_skill_ref
      this_skill.value = val
      val_total += val
      this_skill.save()
  return val_total

def check_gm_shortcuts(ch,sk):
  """ Check for Gamemaster shortcuts for the character """
  if sk.skill_ref.reference in SHORTCUTS:
    score = sk.value + getattr(ch,SHORTCUTS[sk.skill_ref.reference]['attribute'])
    newshortcut = '<p>%s (%s): <b>%d</b></p>'%(SHORTCUTS[sk.skill_ref.reference]['rationale'],SHORTCUTS[sk.skill_ref.reference]['label'],score)
    return newshortcut  
  else:
    return ''


def check_nameless_attributes(ch):
  res = ''
  PA_PHY = (ch.PA_STR + ch.PA_CON + ch.PA_BOD + ch.PA_MOV) // 4
  PA_SPI = (ch.PA_INT + ch.PA_WIL + ch.PA_TEM + ch.PA_PRE) // 4
  PA_COM = (ch.PA_TEC + ch.PA_REF + ch.PA_AGI + ch.PA_AWA) // 4
  res = '<h6>Nameless</h6>Physical:<b>%s</b> Spirit:<b>%s</b> Combat:<b>%s</b>' % (PA_PHY,PA_SPI,PA_COM)
  return res

def check_attacks(ch):
  """ Attacks shortcuts depending on the avatar and his/her weapons and skills """
  ranged_attack = '<h6>Attacks</h6>'
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
      ranged_attack += '<p>%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></p>'%(w.weapon_ref.reference,score,x[0],x[1])
    if w.weapon_ref.category in {'HVY'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Heavy Weapons').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg)
      ranged_attack += '<p>%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></p>'%(w.weapon_ref.reference,score,x[0],x[1])
    if w.weapon_ref.category in {'MELEE'}:      
      sk = ch.skill_set.filter(skill_ref__reference='Melee').first()
      if sk is None:
        sval = 0
      else:
        sval = sk.value
      score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
      dmg = w.weapon_ref.damage_class
      x = minmax_from_dc(dmg) 
      ranged_attack += '<p>%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d (+str:%d)</b></p>'%(w.weapon_ref.reference,score,x[0],x[1], ch.SA_DMG)
  tmpstr = filter(None,ranged_attack.split('</br>'))
  ranged_attack = '<br/>'.join(tmpstr) 
  return ranged_attack

def check_health(ch):
  health_entries = []
  
  return ''.join(health_entries)


def stack_defenses(defenses,a):
  if a:
    if a.armor_ref.head:
      defenses['head'] += a.armor_ref.stopping_power
    if a.armor_ref.right_arm:
      defenses['right_arm'] = a.armor_ref.stopping_power
    if a.armor_ref.torso:
      defenses['torso'] += a.armor_ref.stopping_power
    if a.armor_ref.left_arm:
      defenses['left_arm'] += a.armor_ref.stopping_power
    if a.armor_ref.right_leg:
      defenses['right_leg'] += a.armor_ref.stopping_power
    if a.armor_ref.left_leg:
      defenses['left_leg'] += a.armor_ref.stopping_power
  return defenses

def check_defense(ch):
  """ Calculate defense statistics """
  defenses = {'head':0,'right_arm':0,'torso':0,'left_arm':0,'right_leg':0,'left_leg':0}
  best_soft = None
  best_medium = None
  best_hard = None
  stack = 'Armors stack: '
  for a in ch.armor_set.all():
    if a.armor_ref.category == 'Soft':
      if best_soft == None or (a.armor_ref.stopping_power > best_soft.armor_ref.stopping_power):
        best_soft = a
        stack += best_soft.armor_ref.reference+' '
    if a.armor_ref.category == 'Medium':
      if best_medium == None or (a.armor_ref.stopping_power > best_medium.armor_ref.stopping_power):
        best_medium = a
        stack += best_medium.armor_ref.reference+' '
    if a.armor_ref.category == 'Hard':
      if best_hard == None or (a.armor_ref.stopping_power > best_hard.armor_ref.stopping_power):
        best_hard = a
        stack += best_hard.armor_ref.reference+' '
  a = best_soft
  defenses = stack_defenses(defenses,a)
  a = best_medium
  defenses = stack_defenses(defenses,a)
  a = best_hard
  defenses = stack_defenses(defenses,a)
  defenses['stack']= stack

  defense_str = '<h6>Defense</h6>'
  defense_str += '%s'%(stack)
  defense_str += '<p>Head:%d'%(defenses['head'])
  defense_str += '<br/>Right Arm:%d Torso:%d Left_arm:%d'%(defenses['right_arm'],defenses['torso'],defenses['left_arm'])
  defense_str += '<br/>Right Leg:%d Left_Leg:%d</p>'%(defenses['right_leg'],defenses['left_leg'])
  
  return defense_str

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

def roll(maxi):
  """ A more random '1 to maxi' dice roller  """
  randbyte = int.from_bytes(os.urandom(1),byteorder='big',signed=False)
  x = int(randbyte / 256 * (maxi)) +1
  return x

def choose_pa(weights,maxi,pa):
  #x = randint(1,sum(weights))
  res = -1
  done = False
  attempts = 10
  while not done:
    x = roll(sum(weights))
    cum = 0
    idx = 0
    while idx < 12:
      cum += weights[idx]
      if x <= cum:
        res = idx
        idx = 12
        done = True
      if pa[res]>=maxi:
        res = -1
        idx = 12
        attempts -= 1
        done = False
      if attempts <= 0:
        idx = 12
        done = True
      idx += 1
  return res


def list_attributes(ch,pas):
  if pas == None:
    print()
    print('Attributes for %s'%(ch.rid))
    row =  'STR%2d CON%2d'%(ch.PA_STR,ch.PA_CON)
    row += '  INT%2d WIL%2d'%(ch.PA_INT,ch.PA_WIL)
    row += '  TEC%2d REF%2d'%(ch.PA_TEC,ch.PA_REF)
    print(row)
    row =  'BOD%2d MOV%2d'%(ch.PA_BOD,ch.PA_MOV)
    row += '  TEM%2d PRE%2d'%(ch.PA_TEM,ch.PA_PRE)
    row += '  AGI%2d AWA%2d'%(ch.PA_AGI,ch.PA_AWA)
    print(row)

    row  = '>> PHY %2d '%(ch.PA_STR+ch.PA_CON+ch.PA_BOD+ch.PA_MOV)
    row += ' + MEN %2d'%(ch.PA_INT+ch.PA_WIL+ch.PA_TEM+ch.PA_PRE)
    row += ' + COM %2d'%(ch.PA_TEC+ch.PA_REF+ch.PA_AGI+ch.PA_AWA)
    row += ' = TOTAL %2d'%(ch.PA_STR+ch.PA_CON+ch.PA_BOD+ch.PA_MOV+ch.PA_INT+ch.PA_WIL+ch.PA_TEM+ch.PA_PRE+ch.PA_TEC+ch.PA_REF+ch.PA_AGI+ch.PA_AWA)
    print(row)
  else:
    print()
    print('Attributes for %s'%(ch.rid))
    row =  'STR%2d CON%2d'%(pas[0],pas[1])
    row += '  INT%2d WIL%2d'%(pas[4],pas[5])
    row += '  TEC%2d REF%2d'%(pas[8],pas[9])
    print(row)
    row =  'BOD%2d MOV%2d'%(pas[2],pas[3])
    row += '  TEM%2d PRE%2d'%(pas[6],pas[7])
    row += '  AGI%2d AWA%2d'%(pas[10],pas[11])
    print(row)

    row  = '>> PHY %2d '%(pas[0]+pas[1]+pas[2]+pas[3])
    row += ' + MEN %2d'%(pas[4]+pas[5]+pas[6]+pas[7])
    row += ' + COM %2d'%(pas[8]+pas[9]+pas[10]+pas[11])
    row += ' = TOTAL %2d'%(sum(pas))
    print(row)    

def check_primary_attributes(ch):
  """ Fixing primary attributes """
  if ch.onsave_reroll_attributes:
    pool = ch.role.primaries
    maxi = ch.role.maxi
    mini = int(ch.role.mini)
    pas = [ mini for i in range(12) ]
    pool -= sum(pas)
    weights = ch.profile.get_weights()
    balance = ch.specie.attr_mod_balance
    if ch.player == '':
      while pool>0:
        chosen_pa = choose_pa(weights,maxi,pas)
        idx = chosen_pa
        pas[idx] += 1
        pool -= 1
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
      ch.apply_racial_pa_mods()
      #list_attributes(ch,None)
    ch.onsave_reroll_attributes = False


def get_skills_list(ch,groups):
  """ Prepare the list of skills without specialities """
  skills = SkillRef.objects.all().filter(is_speciality=False)
  master_skills = []
  #gweight = 1
  for s in skills:
    weight = 1
    for g in groups:
      if s.group == g:
        weight = 3 if s.is_root else 2
        #weight += gweight
        #gweight += 1        
    master_skills.append({'skill':s.reference, 'data':s, 'weight':weight})
  msl = []
  
  logger.debug('MASTER LIST')
  for ms in sorted(master_skills,key=lambda ms: ms['skill']):
    logger.debug('%s%s: %d'%('  ' if ms['data'].is_root else '', ms['skill'],ms['weight']))
  return master_skills

def pick_a_speciality_for(s):
  skills = SkillRef.objects.all().filter(is_speciality=True,linked_to=s)
  x = roll(skills.count())
  return skills[x-1]

def choose_sk(alist,maxweight):
  x = roll(maxweight)
  cum = 0
  idx = 0
  while idx < len(alist):
    cum += alist[idx]['weight']
    if x <= cum:
      if alist[idx]['data'].is_root:
        return pick_a_speciality_for(alist[idx]['data'])
      else:
        return alist[idx]['data']
    idx += 1
  return None


def check_skills(ch):
  """ Fixing skills """
  skills_randomizer(ch)

def check_role(ch):
  #print('> %s:'%(ch.full_name))
  pa_pool = ch.role.primaries
  sk_pool = ch.role.skills
  ta_pool = ch.role.talents
  bc_pool = ch.role.bc
  ba_pool = ch.role.ba
  status = True
  if ch.PA_TOTAL < pa_pool:
    logger.info('   Not enough PA: %d (%d)'%(ch.PA_TOTAL,pa_pool))
    status = False 
  elif ch.SK_TOTAL+ch.specie.skill_balance < sk_pool:
    logger.info('   Not enough SK: %d (%d)'%(ch.SK_TOTAL+ch.specie.skill_balance,sk_pool))
    status = False 
  if ch.BA_TOTAL + ch.BC_TOTAL + ch.TA_TOTAL < ba_pool+bc_pool+ta_pool:
    logger.info('   Not enough OP (Talents + Benefice/Afflictions + Blessing/Curses): %d (%d)'%(ch.BA_TOTAL + ch.BC_TOTAL + ch.TA_TOTAL,ba_pool+bc_pool+ta_pool))
    result = False 
  return status

def update_challenge(ch):
  res = ''
  #ch.score = ch.OP / 100
  #res += '%s '%(''.join([ '<i class="fas fa-star fa-xs"></i>' if i<ch.score else '<i class="fas fa-star fa-xs low"></i>' for i in range(6) ]))
  res += '<i class="fas fa-th-large" title="primary attributes"></i>%d '%(ch.AP)
  res += '<i class="fas fa-th-list" title="skills"></i> %d '%(ch.SK_TOTAL)
  res += '<i class="fas fa-th" title="talents"></i> %d '%(ch.TA_TOTAL+ch.BC_TOTAL+ch.BA_TOTAL)
  res += '<i class="fas fa-newspaper" title="OP challenge"></i> %d '%(ch.OP)

  
  return res



def find_rid(s):
  x = s.replace(' ','_').replace("'",'').replace('é','e').replace('è','e').replace('ë','e').replace('â','a').replace('ô','o').replace('"','').replace('ï','i').replace('à','a').replace('-','')
  rid = x.lower()
  return rid

def get_options():
  options = None
  with open('config.yml', 'r') as stream:
    try:
      options = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)
  return options



# New version of the skills randomizer 

def list_skills(ch):
  print("> Skills for %s"%(ch.full_name))
  pool = ch.role.skills
  unit = int(pool / 8)
  modulo = int(pool % 8)
  pool_c = unit*5+modulo
  pool_u = unit*2
  pool_r = unit*1
  print("> Before (%d): c=%4d u=%4d r=%4d"%(pool,pool_c,pool_u,pool_r))
  for skill in ch.skill_set.all().order_by('skill_ref__reference'):
    print("%35s %2d %4s %4s %4s"%(skill.skill_ref.reference,skill.value, '--' if skill.skill_ref.is_common else 'UNCO', 'SPEC' if skill.skill_ref.is_speciality else '--', 'ROOT' if skill.skill_ref.is_root else '--' ))
    if skill.skill_ref.is_speciality == True:
      pool_r -= skill.value
    elif skill.skill_ref.is_common == False:
      pool_u -= skill.value
    elif skill.skill_ref.is_root == False:
      pool_c -= skill.value
  print("> Pools (%d): c=%4d u=%4d r=%4d"%(pool,pool_c,pool_u,pool_r))


def skills_randomizer(ch):
  """ New function to properly calculate random skills"""
  if ch.onsave_reroll_skills == True:

    # 1) Prepare everything
    pool = ch.role.skills
    root_amount = ch.role.skill_roots
    maxi = ch.role.maxi
    #groups = ch.profile.get_groups()
    #current = ch.SK_TOTAL
    balance = ch.specie.skill_balance
    unit = int(pool / 8)
    modulo = int(pool % 8)
    pool_c = unit*5+modulo
    pool_u = unit*2
    pool_r = unit*1
    ch.purgeSkills()
       

    everyman_total = check_everyman_skills(ch)
    for skill in ch.skill_set.all().order_by('skill_ref__reference'):      
      if skill.skill_ref.is_speciality == True:
        pool_r -= skill.value
      elif skill.skill_ref.is_common == False:
        pool_u -= skill.value
      elif skill.skill_ref.is_root == False:
        pool_c -= skill.value

    # 2) Calculate Common Skills 
    common_skills = get_skills_list(ch,False,True)
    common_weight = 0
    for s in common_skills:
      common_weight += s['weight']
    current = pool_c
    while current>0:
      batch = 1
      if current > (pool_c / 2):
        batch = 3
      chosen_sk = choose_sk(common_skills,common_weight)
      sk = ch.add_or_update_skill(chosen_sk,batch)
      current -= batch

    # 3) Calculate Uncommon skills
    uncommon_skills = get_skills_list(ch,False,False)
    uncommon_weight = 0
    for s in uncommon_skills:
      uncommon_weight += s['weight']
    current = pool_u
    while current>0:
      batch = 1
      chosen_sk = choose_sk(uncommon_skills,uncommon_weight)
      sk = ch.add_or_update_skill(chosen_sk,batch)
      current -= batch
    
    # 4) Calculate Roots
    roots = get_roots_list(ch)
    root_weight = 0
    for s in roots:
      root_weight += s['weight']
    current = pool_r
    while current>0:
      batch = 1
      chosen_sk = choose_sk(roots,root_weight)
      sk = ch.add_or_update_skill(chosen_sk,batch)
      current -= batch
    chosen_roots = ch.skill_set.all().filter(skill_ref__is_root = True)
    for root in chosen_roots:
      local_pool = root.value
      speciality_skills = get_specilities_list(ch,root.skill_ref)
      speciality_weight = 0
      for s in speciality_skills:
        speciality_weight += s['weight']      
      while local_pool>0:
        batch = 1
        chosen_sk = choose_sk(speciality_skills,speciality_weight)
        sk = ch.add_or_update_skill(chosen_sk,batch)
        local_pool -= batch
      root.value = 0
    
    # 5) And we are done :)
    ch.add_missing_root_skills()
    #list_skills(ch)   
    ch.onsave_reroll_skills = False
  else:
    print("Nothing to do...")

def get_skills_list(ch,root,com):
  """ Prepare the list of skills without specialities """
  skills = SkillRef.objects.all().filter(is_speciality=False, is_root = root, is_common = com)
  groups = ch.profile.get_groups()
  result_skills = []
  for s in skills:
    weight = 1
    for g in groups:
      if s.group in g:
        weight = 3
    result_skills.append({'skill':s.reference, 'data':s, 'weight':weight})
  return result_skills

def get_roots_list(ch):
  """ Prepare the list of skills without specialities """
  groups = ch.profile.get_groups()
  skills = SkillRef.objects.all().filter(is_root = True)  
  result_skills = []
  for s in skills:
    weight = 1
    for g in groups:
      if s.group == g:
        weight = 7
    if weight > 0:
      result_skills.append({'skill':s.reference, 'data':s, 'weight':weight})
  return result_skills

def get_specialities_list(ch,root):
  """ Prepare the list of skills without specialities """
  groups = ch.profile.get_groups()
  skills = SkillRef.objects.all().filter(is_speciality = True)  
  result_skills = []
  for s in skills:
    weight = 0
    if s.linked_to == root:
      weight = 1
    if weight > 0:
      result_skills.append({'skill':s.reference, 'data':s, 'weight':weight})
  return result_skills


def get_keywords():
  """ Get all keywords """
  from collector.models.characters import Character
  everybody = Character.objects.all()
  keywords = []
  for someone in everybody:
    if someone.keyword != '':
      keywords.append(someone.keyword)
  return sorted(list(set(keywords)))
