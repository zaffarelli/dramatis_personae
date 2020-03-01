'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from datetime import datetime
from collector.utils import fs_fics7
import json
import math

import logging
logger = logging.getLogger(__name__)

class Combattant(models.Model):
    class Meta:
        abstract = True

    fights = models.PositiveIntegerField(default=0)
    victories = models.PositiveIntegerField(default=0)
    victory_rating = models.IntegerField(default=0)
    fencing_league = models.BooleanField(default=False)

    # OPTIMIZER COMBAT METHODS -------------------------------------------------
    def __init__(self, *args, **kwargs):
        super(Combattant,self).__init__(*args,**kwargs)
        self.round_data = {}

    def prepare_for_battle(self):
        self.round_data = {}
        self.round_data['Initiative'] = 0
        self.round_data['Narrative'] = []
        self.round_data['Narrative'].append('%s prepares for battle...'%(self.full_name))
        self.round_data['health_template'] = {
                'HEAD':{'SP':0, 'Wounds':{'Light':0,'Medium':0,'Severe':0}},
                'TORSO':{'SP':0, 'Wounds':{'Light':0,'Medium':0,'Severe':0}},
                'LEFT_ARM':{'SP':0, 'Wounds':{'Light':0,'Medium':0,'Severe':0}},
                'RIGHT_ARM':{'SP':0, 'Wounds':{'Light':0,'Medium':0,'Severe':0}},
                'LEFT_LEG':{'SP':0, 'Wounds':{'Light':0,'Medium':0,'Severe':0}},
                'RIGHT_LEG':{'SP':0, 'Wounds':{'Light':0,'Medium':0,'Severe':0}},
                'shield':{},
                'hit_points':self.SA_END,
                'hp_max':self.SA_END,
                'who':self.id,
                'color':self.color,
                'status':'OK'
        }
        a = self.get_armor()
        self.round_data['Armor'] = {'id':a.id,'name':a.armor_ref.reference,'SP':a.armor_ref.stopping_power,'ENC':a.armor_ref.encumbrance}
        if a.armor_ref.torso:
            self.round_data['health_template']['TORSO']['SP'] = a.armor_ref.stopping_power + self.SA_STA
        else:
            self.round_data['health_template']['TORSO']['SP'] = self.SA_STA
        if a.armor_ref.head:
            self.round_data['health_template']['HEAD']['SP'] = a.armor_ref.stopping_power + self.SA_STA
        else:
            self.round_data['health_template']['HEAD']['SP'] = self.SA_STA
        if a.armor_ref.left_arm:
            self.round_data['health_template']['LEFT_ARM']['SP'] = a.armor_ref.stopping_power + self.SA_STA
        else:
            self.round_data['health_template']['LEFT_ARM']['SP'] = self.SA_STA
        if a.armor_ref.right_arm:
            self.round_data['health_template']['RIGHT_ARM']['SP'] = a.armor_ref.stopping_power + self.SA_STA
        else:
            self.round_data['health_template']['RIGHT_ARM']['SP'] = self.SA_STA
        if a.armor_ref.left_leg:
            self.round_data['health_template']['LEFT_LEG']['SP'] = a.armor_ref.stopping_power + self.SA_STA
        else:
            self.round_data['health_template']['LEFT_LEG']['SP'] = self.SA_STA
        if a.armor_ref.right_leg:
            self.round_data['health_template']['RIGHT_LEG']['SP'] = a.armor_ref.stopping_power + self.SA_STA
        else:
            self.round_data['health_template']['RIGHT_LEG']['SP'] = self.SA_STA
        self.round_data['health_template']['circumstance_modifiers'] = 0

        penalty = self.round_data['Armor']['ENC']
        self.penalize(penalty)
        s = self.shield_set.first()
        if s!=None:
            self.round_data['shield'] = {'id':s.id,'name':s.shield_ref.reference,'min':s.shield_ref.protection_min,'max':s.shield_ref.protection_max}
            self.round_data['health_template']['shield']['charges'] = s.shield_ref.hits
            self.round_data['health_template']['shield']['min'] = s.shield_ref.protection_min
            self.round_data['health_template']['shield']['max'] = s.shield_ref.protection_max
        else:
            self.round_data['shield'] = None
            self.round_data['health_template']['shield']['charges'] = 0
            self.round_data['health_template']['shield']['min'] = 0
            self.round_data['health_template']['shield']['max'] = 0
        self.round_data['health_template']['expertise'] = 0
        self.check_expertise()
        return self.round_data

    def get_rd(self,txt):
        arr = txt.split('.')
        tab = self.round_data
        i = 0
        while i>len(arr):
            if arr[i] in tab:
                tab = tab[arr[i]]
            else:
                return None
            i += 1
        return tab

    def set_rd(self,txt,val):
        arr = txt.split('.')
        tab = self.round_data
        i = 0
        while i>len(arr):
            if arr[i] in tab:
                tab = tab[arr[i]]
            else:
                return None
            i += 1
        tab = val
        return tab

    @property
    def d12(self):
        return fs_fics7.roll(12)

    @property
    def open_d12(self):
        total = 0
        details = ""
        x = fs_fics7.roll(12)
        total = x
        if (x==1):
            details = "[1!]"
            y = fs_fics7.roll(12)
            total -= y
            details += " + (%d!) "%(y)
            while y==12:
                y = fs_fics7.roll(12)
                total -= y
                details += " + (%d!) "%(y)
        elif (x==12):
            details = "[12!]"
            y = fs_fics7.roll(12)
            total += y
            details += " + (%d!) "%(y)
            while y==12:
                y = fs_fics7.roll(12)
                total += y
                details += " + (%d!) "%(y)
        else:
            details = "["+str(x)+"!]"
        return total, details

    def localize_melee_attack(self,x):
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

    def get_skill(self,name):
        sk = self.skill_set.all().filter(skill_ref__reference=name).first()
        if sk==None:
            return -2
        else:
            return sk.value
        return None

    def get_weapon(self,name):
        we = self.weapon_set.all().filter(weapon_ref__category=name).order_by('-weapon_ref__damage_class')
        if we.count==0:
            return None
        else:
            return we.first()
        return None

    def get_armor(self):
        ar = self.armor_set.all().order_by('armor_ref__encumberance')
        if ar.count==0:
            return None
        else:
            return ar.first()
        return None

    def check_highest_bonus(self):
        b = 0
        x = self.round_data['health_template']['expertise_pool']
        s = math.floor(math.sqrt(x*2))
        if s*(s+1)/2 == x:
            b = s
        elif (s+1)*(s+2)/2 == x:
            b = s+1
        self.round_data['health_template']['expertise_pool'] -= b
        return b

    def choose_attack(self):
        self.round_data['name'] = self.full_name
        self.round_data['rid'] = self.rid
        self.round_data['id'] = self.id
        bon = self.check_highest_bonus()
        if bon > 5:
            natk = 3
        elif bon > 2:
            natk = 2
        natk = 1
        self.round_data['expertise_bonus'] = bon
        self.round_data['Number_of_attacks'] = natk
        w = self.get_weapon('MELEE')
        self.round_data['Weapon'] = {'id':w.id,'name':w.weapon_ref.reference,'DC':w.weapon_ref.damage_class,'WA':w.weapon_ref.weapon_accuracy}
        self.round_data['Attribute'] = {'name':'PA_REF','score':self.PA_REF}
        self.round_data['Defense_Attribute'] = {'name':'PA_AGI','score':self.PA_AGI}
        sk = self.skill_set.all().filter(skill_ref__reference='Melee').first()
        if sk==None:
            self.round_data['Skill'] = {'name':'Melee','score':-2}
        else:
            self.round_data['Skill'] = {'name':sk.skill_ref.reference,'score':sk.value}
        sk = self.skill_set.all().filter(skill_ref__reference='Dodge').first()
        if (sk==None):
            self.round_data['Dodge'] = {'name':'Dodge','score':0}
        else:
            self.round_data['Dodge'] = {'name':sk.skill_ref.reference,'score':sk.value}
        self.round_data['Narrative'].append('%s uses his/her <b>%s</b>...'%(self.full_name,self.round_data['Weapon']['name']))

    def check_expertise(self):
        expertise = 0
        manoeuvres_sets = self.beneficeaffliction_set.all().filter(benefice_affliction_ref__watermark__contains='melee_manoeuvres')
        for maneouvres_set in manoeuvres_sets:
            expertise += maneouvres_set.benefice_affliction_ref.value
        self.round_data['health_template']['expertise_pool'] = expertise
        self.round_data['health_template']['expertise'] = expertise

    def initiative_roll(self):
        if self.round_data['Number_of_attacks'] == 1:
            die, _ = self.open_d12
            self.round_data['Initiative'] = self.round_data['Skill']['score']+die
            self.round_data['Narrative'].append('%s rolls initiative for %d...'%(self.full_name,self.round_data['Initiative']))
            self.round_data['Narrative'].append('%s will have 1 action this round.'%(self.full_name))


    def roll_attack(self,target):
        overrun_bonus = 0
        die, detdie = self.open_d12
        die += self.round_data['expertise_bonus']
        self.round_data['attack_roll'] = self.round_data['Attribute']['score']+self.round_data['Skill']['score']+self.round_data['Weapon']['WA']-self.round_data['health_template']['circumstance_modifiers']+die
        self.round_data['attack_sequence'] = "Attacking: REF+Melee+WA-P+d12 --> "+str(self.round_data['Attribute']['score'])+"+"+str(self.round_data['Skill']['score'])+"+"+str(self.round_data['Weapon']['WA'])+"-"+str(self.round_data['health_template']['circumstance_modifiers'])+"+"+detdie+"=<b>"+str(self.round_data['attack_roll'])+"</b>"
        target.round_data['defender_dodge_roll'] = target.roll_dodge()
        self.round_data['Narrative'].append(self.round_data['attack_sequence'])
        target.round_data['Narrative'].append('Dodging %d'%(target.round_data['defender_dodge_roll']))
        overrun = self.round_data['attack_roll'] - target.round_data['defender_dodge_roll']
        if overrun>0:
            overrun_bonus = int(overrun / 3)
        if self.round_data['attack_roll']>target.round_data['defender_dodge_roll']:
            self.round_data['damage'] = fs_fics7.roll_dc(self.round_data['Weapon']['DC'])+self.SA_DMG+fs_fics7.roll_dc("%dD6"%(overrun_bonus))
            target.round_data['Narrative'].append('%s is hit by %s for <b>%d</b> hit points...'%(target.full_name,self.full_name,self.round_data['damage']))
            self.round_data['Narrative'].append('%s rolls for damage: %s + %d + %dD6 = <b>%d</b> hit points...'%(self.full_name,self.round_data['Weapon']['DC'],self.SA_DMG,overrun_bonus,self.round_data['damage']))
        else:
            self.round_data['text'] = "Missed..."
            self.round_data['damage'] = 0
            self.round_data['Narrative'].append('%s misses...'%(self.full_name))
            target.round_data['Narrative'].append('...')


    def shield_deflect(self,damage,source):
        true_damage = damage
        full_block = False
        effect_self = ''
        effect_source = ''
        if self.round_data['shield']==None:
            effect_self = 'No shield'
            effect_source = '...'
        else:
            if true_damage >= self.round_data['shield']['min']:
                if self.round_data['health_template']['shield']['charges']>0:
                    if true_damage <= self.round_data['shield']['max']:
                        true_damage = 0
                        full_block = True
                        effect_self = '%s attack is <b>blocked</b> by an energy shield...'%(source.full_name)
                        effect_source = 'Upcomming damage is %d'%(true_damage)
                        self.round_data['health_template']['shield']['charges'] -= 1
                    else:
                        true_damage = true_damage - self.round_data['shield']['max']
                        effect_self = '%s attack is <b>partially blocked</b> by an energy shield...'%(source.full_name)
                        effect_source = 'Upcomming damage is %d'%(true_damage)
                        self.round_data['health_template']['shield']['charges'] -= 1
                else:
                    true_damage = damage
                    effect_self = '%s attack is unblocked...'%(source.full_name)
                    effect_source = 'Upcomming damage is %d'%(true_damage)
        self.round_data['Narrative'].append(effect_self)
        source.round_data['Narrative'].append(effect_source)
        return true_damage, full_block

    def armor_deflect(self,damage,source,where):
        true_damage = damage
        effect_self = ''
        effect_source = ''
        true_damage = true_damage - self.round_data['health_template'][where]['SP']
        effect_self = '%s armor blocks %d damage...'%(self.full_name,self.round_data['health_template'][where]['SP'])
        effect_source = 'Upcomming damage is %d'%(true_damage)
        self.round_data['Narrative'].append(effect_self)
        source.round_data['Narrative'].append(effect_source)
        return true_damage

    def localize_damage(self,damage,source,where):
        true_damage = damage
        effect_self = ''
        effect_source = ''
        if (where == 'HEAD'):
            true_damage *= 2
            effect_self = '%s attack lands on the <b>%s</b> of %s for double damage!'%(source.full_name,where,self.full_name)
            effect_source = 'Upcomming damage is %d'%(true_damage)
        else:
            effect_self = '%s attack lands on the <b>%s</b> of %s...'%(source.full_name,where,self.full_name)
            effect_source = 'Upcomming damage is %d'%(true_damage)
        self.round_data['Narrative'].append(effect_self)
        source.round_data['Narrative'].append(effect_source)
        return true_damage

    def check_wounds(self,damage,where,source):
        had_a_light_wound = False
        had_a_medium_wound = False
        had_a_severe_wound = False
        effect_self = ''
        effect_source = ''
        if damage> self.SA_REC:
            self.round_data['health_template'][where]['Wounds']['Severe'] += 1
            effect_self = '%s suffers a new <i>severe wound</i> on the <b>%s</b>.'%(self.full_name,where)
            effect_source = '...'
            had_a_severe_wound = True
            self.penalize(4)
        elif damage> math.ceil(self.SA_REC/2):
            self.round_data['health_template'][where]['Wounds']['Medium'] += 1
            effect_self = '%s suffers a new <i>medium wound</i> on the <b>%s</b>.'%(self.full_name,where)
            effect_source = '...'
            had_a_medium_wound = True
            self.penalize(2)
        elif damage>0:
            self.round_data['health_template'][where]['Wounds']['Light'] += 1
            effect_self = '%s suffers a new <i>light wound</i> on the <b>%s</b>.'%(self.full_name,where)
            effect_source = '...'
            had_a_light_wound = True
        self.round_data['Narrative'].append(effect_self)
        source.round_data['Narrative'].append(effect_source)
        return had_a_light_wound, had_a_medium_wound, had_a_severe_wound

    def check_deathsave(self,source):
        is_dead = False
        effect_self = ''
        effect_source = ''
        die, detdie = self.open_d12
        score = die+self.SA_STU-self.round_data['health_template']['circumstance_modifiers']
        if score<10:
            self.round_data['health_template']['status'] = 'D'
            effect_self = 'Death check at DV 10 : %d  !'%(score)
            effect_source = 'Victory!!!'
        else:
            effect_self = 'Death check at passed (%d)  !'%(score)
            effect_source = '...'
        self.round_data['Narrative'].append(effect_self)
        source.round_data['Narrative'].append(effect_source)
        return is_dead


    def check_stun(self,source):
        is_stunned = False
        effect_self = ''
        effect_source = ''
        die, detdie = self.open_d12
        score = die+self.SA_STU-self.round_data['health_template']['circumstance_modifiers']
        if score<10:
            self.round_data['health_template']['status'] = 'S'
            self.penalize(10)
            effect_self = 'Stun check at DV 10 : %d  !'%(score)
            effect_source = 'Enemy is stunned!'
        else:
            effect_self = 'Stun check at DV 10 passed (%d)  !'%(score)
            effect_source = '...'
        self.round_data['Narrative'].append(effect_self)
        source.round_data['Narrative'].append(effect_source)
        return is_stunned


    def absorb_punishment(self,source):
        where = self.localize_melee_attack(self.d12)
        damage = source.round_data['damage']
        true_damage = 0
        if damage>0:
            true_damage = damage
            true_damage, full_block = self.shield_deflect(true_damage,source)
            if not full_block:
                true_damage = self.localize_damage(true_damage,source,where)
                true_damage = self.armor_deflect(true_damage,source,where)
            if true_damage < 0:
                true_damage = 1
            self.round_data['health_template']['hit_points'] -= true_damage
            l, m, s = self.check_wounds(true_damage,where,source)
            if m or s:
                self.check_stun(source)
            if s:
                self.check_deathsave(source)
            if true_damage>0:
                self.round_data['Narrative'].append('After protection checks, %s loses only <b>%s</b> hp...'%(self.full_name,true_damage))
                source.round_data['Narrative'].append('...')

    def penalize(self,x):
        self.round_data['health_template']['circumstance_modifiers'] += x
        #print("%s %d"%(self.full_name,self.round_data['health_template']['circumstance_modifiers']))

    def roll_dodge(self):
        die, detdie = self.open_d12
        die -= self.round_data['health_template']['circumstance_modifiers']
        dodge = self.round_data['Defense_Attribute']['score']+self.round_data['Dodge']['score']+die
        return dodge

    def check_death(self):
        check = self.round_data['health_template']['hit_points']<=0 or self.round_data['health_template']['status'] == 'D'
        if check:
            self.round_data['Narrative'].append('<b>%s is dead !!!</b>'%(self.full_name))
        return check



    # -------------------------------------------------------------------------
