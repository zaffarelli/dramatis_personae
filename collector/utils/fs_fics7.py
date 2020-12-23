"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
 Fading Suns
 Fusion Interlock Custom System v7
 This file contains the core business function of the app
"""
import math
import os
import yaml
from collector.utils.fics_references import *
from collector.utils.rpg import *
import logging


logger = logging.getLogger(__name__)


def check_secondary_attributes(ch):
    """ Compute all secondary attributes (we check nothing in fact)
    """
    ch.SA_REC = ch.PA_STR + ch.PA_CON
    ch.SA_STA = math.ceil(ch.PA_BOD / 2) - 1
    ch.SA_END = (ch.PA_BOD + ch.PA_CON) * 5
    ch.SA_STU = ch.PA_CON + ch.PA_BOD
    ch.SA_RES = ch.PA_WIL + ch.PA_PRE
    ch.SA_DMG = math.ceil(ch.PA_STR / 2) - 2
    ch.SA_TOL = ch.PA_TEM + ch.PA_WIL
    ch.SA_HUM = (ch.PA_TEM + ch.PA_WIL) * 5
    ch.SA_PAS = ch.PA_TEM + ch.PA_AWA
    ch.SA_WYR = ch.PA_INT + ch.PA_REF
    ch.SA_SPD = math.ceil(ch.PA_REF / 2)
    ch.SA_RUN = ch.PA_MOV * 2


def check_gm_shortcuts(ch, sk):
    """ Check for Gamemaster shortcuts for the character """
    if sk.skill_ref.reference in SHORTCUTS:
        score = sk.value + getattr(ch, SHORTCUTS[sk.skill_ref.reference]['attribute'])
        id = ch.rid + "-" + str(score)
        newshortcut = '<tr><td>%s</td><td colspan=4>%s</td><td>%d</td><td><i id="%s" class="action_icon dice_roll fa fa-dice"></i></td></tr>' % (
            SHORTCUTS[sk.skill_ref.reference]['rationale'], SHORTCUTS[sk.skill_ref.reference]['label'], score, id)
        pdf_short = {'rationale': SHORTCUTS[sk.skill_ref.reference]['rationale'],
                     'label': SHORTCUTS[sk.skill_ref.reference]['label'], 'score': score}
        return newshortcut, pdf_short
    else:
        return '', ''


def d12x():
    rolls = []
    total = 0
    details = ""
    x = roll(12)
    rolls.append(x)
    total = x
    if (x == 1):
        details = "[1!]"
        y = roll(12)
        rolls.append(y)
        total -= y
        details += " + (%d!) " % (y)
        while y == 12:
            y = roll(12)
            rolls.append(y)
            total -= y
            details += " + (%d!) " % (y)
    elif (x == 12):
        details = "[12!]"
        y = roll(12)
        rolls.append(y)
        total += y
        details += " + (%d!) " % (y)
        while y == 12:
            y = roll(12)
            rolls.append(y)
            total += y
            details += " + (%d!) " % (y)
    else:
        details = "[" + str(x) + "!]"
    return total, details


def check_nameless_attributes(ch):
    res = ''
    PA_PHY = (ch.PA_STR + ch.PA_CON + ch.PA_BOD + ch.PA_MOV) // 4
    PA_SPI = (ch.PA_INT + ch.PA_WIL + ch.PA_TEM + ch.PA_PRE) // 4
    PA_COM = (ch.PA_TEC + ch.PA_REF + ch.PA_AGI + ch.PA_AWA) // 4
    res = '<h6>Nameless</h6>Physical:<b>%s</b> Spirit:<b>%s</b> Combat:<b>%s</b>' % (PA_PHY, PA_SPI, PA_COM)
    return res


def check_attacks(ch):
    """ Attacks shortcuts depending on the avatar and his/her weapons and skills """
    ranged_attack = '<h6>Attacks</h6>'
    for w in ch.weapon_set.all():
        if w.weapon_ref.category in {'P', 'RIF', 'SMG'}:
            sk = ch.skill_set.filter(skill_ref__reference='Shoot').first()
            if sk is None:
                sval = 0
            else:
                sval = sk.value
            score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
            dmg = w.weapon_ref.damage_class
            x = minmax_from_dc(dmg)
            ranged_attack += '<p>%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></p>' % (
                w.weapon_ref.reference, score, x[0], x[1])
        if w.weapon_ref.category in {'HVY'}:
            sk = ch.skill_set.filter(skill_ref__reference='Heavy Weapons').first()
            if sk is None:
                sval = 0
            else:
                sval = sk.value
            score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
            dmg = w.weapon_ref.damage_class
            x = minmax_from_dc(dmg)
            ranged_attack += '<p>%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d</b></p>' % (
                w.weapon_ref.reference, score, x[0], x[1])
        if w.weapon_ref.category in {'MELEE'}:
            sk = ch.skill_set.filter(skill_ref__reference='Melee').first()
            if sk is None:
                sval = 0
            else:
                sval = sk.value
            score = ch.PA_REF + sval + w.weapon_ref.weapon_accuracy
            dmg = w.weapon_ref.damage_class
            x = minmax_from_dc(dmg)
            ranged_attack += '<p>%s: Roll:<b>%d+1D12</b> Dmg:<b>%d-%d (+str:%d)</b></p>' % (
                w.weapon_ref.reference, score, x[0], x[1], ch.SA_DMG)
    tmpstr = filter(None, ranged_attack.split('</br>'))
    ranged_attack = '<br/>'.join(tmpstr)
    return ranged_attack


def check_health(ch):
    health_entries = []
    return ''.join(health_entries)


def stack_defenses(defenses, a):
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
    defenses = {'head': 0, 'right_arm': 0, 'torso': 0, 'left_arm': 0, 'right_leg': 0, 'left_leg': 0}
    best_soft = None
    best_medium = None
    best_hard = None
    stack = 'Armors stack: '
    for a in ch.armor_set.all():
        if a.armor_ref.category == 'Soft':
            if best_soft == None or (a.armor_ref.stopping_power > best_soft.armor_ref.stopping_power):
                best_soft = a
                stack += best_soft.armor_ref.reference + ' '
        if a.armor_ref.category == 'Medium':
            if best_medium == None or (a.armor_ref.stopping_power > best_medium.armor_ref.stopping_power):
                best_medium = a
                stack += best_medium.armor_ref.reference + ' '
        if a.armor_ref.category == 'Hard':
            if best_hard == None or (a.armor_ref.stopping_power > best_hard.armor_ref.stopping_power):
                best_hard = a
                stack += best_hard.armor_ref.reference + ' '
    a = best_soft
    defenses = stack_defenses(defenses, a)
    a = best_medium
    defenses = stack_defenses(defenses, a)
    a = best_hard
    defenses = stack_defenses(defenses, a)
    defenses['stack'] = stack

    defense_str = '<h6>Defense</h6>'
    defense_str += '%s' % (stack)
    defense_str += '<p>Head:%d' % (defenses['head'])
    defense_str += '<br/>Right Arm:%d Torso:%d Left_arm:%d' % (
        defenses['right_arm'], defenses['torso'], defenses['left_arm'])
    defense_str += '<br/>Right Leg:%d Left_Leg:%d</p>' % (defenses['right_leg'], defenses['left_leg'])

    return defense_str


def minmax_from_dc(sdc):
    if sdc == '':
        return (0, 0)
    s = sdc.lower()
    dmin, dmax, dbonus = 0, 0, 0
    split_bonus = s.split('+')
    split_scope = split_bonus[0].split('d')
    if split_bonus.count == 2:
        dbonus = int(split_bonus[1])
    dmin = int(split_scope[0]) + dbonus
    dmax = dmin * int(split_scope[1]) + dbonus
    return (dmin, dmax)


def roll_dc(sdc):
    if sdc == '':
        return 0
    s = sdc.lower()
    total, dbonus = 0, 0
    split_bonus = s.split('+')
    split_scope = split_bonus[0].split('d')
    if split_bonus.count == 2:
        dbonus = int(split_bonus[1])
    d = 0
    while d < int(split_scope[0]):
        total += roll(int(split_scope[1]))
        d += 1
    total += dbonus
    return total





def choose_pa(weights, maxi, pa):
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
            if pa[res] >= maxi:
                res = -1
                idx = 12
                attempts -= 1
                done = False
            if attempts <= 0:
                idx = 12
                done = True
            idx += 1
    return res


def get_skills_list(ch, groups):
    """ Prepare the list of skills without specialities """
    from collector.models.skill import SkillRef
    skills = SkillRef.objects.all().filter(is_speciality=False)
    master_skills = []
    for s in skills:
        weight = 1
        for g in groups:
            if s.group == g:
                weight = 3 if s.is_root else 2
        master_skills.append({'skill': s.reference, 'data': s, 'weight': weight})

    logger.debug('MASTER LIST')
    for ms in sorted(master_skills, key=lambda ms: ms['skill']):
        logger.debug('%s%s: %d' % ('  ' if ms['data'].is_root else '', ms['skill'], ms['weight']))
    return master_skills


def pick_a_speciality_for(s):
    from collector.models.skill import SkillRef
    skills = SkillRef.objects.all().filter(is_speciality=True, linked_to=s)
    x = roll(skills.count())
    return skills[x - 1]


def choose_sk(alist, maxweight):
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


def find_rid(s):
    x = s.replace(' ', '_').replace("'", '').replace('é', 'e') \
        .replace('è', 'e').replace('ë', 'e').replace('â', 'a') \
        .replace('ô', 'o').replace('"', '').replace('ï', 'i') \
        .replace('à', 'a').replace('-', '')
    rid = x.lower()
    return rid


def get_options():
    options = None
    with open('config.yml', 'r') as stream:
        try:
            options = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(exc)
    return options


def list_skills(ch):
    print("> Skills for %s" % (ch.full_name))
    pool = ch.role.skills
    unit = int(pool / 8)
    modulo = int(pool % 8)
    pool_c = unit * 5 + modulo
    pool_u = unit * 2
    pool_r = unit * 1
    print("> Before (%d): c=%4d u=%4d r=%4d" % (pool, pool_c, pool_u, pool_r))
    for skill in ch.skill_set.all().order_by('skill_ref__reference'):
        print("%35s %2d %4s %4s %4s" % (
            skill.skill_ref.reference, skill.value, '--' if skill.skill_ref.is_common else 'UNCO',
            'SPEC' if skill.skill_ref.is_speciality else '--', 'ROOT' if skill.skill_ref.is_root else '--'))
        if skill.skill_ref.is_speciality == True:
            pool_r -= skill.value
        elif skill.skill_ref.is_common == False:
            pool_u -= skill.value
        elif skill.skill_ref.is_root == False:
            pool_c -= skill.value
    print("> Pools (%d): c=%4d u=%4d r=%4d" % (pool, pool_c, pool_u, pool_r))


def get_skills_list(ch, root, com):
    """ Prepare the list of skills without specialities """
    from collector.models.skill import SkillRef
    skills = SkillRef.objects.all().filter(is_speciality=False, is_root=root, is_common=com)
    groups = ch.profile.get_groups()
    result_skills = []
    for s in skills:
        weight = 1
        for g in groups:
            if s.group in g:
                weight = 3
        result_skills.append({'skill': s.reference, 'data': s, 'weight': weight})
    return result_skills


def get_roots_list(ch):
    """ Prepare the list of skills without specialities """
    from collector.models.skill import SkillRef
    groups = ch.profile.get_groups()
    skills = SkillRef.objects.all().filter(is_root=True)
    result_skills = []
    for s in skills:
        weight = 1
        for g in groups:
            if s.group == g:
                weight = 7
        if weight > 0:
            result_skills.append({'skill': s.reference, 'data': s, 'weight': weight})
    return result_skills


def get_specialities_list(ch, root):
    """ Prepare the list of skills without specialities """
    from collector.models.skill import SkillRef
    groups = ch.profile.get_groups()
    skills = SkillRef.objects.all().filter(is_speciality=True)
    result_skills = []
    for s in skills:
        weight = 0
        if s.linked_to == root:
            weight = 1
        if weight > 0:
            result_skills.append({'skill': s.reference, 'data': s, 'weight': weight})
    return result_skills


def get_keywords():
    """ Get all keywords """
    from collector.models.character import Character
    everybody = Character.objects.all()
    keywords = []
    for someone in everybody:
        if someone.keyword != '':
            keywords.append(someone.keyword)
    return sorted(list(set(keywords)))
