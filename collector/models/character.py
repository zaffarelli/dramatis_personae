"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
import hashlib
from scenarist.models.epics import Epic
from collector.models.fics_models import Specie
from collector.models.combattant import Combattant
from collector.utils import fs_fics7

import logging

logger = logging.getLogger(__name__)


class Character(Combattant):
    class Meta:
        ordering = ['full_name']

    pagenum = 0
    full_name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200, blank=True, null=True, default='')
    rid = models.CharField(max_length=200, default='none')
    alliance = models.CharField(max_length=200, blank=True, default='')
    faction = models.CharField(max_length=200, blank=True, default='')
    alliancehash = models.CharField(max_length=200, blank=True, default='none')
    player = models.CharField(max_length=200, default='', blank=True)
    specie = models.ForeignKey(Specie, null=True, default=31, blank=True,
                               on_delete=models.SET_NULL)
    birthdate = models.IntegerField(default=0)
    gender = models.CharField(max_length=30, default='female')
    native_fief = models.CharField(max_length=200, default='none', blank=True)
    caste = models.CharField(max_length=100, default='Freefolk', blank=True)
    rank = models.CharField(max_length=100, default='', blank=True)
    height = models.IntegerField(default=150)
    weight = models.IntegerField(default=50)
    narrative = models.TextField(default='', blank=True)
    buildlog = models.TextField(default='', blank=True)
    entrance = models.CharField(max_length=100, default='', blank=True)
    keyword = models.CharField(max_length=32, blank=True, default='new')
    stars = models.CharField(max_length=256, blank=True, default='')
    importance = models.PositiveIntegerField(default=1)
    PA_STR = models.PositiveIntegerField(default=1)
    PA_CON = models.PositiveIntegerField(default=1)
    PA_BOD = models.PositiveIntegerField(default=1)
    PA_MOV = models.PositiveIntegerField(default=1)
    PA_INT = models.PositiveIntegerField(default=1)
    PA_WIL = models.PositiveIntegerField(default=1)
    PA_TEM = models.PositiveIntegerField(default=1)
    PA_PRE = models.PositiveIntegerField(default=1)
    PA_REF = models.PositiveIntegerField(default=1)
    PA_TEC = models.PositiveIntegerField(default=1)
    PA_AGI = models.PositiveIntegerField(default=1)
    PA_AWA = models.PositiveIntegerField(default=1)
    pub_date = models.DateTimeField('Date published', default=datetime.now)
    SA_REC = models.IntegerField(default=0)
    SA_STA = models.IntegerField(default=0)
    SA_END = models.IntegerField(default=0)
    SA_STU = models.IntegerField(default=0)
    SA_RES = models.IntegerField(default=0)
    SA_DMG = models.IntegerField(default=0)
    SA_TOL = models.IntegerField(default=0)
    SA_HUM = models.IntegerField(default=0)
    SA_PAS = models.IntegerField(default=0)
    SA_WYR = models.IntegerField(default=0)
    SA_SPD = models.IntegerField(default=0)
    SA_RUN = models.IntegerField(default=0)
    PA_TOTAL = models.IntegerField(default=0)
    SK_TOTAL = models.IntegerField(default=0)
    TA_TOTAL = models.IntegerField(default=0)
    BC_TOTAL = models.IntegerField(default=0)
    BA_TOTAL = models.IntegerField(default=0)
    weapon_cost = models.IntegerField(default=0)
    armor_cost = models.IntegerField(default=0)
    shield_cost = models.IntegerField(default=0)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    gm_shortcuts = models.TextField(default='', blank=True)
    gm_shortcuts_pdf = models.TextField(default='', blank=True)
    age = models.IntegerField(default=0)
    OCC_LVL = models.PositiveIntegerField(default=0)
    OCC_DRK = models.PositiveIntegerField(default=0)
    occult = models.CharField(max_length=50, default='', blank=True)
    challenge = models.TextField(default='', blank=True)
    todo_list = models.TextField(default='', blank=True)
    # is_exportable = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    is_dead = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_partial = models.BooleanField(default=True)
    spotlight = models.BooleanField(default=False)
    use_history_creation = models.BooleanField(default=False)
    use_only_entrance = models.BooleanField(default=False)
    epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
    picture = models.CharField(max_length=512, blank=True,
                               default='https://drive.google.com/open?id=15hdubdMt1t_deSXkbg9dsAjWi5tZwMU0')
    alliance_picture = models.CharField(max_length=256, blank=True, default='')
    onsave_reroll_attributes = models.BooleanField(default=False)
    onsave_reroll_skills = models.BooleanField(default=False)
    lifepath_total = models.IntegerField(default=0)
    balanced = models.BooleanField(default=False)
    historical_figure = models.BooleanField(default=False)
    nameless = models.BooleanField(default=False)
    color = models.CharField(max_length=20, blank=True, default='#CCCCCC')
    skills_options = []
    ba_options = []
    bc_options = []
    skills_options_not = []
    ba_options_not = []
    bc_options_not = []
    AP_tod_pool = 0
    OP_tod_pool = 0
    WP_tod_pool = 0
    weapon_options = []
    weapon_options_not = []
    armor_options = []
    armor_options_not = []
    shield_options = []
    shield_options_not = []

    @property
    def info_str(self):
        return self.get_pa("PA_STR")

    @property
    def info_con(self):
        return self.get_pa("PA_CON")

    @property
    def info_bod(self):
        return self.get_pa("PA_BOD")

    @property
    def info_mov(self):
        return self.get_pa("PA_MOV")

    @property
    def info_int(self):
        return self.get_pa("PA_INT")

    @property
    def info_wil(self):
        return self.get_pa("PA_WIL")

    @property
    def info_tem(self):
        return self.get_pa("PA_TEM")

    @property
    def info_pre(self):
        return self.get_pa("PA_PRE")

    @property
    def info_tec(self):
        return self.get_pa("PA_TEC")

    @property
    def info_ref(self):
        return self.get_pa("PA_REF")

    @property
    def info_agi(self):
        return self.get_pa("PA_AGI")

    @property
    def info_awa(self):
        return self.get_pa("PA_AWA")

    @property
    def info_lvl(self):
        return self.get_pa("OCC_LVL")

    @property
    def info_drk(self):
        return self.get_pa("OCC_DRK")

    def get_absolute_url(self):
        return reverse('view_character', kwargs={'pk': self.pk})

    def get_pa(self, str):
        context = {}
        context["attribute"] = str
        context["value"] = getattr(self, str)
        context["id"] = self.id
        return context

    def rebuild_from_lifepath(self):
        """ Historical Creation """
        self.buildlog = ''
        from collector.models.character_custo import CharacterCusto
        found_custo = CharacterCusto.objects.filter(character=self).first()
        if found_custo is None:
            self.charactercusto = CharacterCusto.objects.create(character=self)
        self.resetPA()
        self.purgeSkills()
        self.purgeBC()
        self.purgeBA()
        self.purgeWeapons()
        self.purgeArmors()
        self.purgeShields()
        self.purgeRituals()
        self.purgeTalents()
        self.AP_tod_pool = 0
        self.OP_tod_pool = 0
        self.WP_tod_pool = 0
        self.lifepath_total = 0
        bl = []
        TOD_REP = {
            'RA': 0,
            'UP': 0,
            'AP': 0,
            'EC': 0,
            'TO': 0,
            'WB': 0,
        }
        for tod in self.tourofduty_set.all():
            AP, OP, WP = tod.push(self)
            self.AP_tod_pool += AP
            self.OP_tod_pool += OP
            self.OP_tod_pool += WP
            self.WP_tod_pool += WP
            self.lifepath_total += tod.tour_of_duty_ref.value
            if (tod.tour_of_duty_ref.category == '0' or tod.tour_of_duty_ref.category == '5'):
                TOD_REP['RA'] += tod.tour_of_duty_ref.value
            elif (tod.tour_of_duty_ref.category == '10'):
                TOD_REP['UP'] += tod.tour_of_duty_ref.value
            elif (tod.tour_of_duty_ref.category == '20'):
                TOD_REP['AP'] += tod.tour_of_duty_ref.value
            elif (tod.tour_of_duty_ref.category == '30'):
                TOD_REP['EC'] += tod.tour_of_duty_ref.value
            elif (tod.tour_of_duty_ref.category == '40'):
                TOD_REP['TO'] += tod.tour_of_duty_ref.value
            elif (tod.tour_of_duty_ref.category == '50'):
                TOD_REP['WB'] += tod.tour_of_duty_ref.value
        if self.charactercusto:
            self.charactercusto.comment = self.full_name
            self.charactercusto.push(self)
            self.charactercusto.save()

        PA_TOTAL = self.sumPA
        PO_TOTAL = 0
        for s in self.skill_set.all():
            if s.skill_ref.is_root == False:
                PO_TOTAL += s.value
        BA_TOTAL = 0
        for ba in self.beneficeaffliction_set.all():
            BA_TOTAL += ba.benefice_affliction_ref.value
        BC_TOTAL = 0
        for bc in self.blessingcurse_set.all():
            BC_TOTAL += bc.blessing_curse_ref.value

        bl.append("")
        bl.append("Tour Summary:")
        bl.append("- APx3+OP+BA+BC... " + str(PA_TOTAL * 3 + PO_TOTAL + BA_TOTAL + BC_TOTAL))
        bl.append("- WP.............. " + str(self.WP_tod_pool))
        bl.append("- Value........... " + str(self.charactercusto.value))
        bl.append("- Lifepath ....... " + str(self.lifepath_total))
        bl.append("- Repartition .... " + str(TOD_REP))
        fs_fics7.check_secondary_attributes(self)
        self.charactercusto.save()
        self.prepareDisplay()
        self.handleWildcards()
        self.add_missing_root_skills()
        self.resetTotal()
        self.balanced = (self.lifepath_total == self.OP) and (self.OP > 0)
        self.buildlog = "\n".join(bl)
        if self.player != '':
            self.balanced = True
        if self.color == '#CCCCCC':
            d = lambda x: fs_fics7.roll(x) - 1
            self.color = '#%01X%01X%01X%01X%01X%01X' % (d(8) + 4, d(16), d(8) + 4, d(16), d(8) + 4, d(16))

    def prepareDisplay(self):
        self.refresh_skills_options()
        self.refresh_options("ba_options", "ba_options_not", self.charactercusto.beneficeafflictioncusto_set.all(),
                             "benefice_affliction_ref", "BeneficeAfflictionRef")
        self.refresh_options("bc_options", "bc_options_not", self.charactercusto.blessingcursecusto_set.all(),
                             "blessing_curse_ref", "BlessingCurseRef")
        self.refresh_options("weapon_options", "weapon_options_not", self.charactercusto.weaponcusto_set.all(),
                             "weapon_ref", "WeaponRef")
        self.refresh_options("shield_options", "shield_options_not", self.charactercusto.shieldcusto_set.all(),
                             "shield_ref", "ShieldRef")
        self.refresh_options("armor_options", "armor_options_not", self.charactercusto.armorcusto_set.all(),
                             "armor_ref", "ArmorRef")
        self.refresh_options("ritual_options", "ritual_options_not", self.charactercusto.ritualcusto_set.all(),
                             "ritual_ref", "RitualRef")
        # self.preparePADisplay()

    def handleWildcards(self):
        pass

    def rebuild_free_form(self):
        """ Freeform Creation """
        # self.resetTotal()
        # if self.onsave_reroll_attributes:
        #     fs_fics7.check_primary_attributes(self)
        #     fs_fics7.check_secondary_attributes(self)
        # if self.onsave_reroll_skills:
        #     fs_fics7.check_skills(self)
        # else:
        self.add_missing_root_skills()
        self.resetTotal()

    def fix(self, conf=None):
        """ Check / calculate other characteristics """
        logger.info('Fixing ........: %s' % (self.full_name))
        if not conf:
            if self.birthdate < 1000:
                self.birthdate = 5017 - self.birthdate
                self.age = 5017 - self.birthdate
        else:
            if self.birthdate < 1000:
                self.birthdate = conf.epic.era - self.birthdate
                self.age = conf.epic.era - self.birthdate
        # NPC fix
        if self.player == 'none':
            self.player = ''
        if self.use_history_creation:
            self.rebuild_from_lifepath()
        else:
            self.rebuild_free_form()
        self.calculateShortcuts()
        if self.PA_BOD != 0:
            if self.height == 0:
                if "urthish" in self.specie.species.lower():
                    self.height = 145 + 2.39473 * (self.PA_BOD / 2 + self.PA_STR / 2 + self.PA_CON + 2)
                    if self.gender == 'male':
                        self.weight = self.height / (2.98 - 0.0336 * (self.PA_BOD + self.PA_CON))
                    else:
                        self.weight = self.height / (3.09 - 0.02975 * (self.PA_BOD + self.PA_CON))
                    if self.PA_MOV != self.PA_CON:
                        self.weight *= 1 + (self.PA_CON - self.PA_MOV) * 0.1
                    logger.info("Height/Weight Experiment 1: %s --> %0.2f %0.2f BODY:%d CONSTITUTION:%d" % (
                        self.full_name, self.height, self.weight, self.PA_BOD, self.PA_CON))
        # self.is_exportable = True #self.check_exportable()
        self.update_challenge()
        self.check_todo_list()
        logger.debug('Done fixing ...: %s' % (self.full_name))

    def check_todo_list(self):
        pass
        # self.todo_list = ""
        # tsk = []
        # if self.use_history_creation:
        #     for tod in self.tourofduty_set.all():
        #         tsk = "%s - %s"%()
        # self.todo_list = "\n".join(tsk)

    def update_challenge(self):
        res = ''
        res += '<i class="fas fa-th-large" title="primary attributes"></i>%d ' % (self.AP)
        res += '<i class="fas fa-th-list" title="skills"></i> %d ' % (self.SK_TOTAL)
        res += '<i class="fas fa-th" title="talents"></i> %d ' % (self.TA_TOTAL + self.BC_TOTAL + self.BA_TOTAL)
        res += '<i class="fas fa-star" title="wildcards"></i> %d ' % (self.WP_tod_pool)
        res += '<i class="fas fa-newspaper" title="OP challenge"></i> %d/%d' % (self.OP, self.lifepath_total)
        self.challenge = res

    def calculateShortcuts(self):
        """ Calculate shortcuts for the avatar skills. A shortcut appears if skill.value>0  """
        shortcuts = []
        shortcuts_pdf = []
        skills = self.skill_set.all()
        for s in skills:
            sc, pdf = fs_fics7.check_gm_shortcuts(self, s)
            if sc != '':
                shortcuts.append(sc)
                shortcuts_pdf.append("{:s}:{:s} ({:d})".format(pdf['rationale'], pdf['label'], pdf['score']))
        self.gm_shortcuts = ''.join(shortcuts)
        # print(shortcuts_pdf)
        self.gm_shortcuts_pdf = ', '.join(shortcuts_pdf)

    def refresh_options(self, options, options_not, custo_set, ref_type, refclass):
        """ Refresh options / options_not global engine """
        # from collector.models.weapon import WeaponRef
        # from collector.models.shield import ShieldRef
        # from collector.models.armor import ArmorRef
        # from collector.models.benefice_affliction import BeneficeAfflictionRef
        # from collector.models.blessing_curse import BlessingCurseRef
        # from collector.models.ritual import RitualRef
        o = []
        o_n = []
        custo_items = custo_set
        custo_ref_items = []
        for item in custo_items:
            custo_ref_items.append(getattr(item, ref_type))
        all_items = eval(refclass).objects.all()
        for item in all_items:
            if item in custo_ref_items:
                o_n.append(item)
            else:
                o.append(item)

        setattr(self, options, o)
        setattr(self, options_not, o_n)

    def refresh_skills_options(self):
        """ This one is special: it only reflects skills that are not in the character """
        from collector.models.skill import SkillRef
        self.skills_options = []
        self.skills_options_not = []
        ss = self.skill_set.all()
        sr = []
        for x in ss:
            sr.append(x.skill_ref)
        all = SkillRef.objects.all().exclude(is_root=True).order_by('is_speciality', 'is_wildcard', 'reference')
        for s in all:
            if s in sr:
                self.skills_options_not.append(s)
            else:
                self.skills_options.append(s)

    def add_or_update_skill(self, askill, modifier=0, stack=False):
        from collector.models.skill import Skill
        found_skill = self.skill_set.all().filter(skill_ref=askill).first()
        if found_skill:
            if modifier == 0:
                found_skill.value += 1
            else:
                found_skill.value += modifier
            found_skill.save()
            return found_skill
        else:
            skill = Skill()
            skill.character = self
            skill.skill_ref = askill
            if modifier == 0:
                skill.value = 1
            else:
                if stack:
                    skill.value += modifier
                else:
                    skill.value = modifier
            skill.save()
        return skill

    def remove_or_update_skill(self, askill, modifier=0, stack=False):
        # from collector.models.skill import Skill
        found_skill = self.skill_set.all().filter(skill_ref=askill).first()
        if found_skill:  # There is no reason not to find the skill...
            found_skill.value -= modifier
            found_skill.save()
            if found_skill.value == 0:
                found_skill.delete()

    def add_bc(self, aref):
        from collector.models.blessing_curse import BlessingCurse
        found_bc = self.blessingcurse_set.all().filter(blessing_curse_ref=aref).first()
        if found_bc:
            return found_bc
        else:
            bc = BlessingCurse()
            bc.character = self
            bc.blessing_curse_ref = aref
            bc.save()
            return bc

    def remove_bc(self, aref):
        # from collector.models.blessing_curse import BlessingCurse
        found_bc = self.blessingcurse_set.all().filter(blessing_curse_ref=aref).first()
        if found_bc:
            found_bc.delete()

    def add_weapon(self, aref):
        from collector.models.weapon import Weapon
        found_item = self.weapon_set.all().filter(weapon_ref=aref).first()
        if found_item:
            return found_item
        else:
            item = Weapon()
            item.character = self
            item.weapon_ref = aref
            item.save()
            return item

    def add_ritual(self, aref):
        from collector.models.ritual import Ritual
        found_item = self.ritual_set.all().filter(ritual_ref=aref).first()
        if found_item:
            return found_item
        else:
            item = Ritual()
            item.character = self
            item.ritual_ref = aref
            item.save()
            return item

    def add_armor(self, aref):
        from collector.models.armor import Armor
        found_item = self.armor_set.all().filter(armor_ref=aref).first()
        if found_item:
            return found_item
        else:
            item = Armor()
            item.character = self
            item.armor_ref = aref
            item.save()
            return item

    def add_shield(self, aref):
        from collector.models.shield import Shield
        found_item = self.shield_set.all().filter(shield_ref=aref).first()
        if found_item:
            return found_item
        else:
            item = Shield()
            item.character = self
            item.shield_ref = aref
            item.save()
            return item

    def remove_weapon(self, aref):
        from collector.models.weapon import Weapon
        found_item = self.weapon_set.all().filter(weapon_ref=aref).first()
        if found_item:
            found_item.delete()

    def remove_ritual(self, aref):
        from collector.models.ritual import Ritual
        found_item = self.ritual_set.all().filter(ritual_ref=aref).first()
        if found_item:
            found_item.delete()

    def remove_armor(self, aref):
        from collector.models.armor import Armor
        found_item = self.armor_set.all().filter(armor_ref=aref).first()
        if found_item:
            found_item.delete()

    def remove_shield(self, aref):
        from collector.models.shield import Shield
        found_item = self.shield_set.all().filter(shield_ref=aref).first()
        if found_item:
            found_item.delete()

    def add_ba(self, aref, adesc=''):
        from collector.models.benefice_affliction import BeneficeAffliction
        ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref, description=adesc).first()
        if ba:
            return ba
        else:
            ba = BeneficeAffliction()
            ba.character = self
            ba.benefice_affliction_ref = aref
            print("ADD_BA " + adesc)
            ba.description = adesc
            ba.save()
            print("ADD_BA (after) " + ba.description)
            return ba

    def remove_ba(self, aref):
        from collector.models.benefice_affliction import BeneficeAffliction
        found_ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref).first()
        if found_ba:
            found_ba.delete()

    def add_missing_root_skills(self):
        """ According to the character specialities, fixing the root skills """
        # from collector.models.skills import Skill
        from collector.models.skill import SkillRef
        roots_list = []
        # Get all roots in the avatar in roots_list
        for skill in self.skill_set.all():
            if skill.skill_ref.is_speciality:
                if not skill.skill_ref.is_wildcard:
                    roots_list.append(skill.skill_ref.linked_to)
        # Delete all roots from the avatar skills
        for skill in self.skill_set.all():
            if skill.skill_ref.is_root:
                skill.delete()
        # Add the roots from the root_list
        for skillref in SkillRef.objects.all():
            if skillref in roots_list:
                self.add_or_update_skill(skillref, roots_list.count(skillref))
        for item in roots_list:
            logger.debug('ROOT_LIST:%s' % (item.reference))

    def resetPA(self):
        self.PA_STR = self.PA_CON = self.PA_BOD = self.PA_MOV = self.PA_INT = self.PA_WIL = self.PA_TEM = self.PA_PRE = self.PA_TEC = self.PA_REF = self.PA_AGI = self.PA_AWA = self.OCC_LVL = self.OCC_DRK = 0

    @property
    def sumPA(self):
        return self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA + self.OCC_LVL - self.OCC_DRK

    def purgeSkills(self):
        """ Deleting all character skills """
        for skill in self.skill_set.all():
            skill.delete()
        logger.debug('PurgeSkill count: %d' % (self.skill_set.all().count()))

    def purgeTalents(self):
        """ Deleting all character talents """
        for talent in self.talent_set.all():
            talent.delete()
        logger.debug('PurgeTalent count: %d' % (self.talent_set.all().count()))

    def purgeBC(self):
        """ Deleting all character BC """
        for bc in self.blessingcurse_set.all():
            bc.delete()
        logger.debug('PurgeBC count: %d' % (self.blessingcurse_set.all().count()))

    def purgeBA(self):
        """ Deleting all character BA """
        for ba in self.beneficeaffliction_set.all():
            ba.delete()
        logger.debug('PurgeBA count: %d' % (self.beneficeaffliction_set.all().count()))

    def purgeWeapons(self):
        """ Deleting all character Weapons """
        for item in self.weapon_set.all():
            item.delete()
        logger.debug('PurgeWeapon count: %d' % (self.weapon_set.all().count()))

    def purgeShields(self):
        """ Deleting all character Shields """
        for item in self.shield_set.all():
            item.delete()
        logger.debug('PurgeShield count: %d' % (self.shield_set.all().count()))

    def purgeArmors(self):
        """ Deleting all character Weapons """
        for item in self.armor_set.all():
            item.delete()
        logger.debug('PurgeArmor count: %d' % (self.armor_set.all().count()))

    def purgeRituals(self):
        """ Deleting all character Rituals """
        for item in self.ritual_set.all():
            item.delete()
        logger.debug('PurgeRitual count: %d' % (self.ritual_set.all().count()))

    def resetTotal(self):
        """ Compute all sums for all stats """
        self.SK_TOTAL = 0
        self.BC_TOTAL = 0
        self.BA_TOTAL = 0
        self.weapon_cost = 0
        self.armor_cost = 0
        self.shield_cost = 0
        self.PA_TOTAL = \
            self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + \
            self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + \
            self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA + self.OCC_LVL - self.OCC_DRK
        skills = self.skill_set.all()
        for s in skills:
            if not s.skill_ref.is_root:
                if not s.skill_ref.is_wildcard:
                    self.SK_TOTAL += s.value
        blessingcurses = self.blessingcurse_set.all()
        for bc in blessingcurses:
            self.BC_TOTAL += bc.blessing_curse_ref.value
        beneficeafflictions = self.beneficeaffliction_set.all()
        for ba in beneficeafflictions:
            self.BA_TOTAL += ba.benefice_affliction_ref.value
        self.AP = self.PA_TOTAL
        self.OP = self.PA_TOTAL * 3 + self.SK_TOTAL + self.BC_TOTAL + self.BA_TOTAL
        weapons = self.weapon_set.all()
        for w in weapons:
            self.weapon_cost += w.weapon_ref.cost
        armors = self.armor_set.all()
        for a in armors:
            self.armor_cost += a.armor_ref.cost
        shields = self.shield_set.all()
        for s in shields:
            self.shield_cost += s.shield_ref.cost
        return "ok"

    def backup(self):
        """ Transform to PDF if exportable"""
        from collector.utils.basic import write_pdf
        proceed = True
        try:
            item = self
            context = {'c': item, 'filename': '%s' % (item.rid)}
            write_pdf('collector/character_roster.html', context)
        except:
            proceed = False
        return proceed

    def __str__(self):
        if self.alias:
            return '%s' % (self.alias)
        else:
            return '%s' % (self.full_name)

    def get_rid(self, s):
        self.rid = fs_fics7.find_rid(s)

    # Auto build character
    # def autobuild(self):
    #     # if self.role.value == 0 and not self.profile:
    #     #     return False
    #     # else:
    #     return True


@receiver(pre_save, sender=Character, dispatch_uid='update_character')
def update_character(sender, instance, conf=None, **kwargs):
    """ Before saving, fix() and  get_RID() for the character """
    if instance.rid != 'none':
        instance.fix(conf)
    instance.get_rid(instance.full_name)
    instance.alliancehash = hashlib.sha1(
        bytes(instance.alliance, 'utf-8')
    ).hexdigest()


@receiver(post_save, sender=Character, dispatch_uid='backup_character')
def backup_character(sender, instance, **kwargs):
    """ After saving, create PDF for the character """
    if instance.rid != 'none':
        instance.backup()
