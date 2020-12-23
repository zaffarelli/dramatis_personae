"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from datetime import datetime
from collector.utils import fs_fics7
from collector.models.avatar import Avatar
import json
import math

import logging

logger = logging.getLogger(__name__)



class Combattant(Avatar):
    class Meta:
        abstract = True

    fights = models.PositiveIntegerField(default=0)
    victories = models.PositiveIntegerField(default=0)
    victory_rating = models.IntegerField(default=0)
    fencing_league = models.BooleanField(default=False)

    # OPTIMIZER COMBAT METHODS -------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(Combattant, self).__init__(*args, **kwargs)
        self.round_data = {}

    def prepare_for_battle(self):
        a = self.get_armor()
        s = self.shield_set.first()
        w = self.get_weapon('MELEE')
        self.round_data = {
            'name': self.full_name,
            'rid': self.rid,
            'id': self.id,
            'initiative': 0,
            'multiattack_malus': 0,
            'number_of_attacks': 1,
            'max_attacks': 0,
            'narrative': [],
            'health_template': {
                'HEAD': {'SP': self.SA_STA, 'wounds': {'light': 0, 'medium': 0, 'severe': 0}},
                'TORSO': {'SP': self.SA_STA, 'wounds': {'light': 0, 'medium': 0, 'severe': 0}},
                'LEFT_ARM': {'SP': self.SA_STA, 'wounds': {'light': 0, 'medium': 0, 'severe': 0}},
                'RIGHT_ARM': {'SP': self.SA_STA, 'wounds': {'light': 0, 'medium': 0, 'severe': 0}},
                'LEFT_LEG': {'SP': self.SA_STA, 'wounds': {'light': 0, 'medium': 0, 'severe': 0}},
                'RIGHT_LEG': {'SP': self.SA_STA, 'wounds': {'light': 0, 'medium': 0, 'severe': 0}},
                'shield': {'charges': 0, 'min': 0, 'max': 0},
                'hit_points': self.SA_END,
                'hp_max': self.SA_END,
                'who': self.id,
                'color': self.color,
                'status': 'OK',
                'circumstance_modifiers': 0,
                'expertise': 0,
                'expertise_pool': 0,
                'expertise_bonus': 0,
            },
            'armor': {
                'id': a.id,
                'name': a.armor_ref.reference,
                'SP': a.armor_ref.stopping_power,
                'ENC': a.armor_ref.encumbrance,
            },
            'shield': {'id': 0, 'name': 'no shield', 'min': 0, 'max': 0, 'charges': 0},
            'weapon': {'id': w.id, 'name': w.weapon_ref.reference, 'DC': w.weapon_ref.damage_class,
                       'WA': w.weapon_ref.weapon_accuracy},
            'REF': 0,
            'AGI': 0,
            'melee': 0,
            'dodge': 0,
        }
        self.poke('REF', self.PA_REF)
        self.poke('AGI', self.PA_AGI)
        sk = self.skill_set.all().filter(skill_ref__reference='Melee').first()
        if sk == None:
            self.poke('melee', -2)
        else:
            self.poke('melee', sk.value)
        sk = self.skill_set.all().filter(skill_ref__reference='Dodge').first()
        if sk == None:
            self.poke('dodge', -2)
        else:
            self.poke('dodge', sk.value)

        self.tell('<u>%s</u> prepares for battle...' % (self.full_name))
        if a.armor_ref.torso:
            self.poke('health_template.TORSO.SP', a.armor_ref.stopping_power + self.SA_STA)
        if a.armor_ref.head:
            self.poke('health_template.HEAD.SP', a.armor_ref.stopping_power + self.SA_STA)
        if a.armor_ref.left_arm:
            self.poke('health_template.LEFT_ARM.SP', a.armor_ref.stopping_power + self.SA_STA)
        if a.armor_ref.right_arm:
            self.poke('health_template.RIGHT_ARM.SP', a.armor_ref.stopping_power + self.SA_STA)
        if a.armor_ref.left_leg:
            self.poke('health_template.LEFT_LEG.SP', a.armor_ref.stopping_power + self.SA_STA)
        if a.armor_ref.right_leg:
            self.poke('health_template.RIGHT_LEG.SP', a.armor_ref.stopping_power + self.SA_STA)
        penalty = self.peek('armor.ENC')
        self.poke('weapon.id', w.id)
        self.poke('weapon.name', w.weapon_ref.reference)
        self.poke('weapon.DC', w.weapon_ref.damage_class)
        self.poke('weapon.WA', w.weapon_ref.weapon_accuracy)
        self.penalize(penalty)
        if s != None:
            self.poke('shield.id', s.id)
            self.poke('shield.name', s.shield_ref.reference)
            self.poke('shield.min', s.shield_ref.protection_min)
            self.poke('shield.max', s.shield_ref.protection_max)
            self.poke('health_template.shield.charges', s.shield_ref.hits)
            self.poke('health_template.shield.min', s.shield_ref.protection_min)
            self.poke('health_template.shield.max', s.shield_ref.protection_max)

        self.check_expertise()
        self.tell(
            '<u>%s</u> uses his/her <b>%s</b>, granting himself/herself an accuracy bonus of <b>%d</b>, for a damage class of <b>%s</b>.' % (
            self.full_name, self.peek('weapon.name'), self.peek('weapon.WA'), self.peek('weapon.DC')))
        return self.round_data

    def check_stunrecover(self, target):
        x = self.d12
        if x + self.SA_REC > 15:
            self.poke('round_data.health_template.status', 'OK')
            self.tell('%s recovers from stunned status.' % (self.full_name))
            target.tell('...')

    def get_skill(self, name):
        sk = self.skill_set.all().filter(skill_ref__reference=name).first()
        if sk == None:
            return -2
        else:
            return sk.value
        return None

    def get_weapon(self, name):
        we = self.weapon_set.all().filter(weapon_ref__category=name).order_by('-weapon_ref__damage_class')
        if we.count == 0:
            return None
        else:
            return we.first()
        return None

    def get_armor(self):
        ar = self.armor_set.all().order_by('armor_ref__encumberance')
        if ar.count == 0:
            return None
        else:
            return ar.first()
        return None

    def check_highest_bonus(self):
        b = 0
        x = self.peek('health_template.expertise_pool')
        s = math.floor(math.sqrt(x * 2))
        if s * (s + 1) / 2 == x:
            b = s
        elif (s + 1) * (s + 2) / 2 == x:
            b = s + 1
        self.poke_inc('health_template.expertise_pool', -b)
        return b

    def choose_attack(self, target):
        bon = self.check_highest_bonus()
        if bon > 0:
            self.tell("<u>%s</u> has an expertise bonus of <i>+%d</i>." % (self.full_name, bon))
            target.tell("")
        self.poke('health_template.expertise_bonus', bon)
        natk = 1
        if bon >= 4:
            natk = 3
        elif bon >= 2:
            natk = 2
        status = self.peek('health_template.status')
        if status == 'S':
            self.check_stunrecover(target)

        self.poke('number_of_attacks', natk)
        self.poke('max_attacks', natk)

    def check_expertise(self):
        expertise = 0
        manoeuvres_sets = self.beneficeaffliction_set.all().filter(
            benefice_affliction_ref__watermark__contains='melee_manoeuvres')
        for manoeuvres_set in manoeuvres_sets:
            expertise += manoeuvres_set.benefice_affliction_ref.value
        self.poke('health_template.expertise_pool', expertise)
        self.poke('health_template.expertise', expertise)
        self.tell("<u>%s</u> has an expertise of %d on melee manoeuvres." % (self.full_name, expertise))

    def initiative_roll(self, rnd):
        die, _ = self.open_d12
        self.poke('initiative', self.peek('melee') + die)
        self.tell('<u>%s</u> rolls initiative for %d...' % (self.full_name, self.peek('initiative')))
        self.tell('<u>%s</u> will have %d action this round.' % (self.full_name, self.peek('number_of_attacks')))

    def choose_parry(self):
        if self.round_data['number_of_attacks'] > 0:
            if self.round_data['max_attacks'] == 3:
                return self.d12 < 8
            elif self.round_data['max_attacks'] == 2:
                return self.d12 < 6
            else:
                return self.d12 < 4
        else:
            return False

    def roll_attack(self, target):
        if self.peek('number_of_attacks') > 0:
            bon = self.check_highest_bonus()
            if bon > 0:
                self.tell("<u>%s</u> has a bonus of <b>+%d</b>." % (self.full_name, bon))
                target.tell("")
            self.poke('health_template.expertise_bonus', bon)
            overrun_bonus = 0
            self.poke('multiattack_malus', (self.peek('max_attacks') - 1) * 3)
            die, detdie = self.open_d12
            self.poke('attack_roll', self.peek('REF') + self.peek('melee') + self.peek('weapon.WA') - self.peek(
                'health_template.circumstance_modifiers') - self.peek('multiattack_malus') + self.peek(
                'health_template.expertise_bonus') + die)
            sum = self.peek('REF') + self.peek('melee') + self.peek('weapon.WA') - self.peek(
                'health_template.circumstance_modifiers') - self.peek('multiattack_malus') + self.peek(
                'health_template.expertise_bonus')

            attk_order = ['first', 'second', 'third'][self.peek('max_attacks') - self.peek('number_of_attacks')]
            x = f"{self.peek('REF')} + {self.peek('melee')} + {self.peek('weapon.WA')} - {self.peek('health_template.circumstance_modifiers')} - {self.peek('multiattack_malus')} + {self.peek('health_template.expertise_bonus')} = "
            self.poke('attack_sequence',
                      "<u>" + self.full_name + "</u> <b>" + attk_order + " attack !<br/></b> REF + Melee + WA - CM - MA + EX -> " + x + str(
                          sum) + "+" + detdie + "=<b>" + str(self.peek('attack_roll')) + "</b>")
            self.tell(self.peek('attack_sequence'))
            tgt_parry = target.choose_parry()
            if tgt_parry:
                target.poke('defender_dodge_roll', target.roll_parry())
                target.tell('Parrying %d' % (target.peek('defender_dodge_roll')))
                overrun = self.peek('attack_roll') - target.peek('defender_dodge_roll')
                target.poke_inc('number_of_attacks', -1)
            else:
                target.poke('defender_dodge_roll', target.roll_dodge())
                target.tell('Dodging %d' % (target.peek('defender_dodge_roll')))
                overrun = self.peek('attack_roll') - target.peek('defender_dodge_roll')
            if overrun > 0:
                overrun_bonus = int(overrun / 3)
            if self.peek('attack_roll') > target.peek('defender_dodge_roll'):
                self.poke('damage', fs_fics7.roll_dc(self.peek('weapon.DC')) + self.SA_DMG + fs_fics7.roll_dc(
                    "%dD6" % (overrun_bonus)))
                target.tell('<u>%s</u> is hit by %s for <b>%d</b> hit points...' % (
                target.full_name, self.full_name, self.peek('damage')))
                self.tell('<u>%s</u> rolls for damage: %s + %d + %dD6 = <b>%d</b> hit points...' % (
                self.full_name, self.peek('weapon.DC'), self.SA_DMG, overrun_bonus, self.peek('damage')))
            else:
                self.poke('damage', 0)
                if tgt_parry:
                    self.tell("For Pancreator's sake!")
                    target.tell('<u>%s</u> block the attack with a parry action.' % (target.full_name))
                else:
                    self.tell('<u>%s</u> misses...' % (self.full_name))
                    target.tell('...')
            self.poke_inc('number_of_attacks', -1)
            self.poke('health_template.expertise_bonus', 0)
            self.tell(f"Remaining actions: {self.peek('number_of_attacks')}")
            target.tell("")
        else:
            self.tell('No more attacks for <u>%s</u>' % (self.full_name))
            target.tell('<u>%s</u> seems to be overrun...' % (self.full_name))
            self.poke('damage', 0)

    def shield_deflect(self, damage, source):
        true_damage = damage
        full_block = False
        effect_self = ''
        effect_source = ''
        if self.peek('shield') == None:
            effect_self = 'No shield'
            effect_source = '...'
        else:
            if true_damage >= self.peek('health_template.shield.min'):
                if self.peek('health_template.shield.charges') > 0:
                    if true_damage <= self.peek('health_template.shield.max'):
                        true_damage = 0
                        full_block = True
                        effect_self = '<u>%s</u> attack is <b>blocked</b> by an energy shield...' % (source.full_name)
                        effect_source = 'After shield block, upcomming damage is %d' % (true_damage)
                        self.poke_inc('health_template.shield.charges', -1)
                    else:
                        true_damage = true_damage - self.peek('health_template.shield.max')
                        effect_self = '<u>%s</u> attack is <b>partially blocked</b> by an energy shield...' % (
                            source.full_name)
                        effect_source = 'After shield block, upcomming damage is %d' % (true_damage)
                        self.poke_inc('health_template.shield.charges', -1)
                else:
                    true_damage = damage
                    effect_self = '<u>%s</u> attack is unblocked...' % (source.full_name)
                    effect_source = 'After shield block, upcomming damage is %d' % (true_damage)
        self.tell(effect_self)
        source.tell(effect_source)
        return true_damage, full_block

    def armor_deflect(self, damage, source, where):
        true_damage = damage
        effect_self = ''
        effect_source = ''
        true_damage = true_damage - self.peek('health_template.' + where + '.SP')
        effect_self = '<u>%s</u> armor blocks %d damage...' % (
        self.full_name, self.peek('health_template.' + where + '.SP'))
        effect_source = 'After armor block, upcomming damage is %d' % (true_damage)
        self.tell(effect_self)
        source.tell(effect_source)
        return true_damage

    def localize_damage(self, damage, source, where):
        true_damage = damage
        effect_self = ''
        effect_source = ''
        if (where == 'HEAD'):
            true_damage *= 2
            effect_self = '<u>%s</u> attack lands on the <b>%s</b> of <u>%s</u> for double damage!' % (
            source.full_name, where, self.full_name)
            effect_source = 'After localisation check, upcomming damage is %d' % (true_damage)
        else:
            effect_self = '<u>%s</u> attack lands on the <b>%s</b> of <u>%s</u>...' % (
            source.full_name, where, self.full_name)
            effect_source = 'After localisation check, upcomming damage is %d' % (true_damage)
        self.tell(effect_self)
        source.tell(effect_source)
        return true_damage

    def check_wounds(self, damage, where, source):
        had_a_light_wound = False
        had_a_medium_wound = False
        had_a_severe_wound = False
        effect_self = ''
        effect_source = ''
        if damage > self.SA_REC:
            self.poke_inc('health_template.' + where + '.wounds.severe', 1)
            effect_self = '<u>%s</u> suffers a new <i>severe wound</i> on the <b>%s</b>.' % (self.full_name, where)
            effect_source = '...'
            had_a_severe_wound = True
            self.penalize(4)
        elif damage > math.ceil(self.SA_REC / 2):
            self.poke_inc('health_template.' + where + '.wounds.medium', 1)
            effect_self = '<u>%s</u> suffers a new <i>medium wound</i> on the <b>%s</b>.' % (self.full_name, where)
            effect_source = '...'
            had_a_medium_wound = True
            self.penalize(2)
        elif damage > 0:
            self.poke_inc('health_template.' + where + '.wounds.light', 1)
            effect_self = '<u>%s</u> suffers a new <i>light wound</i> on the <b>%s</b>.' % (self.full_name, where)
            effect_source = '...'
            had_a_light_wound = True
        self.tell(effect_self)
        source.tell(effect_source)
        return had_a_light_wound, had_a_medium_wound, had_a_severe_wound

    def check_deathsave(self, source):
        is_dead = False
        effect_self = ''
        effect_source = ''
        die, detdie = self.open_d12
        score = die + self.SA_STU  # -self.round_data['health_template']['circumstance_modifiers']
        if score < 10:
            self.poke('health_template.status', 'D')
            effect_self = 'Death check at DV 10 : %d!' % (score)
            effect_source = 'Victory!!!'
        else:
            effect_self = 'Death check at DV 10 passed : %d !' % (score)
            effect_source = '...'
        self.tell(effect_self)
        source.tell(effect_source)
        return is_dead

    def check_stunsave(self, source):
        is_stunned = False
        effect_self = ''
        effect_source = ''
        die, detdie = self.open_d12
        score = die + self.SA_STU  # -self.round_data['health_template']['circumstance_modifiers']
        if score < 10:
            self.poke('health_template.status', 'S')
            self.penalize(10)
            effect_self = 'Stun check at DV 10 : %d  !' % (score)
            effect_source = 'Enemy is stunned!'
        else:
            effect_self = 'Stun check at DV 10 passed (%d)  !' % (score)
            effect_source = '...'
        self.tell(effect_self)
        source.tell(effect_source)
        return is_stunned

    def absorb_punishment(self, source):
        where = self.localize_melee_attack(self.d12)
        damage = source.peek('damage')
        true_damage = 0
        if damage > 0:
            true_damage = damage
            true_damage, full_block = self.shield_deflect(true_damage, source)
            if not full_block:
                true_damage = self.localize_damage(true_damage, source, where)
                true_damage = self.armor_deflect(true_damage, source, where)
            if true_damage < 0:
                true_damage = 1
            self.poke_inc('health_template.hit_points', -true_damage)
            l, m, s = self.check_wounds(true_damage, where, source)
            if m or s:
                self.check_stunsave(source)
            if s:
                self.check_deathsave(source)
            if true_damage > 0:
                self.tell(
                    'After protection checks, <u>%s</u> loses only <b>%s</b> hp...' % (self.full_name, true_damage))
                source.tell('...')

    def penalize(self, x):
        self.round_data['health_template']['circumstance_modifiers'] += x
        # print("%s %d"%(self.full_name,self.round_data['health_template']['circumstance_modifiers']))

    def roll_dodge(self):
        die, detdie = self.open_d12
        die -= self.peek('health_template.circumstance_modifiers')
        dodge = self.peek('AGI') + self.peek('dodge') + die
        return dodge

    def roll_parry(self):
        if self.peek('max_attacks') == 1:
            self.poke('multiattack_malus', 8)
        else:
            self.poke('multiattack_malus', (self.peek('max_attacks') - 1) * 3)
        die, detdie = self.open_d12
        die += 2
        die -= self.peek('multiattack_malus')
        die -= self.peek('health_template.circumstance_modifiers')
        parry = self.peek('REF') + self.peek('melee') + die
        return parry

    def check_death(self, source):
        check = self.peek('health_template.hit_points') <= 0 or self.peek('health_template.status') == 'D'
        if check:
            self.tell('<b>%s is dead !!!</b>' % (self.full_name))
            source.tell('VICTORY! <b>%s is dead !!!</b>' % (self.full_name))
        return check

    # --- Utilities functions -------------------------------------------------
    def tell(self, txt):
        self.round_data['narrative'].append(txt)

    def peek(self, txt):
        map = txt.split('.')
        tab = self.round_data
        for k in map:
            tab = tab[k]
        return tab

    def poke(self, txt, val):
        map = txt.split('.')
        tab = self.round_data
        for k in map[:-1]:
            tab = tab.setdefault(k, {})
        tab[map[-1]] = val
        return tab

    def poke_inc(self, txt, val):
        x = self.peek(txt)
        self.poke(txt, x + val)

    @property
    def d12(self):
        return fs_fics7.roll(12)

    @property
    def open_d12(self):
        total = 0
        details = ""
        x = fs_fics7.roll(12)
        total = x
        if (x == 1):
            details = "[1!]"
            y = fs_fics7.roll(12)
            total -= y
            details += " + (%d!) " % (y)
            while y == 12:
                y = fs_fics7.roll(12)
                total -= y
                details += " + (%d!) " % (y)
        elif (x == 12):
            details = "[12!]"
            y = fs_fics7.roll(12)
            total += y
            details += " + (%d!) " % (y)
            while y == 12:
                y = fs_fics7.roll(12)
                total += y
                details += " + (%d!) " % (y)
        else:
            details = "[" + str(x) + "!]"
        return total, details

    def localize_melee_attack(self, x):
        loc = {
            1: 'RIGHT_LEG',
            2: 'LEFT_LEG',
            3: 'RIGHT_ARM',
            4: 'RIGHT_ARM',
            5: 'LEFT_ARM',
            6: 'LEFT_ARM',
            7: 'TORSO',
            8: 'TORSO',
            9: 'TORSO',
            10: 'TORSO',
            11: 'HEAD',
            12: 'HEAD'
        }
        return loc[x]

    def fix(self, conf=None):
        super().fix(conf)