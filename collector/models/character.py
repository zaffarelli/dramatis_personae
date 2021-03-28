"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from datetime import datetime
from django.urls import reverse
from collector.models.specie import Specie
from collector.models.combattant import Combattant
from collector.models.alliance_ref import AllianceRef
from cartograph.models.system import System
from collector.utils import fs_fics7
from django.utils.timezone import get_current_timezone
import itertools
import logging
import json
from colorfield.fields import ColorField

logger = logging.getLogger(__name__)

DRAMA_SEATS = (
    ('11-foe', 'Foe'),
    ('10-enemy', 'Enemy'),
    ('09-lackey', 'Lackey'),
    ('08-antagonist', 'Antagonist'),
    ('07-opponent', 'Opponent'),
    ('06-neutral', 'Neutral'),
    ('05-partisan', 'Partisan'),
    ('04-protagonist', 'Protagonist'),
    ('03-servant', 'Servant'),
    ('02-ally', 'Ally'),
    ('01-friend', 'Friend'),
    ('00-players', 'Players'),
)

BLOKES = {
    'allies': ['05-partisan', '04-protagonist', '03-servant', '02-ally', '01-friend'],
    'foes': ['11-foe', '10-enemy', '09-lackey', '08-antagonist', '07-opponent'],
    'others': ['06-neutral']
}


class Character(Combattant):
    class Meta:
        ordering = ['full_name']
        verbose_name = "FICS: Character"

    page_num = 0
    alias = models.CharField(max_length=200, default='', blank=True)
    alliance = models.CharField(max_length=200, default='', blank=True)
    faction = models.CharField(max_length=200, default='', blank=True)
    # alliance_hash = models.CharField(max_length=200, default='none')
    alliance_ref = models.ForeignKey(AllianceRef, blank=True, null=True, on_delete=models.SET_NULL)
    specie = models.ForeignKey(Specie, default=31, blank=True, null=True, on_delete=models.SET_NULL)
    race = models.TextField(max_length=256, default='', blank=True)
    native_fief = models.CharField(max_length=200, default='none')
    fief = models.ForeignKey(System, blank=True, null=True, on_delete=models.SET_NULL, related_name='fief')
    current_fief = models.ForeignKey(System, blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='current_fief')
    caste = models.CharField(max_length=100, default='Freefolk')
    rank = models.CharField(max_length=100, default='', blank=True)
    build_log = models.TextField(default='', blank=True)
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

    physical = models.IntegerField(default=0, blank=True)
    mental = models.IntegerField(default=0, blank=True)
    combat = models.IntegerField(default=0, blank=True)
    tod_count = models.IntegerField(default=0, blank=True)

    weapon_cost = models.IntegerField(default=0)
    armor_cost = models.IntegerField(default=0)
    shield_cost = models.IntegerField(default=0)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    gm_shortcuts = models.TextField(default='', blank=True)
    gm_shortcuts_pdf = models.TextField(default='', blank=True)
    team = models.CharField(max_length=128, choices=DRAMA_SEATS, default='06-neutral', blank=True)
    OCC_LVL = models.PositiveIntegerField(default=0)
    OCC_DRK = models.PositiveIntegerField(default=0)
    occult = models.CharField(max_length=50, default='', blank=True)
    challenge = models.TextField(default='')
    challenge_value = models.IntegerField(default=0)
    todo_list = models.TextField(default='', blank=True)
    path = models.CharField(max_length=256, default='', blank=True)
    # is_exportable = models.BooleanField(default=False)
    use_history_creation = models.BooleanField(default=False)
    use_only_entrance = models.BooleanField(default=False)
    picture = models.CharField(max_length=1024,
                               default='https://drive.google.com/open?id=15hdubdMt1t_deSXkbg9dsAjWi5tZwMU0', blank=True)
    alliance_picture = models.CharField(max_length=256, default='', blank=True)
    on_save_re_roll_attributes = models.BooleanField(default=False)
    on_save_re_roll_skills = models.BooleanField(default=False)
    life_path_total = models.IntegerField(default=0)
    overhead = models.IntegerField(default=0)
    stories_count = models.PositiveIntegerField(default=0)
    stories = models.TextField(max_length=1024, default='', blank=True)
    balanced = models.BooleanField(default=False)
    historical_figure = models.BooleanField(default=False)
    nameless = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    ranking = models.IntegerField(default=0, blank=True)
    group_color = ColorField(default='#888888', blank=True)
    color = ColorField(default='#CCCCCC', blank=True)

    storytelling_note = models.TextField(default='', blank=True)

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
    def ghostmark_data(self):
        if self.alliance_ref:
            alliance_ref = AllianceRef.objects.get(reference=self.alliance_ref.reference)
        else:
            alliance_ref = AllianceRef.objects.get(reference='None')
        x = self.id

        data = {
            'id': x,
            'character': {
                'rid': self.rid,
                'id': x,
                'full_name': self.full_name,
                'gender': self.gender,
                'race': self.specie.species,
                'OCC_LVL': self.OCC_LVL,
                'OCC_DRK': self.OCC_DRK,
                'occult': self.occult,
                'ranking': self.ranking,
                'physical': self.physical,
                'mental': self.mental,
                'combat': self.combat,
                'tod_count': self.tod_count,
                'balanced': self.balanced,
            },
            'alliance': {
                'reference': alliance_ref.reference,
                'color_front': alliance_ref.color_front,
                'color_back': alliance_ref.color_back,
                'color_highlight': alliance_ref.color_highlight,
                'icon_simple': alliance_ref.icon_simple,
                'icon_complex': alliance_ref.icon_complex,
                'color_icon_fill': alliance_ref.color_icon_fill,
                'color_icon_stroke': alliance_ref.color_icon_stroke,
                'category': alliance_ref.category,
                'faction': alliance_ref.faction,
            }
        }
        jdata = json.dumps(data, sort_keys=True, indent=4)
        return jdata

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
        return reverse('recalc_avatar', kwargs={'id': self.id})

    def get_pa(self, str):
        context = {"attribute": str, "value": getattr(self, str), "id": self.id}
        return context

    # def toJSON(self):
    #     """ Returns JSON of object """
    #     return json.dumps(self, default=json_default,sort_keys=True, indent=4)

    def rebuild_from_lifepath(self):
        """ Historical Creation """
        old_op = self.OP
        self.build_log = ''
        from collector.models.character_custo import CharacterCusto
        found_custo = CharacterCusto.objects.filter(character=self).first()
        if found_custo is None:
            self.charactercusto = CharacterCusto.objects.create(character=self)
        self.resetPA()
        self.purge_skills()
        self.purge_bc()
        self.purge_ba()
        self.purge_weapons()
        self.purge_armors()
        self.purge_shields()
        self.purge_rituals()
        # self.purge_talents()
        self.AP_tod_pool = 0
        self.OP_tod_pool = 0
        self.WP_tod_pool = 0
        self.life_path_total = 0
        self.race = self.specie.species
        bl = []
        tod_rep = {
            'RA': 0,
            'UP': 0,
            'AP': 0,
            'EC': 0,
            'TO': 0,
            'WB': 0,
        }
        all_tod_wp_roots = []
        for tod in self.tourofduty_set.all():
            AP, OP, WP, tod_wp_roots = tod.push(self)
            all_tod_wp_roots.append(tod_wp_roots)
            self.AP_tod_pool += AP
            self.OP_tod_pool += OP
            self.OP_tod_pool += WP
            self.WP_tod_pool += WP
            self.life_path_total += tod.tour_of_duty_ref.value
            if tod.tour_of_duty_ref.category == '0' or tod.tour_of_duty_ref.category == '5':
                tod_rep['RA'] += tod.tour_of_duty_ref.value
            elif tod.tour_of_duty_ref.category == '10':
                tod_rep['UP'] += tod.tour_of_duty_ref.value
            elif tod.tour_of_duty_ref.category == '20':
                tod_rep['AP'] += tod.tour_of_duty_ref.value
            elif tod.tour_of_duty_ref.category == '30':
                tod_rep['EC'] += tod.tour_of_duty_ref.value
            elif tod.tour_of_duty_ref.category == '40':
                tod_rep['TO'] += tod.tour_of_duty_ref.value
            elif tod.tour_of_duty_ref.category == '50':
                tod_rep['WB'] += tod.tour_of_duty_ref.value
        # Flatten
        doubles_all_wp_roots = list(itertools.chain(*all_tod_wp_roots))
        # Remove multi
        all_wp_roots = list(dict.fromkeys(doubles_all_wp_roots))
        if self.charactercusto:
            self.charactercusto.comment = self.full_name
            self.charactercusto.push(self)
            self.charactercusto.save()
        pa_total = self.sumPA
        po_total = 0
        for s in self.skill_set.all():
            if not s.skill_ref.is_root:
                po_total += s.value
        ba_total = 0
        for ba in self.beneficeaffliction_set.all():
            ba_total += ba.benefice_affliction_ref.value
        bc_total = 0
        for bc in self.blessingcurse_set.all():
            bc_total += bc.blessing_curse_ref.value
        bl.append("")
        # bl.append("Tour Summary:")
        # bl.append("- APx3+OP+BA+BC... " + str(pa_total * 3 + po_total + ba_total + bc_total))
        # bl.append("- WP.............. " + str(self.WP_tod_pool))
        # bl.append("- Value........... " + str(self.charactercusto.value))
        # bl.append("- Lifepath ....... " + str(self.life_path_total))
        # bl.append("- Repartition .... " + str(tod_rep))
        fs_fics7.check_secondary_attributes(self)
        self.handle_wildcards(all_wp_roots)
        self.charactercusto.save()
        self.prepare_display()

        self.add_missing_root_skills()
        self.reset_total()
        self.checkOverhead()
        self.balanced = (self.life_path_total == self.OP) and (self.OP > 0)
        self.priority = (abs(self.life_path_total - self.OP) < 8) and (self.OP > 0) and (
                abs(self.life_path_total - self.OP) > 0)
        self.build_log = "\n".join(bl)
        if self.player != '':
            self.balanced = True
        if self.historical_figure:
            self.balanced = True
        if self.balanced:
            logger.info(f'Current option Points: {self.OP}')
        else:
            logger.error(f'{self.full_name} is not properly balanced: {self.OP} vs {self.life_path_total}!')
        if self.color == '#CCCCCC':
            d = lambda x: fs_fics7.roll(x) - 1
            self.color = '#%01X%01X%01X%01X%01X%01X' % (d(8) + 4, d(16), d(8) + 4, d(16), d(8) + 4, d(16))
        self.need_pdf = old_op != self.OP

    def checkOverhead(self):
        overhead = 0
        if self.PA_STR > 10:
            overhead += 10 - self.PA_STR
        if self.PA_CON > 10:
            overhead += 10 - self.PA_CON
        if self.PA_BOD > 10:
            overhead += 10 - self.PA_BOD
        if self.PA_MOV > 10:
            overhead += 10 - self.PA_MOV
        if self.PA_INT > 10:
            overhead += 10 - self.PA_INT
        if self.PA_WIL > 10:
            overhead += 10 - self.PA_WIL
        if self.PA_TEM > 10:
            overhead += 10 - self.PA_TEM
        if self.PA_PRE > 10:
            overhead += 10 - self.PA_PRE
        if self.PA_REF > 10:
            overhead += 10 - self.PA_REF
        if self.PA_AGI > 10:
            overhead += 10 - self.PA_AGI
        if self.PA_AWA > 10:
            overhead += 10 - self.PA_AWA
        if self.PA_TEC > 10:
            overhead += 10 - self.PA_TEC
        self.overhead = overhead
        if overhead > 0:
            logger.error(f'>>> Overhead found: {overhead}')
        else:
            logger.info(f'>>> No Overhead.')

    def prepare_display(self):
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

    def handle_wildcards(self, root_list):
        """ Calculate wildcard amount from the ToDs (ToD_WC), and check if the amount is satisfied with skills
            matching the wildcards roots in the custo (C_WC).
        """
        # print(root_list)
        self.charactercusto.watch_roots = "_".join(root_list)

    def rebuild_free_form(self):
        """ Freeform Creation """
        # self.reset_total()
        # if self.onsave_reroll_attributes:
        #     fs_fics7.check_primary_attributes(self)
        #     fs_fics7.check_secondary_attributes(self)
        # if self.onsave_reroll_skills:
        #     fs_fics7.check_skills(self)
        # else:
        self.add_missing_root_skills()
        self.reset_total()

    def fix(self, conf=None):
        super().fix(conf)
        """ Check / calculate other characteristics """

        if not conf:
            if self.birthdate < 1000:
                self.birthdate = 5017 - self.birthdate
                self.age = 5017 - self.birthdate
        else:
            if self.birthdate < 1000:
                self.birthdate = conf.epic.era - self.birthdate
                self.age = conf.epic.era - self.birthdate
        # NPC fix
        if self.use_history_creation:
            self.rebuild_from_lifepath()
        else:
            self.rebuild_free_form()
        self.calculate_shortcuts()

        self.update_ranking()
        self.race = self.specie.species

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
        self.update_stories_count()
        self.race = self.specie.species
        if self.use_history_creation:
            self.check_todo_list()
        self.need_fix = False
        self.update_game_parameters()
        logger.info(f'    => Done fixing ...: {self.full_name} NeedFIX:{self.need_fix}')

    def check_todo_list(self):
        """ Check for invalid tours of duty for the character
        """
        self.todo_list = ""
        tsk = []
        histories = {'10':0,'20':0, '30':0, '40':0, '50':0}
        if self.use_history_creation:
            for tod in self.tourofduty_set.all():
                if not tod.tour_of_duty_ref.valid:
                    tsk.append(f'--> *{tod.tour_of_duty_ref.reference}* is not a valid Tour of Duty.')
                    logger.error(tsk)
            if not self.nameless:
                for tod in self.tourofduty_set.all():
                    # logger.debug(tod.tour_of_duty_ref.category)
                    if tod.tour_of_duty_ref.category in ['10','20','30', '40', '50']:
                        histories[tod.tour_of_duty_ref.category] += tod.tour_of_duty_ref.value
                x = f'--> {histories}'
                logger.debug(x)
                if (histories['10'] == 20) and (histories['20'] == 25) and (histories['30'] == 48) and (histories['50'] == 7):
                    logger.info('Basic histories balanced')
                else:
                    tsk.append(x)
                logger.debug(f' Number of ToDS: {histories["40"]/10}')
                self.tod_count = histories["40"]/10

        self.todo_list = "\n".join(tsk)

    def update_challenge(self):
        res = ''
        res += '<i class="fas fa-th-large" title="primary attributes"></i>%d ' % (self.AP)
        res += '<i class="fas fa-th-list" title="skills"></i> %d ' % (self.SK_TOTAL)
        res += '<i class="fas fa-th" title="talents"></i> %d ' % (self.TA_TOTAL + self.BC_TOTAL + self.BA_TOTAL)
        res += '<i class="fas fa-star" title="wildcards"></i> %d ' % (self.WP_tod_pool)
        res += '<i class="fas fa-newspaper" title="OP challenge"></i> %d/%d' % (self.OP, self.life_path_total)
        self.challenge_value = self.AP * 3 + self.SK_TOTAL + self.BC_TOTAL + self.BA_TOTAL
        self.challenge = res

    def calculate_shortcuts(self):
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
        self.gm_shortcuts_pdf = ', '.join(shortcuts_pdf)

    def refresh_options(self, options, options_not, custo_set, ref_type, ref_class):
        """ Refresh options / options_not global engine
            Warning: Keep the model imports right here. PyCharm will not see that we are actually using these models
            as we are using string to model to handle all of this.
        """
        from collector.models.benefice_affliction import BeneficeAfflictionRef
        from collector.models.blessing_curse import BlessingCurseRef
        from collector.models.weapon import WeaponRef
        from collector.models.armor import ArmorRef
        from collector.models.shield import ShieldRef
        from collector.models.ritual import RitualRef
        o = []
        o_n = []
        custo_items = custo_set
        custo_ref_items = []
        for item in custo_items:
            custo_ref_items.append(getattr(item, ref_type))
        all_items = eval(ref_class).objects.all()
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
        found_item = self.weapon_set.all().filter(weapon_ref=aref).first()
        if found_item:
            found_item.delete()

    def remove_ritual(self, aref):
        found_item = self.ritual_set.all().filter(ritual_ref=aref).first()
        if found_item:
            found_item.delete()

    def remove_armor(self, aref):
        found_item = self.armor_set.all().filter(armor_ref=aref).first()
        if found_item:
            found_item.delete()

    def remove_shield(self, aref):
        found_item = self.shield_set.all().filter(shield_ref=aref).first()
        if found_item:
            found_item.delete()

    def update_ranking(self):
        all = self.beneficeaffliction_set.all()
        self.ranking = 0
        rankraise = 0
        for ba in all:
            if ba.benefice_affliction_ref.ranking:
                if ba.benefice_affliction_ref.emphasis == '':
                    self.ranking += ba.benefice_affliction_ref.value
                else:
                    if ba.benefice_affliction_ref.emphasis == 'rankraise':
                        if ba.benefice_affliction_ref.value > rankraise:
                            rankraise = ba.benefice_affliction_ref.value
        self.ranking += rankraise

    def add_ba(self, aref, adesc=''):
        from collector.models.benefice_affliction import BeneficeAffliction
        ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref, description=adesc).first()
        if ba:
            return ba
        else:
            ba = BeneficeAffliction()
            ba.character = self
            ba.benefice_affliction_ref = aref
            ba.description = adesc
            ba.save()
            return ba

    def remove_ba(self, aref):
        found_ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref).first()
        if found_ba:
            found_ba.delete()

    def add_missing_root_skills(self):
        from collector.models.skill import SkillRef
        roots_list = []
        for skill in self.skill_set.all():
            if skill.skill_ref.is_speciality:
                if not skill.skill_ref.is_wildcard:
                    roots_list.append(skill.skill_ref.linked_to)
        for skill in self.skill_set.all():
            if skill.skill_ref.is_root:
                skill.delete()
        for skill_ref in SkillRef.objects.all():
            if skill_ref in roots_list:
                self.add_or_update_skill(skill_ref, roots_list.count(skill_ref))

    def resetPA(self):
        self.PA_STR = self.PA_CON = self.PA_BOD = self.PA_MOV = self.PA_INT = self.PA_WIL = self.PA_TEM = self.PA_PRE = self.PA_TEC = self.PA_REF = self.PA_AGI = self.PA_AWA = self.OCC_LVL = self.OCC_DRK = 0

    @property
    def sumPA(self):
        return self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA + self.OCC_LVL - self.OCC_DRK

    def purge_skills(self):
        for skill in self.skill_set.all():
            skill.delete()

    def purge_bc(self):
        for bc in self.blessingcurse_set.all():
            bc.delete()

    def purge_ba(self):
        for ba in self.beneficeaffliction_set.all():
            ba.delete()

    def purge_weapons(self):
        for item in self.weapon_set.all():
            item.delete()

    def purge_shields(self):
        for item in self.shield_set.all():
            item.delete()

    def purge_armors(self):
        for item in self.armor_set.all():
            item.delete()

    def purge_rituals(self):
        for item in self.ritual_set.all():
            item.delete()

    def reset_total(self):
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
        proceed = False
        if self.need_pdf:
            from collector.utils.basic import write_pdf
            try:
                context = dict(c=self, filename=f'{self.rid}', now=datetime.now(tz=get_current_timezone()))
                write_pdf('collector/character_roster.html', context)
                logger.info(f'    => PDF created ...: {self.rid}')
                proceed = True
                self.need_pdf = False
                self.save()
            except:
                logger.error(f'    => PDF creation error !!! {self.rid}')
        return proceed

    def __str__(self):
        if self.alias:
            return f'{self.alias}'
        else:
            return f'{self.full_name}'

    @property
    def na_phy(self):
        return round((self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV) / 4)

    @property
    def na_men(self):
        return round((self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE) / 4)

    @property
    def na_com(self):
        return round((self.PA_TEC + self.PA_AGI + self.PA_REF + self.PA_AWA) / 4)

    # Auto build character
    def autobuild(self):
        # if self.role.value == 0 and not self.profile:
        #     return False
        # else:
        return True

    def count_cast(self, all):
        result = 0
        for story in all:
            if story.got(self.rid):
                result += 1
                self.stories += f'{story.get_full_id}_{story.title}#'
        return result

    def update_stories_count(self):
        self.stories_count = 0
        self.stories = ''
        from scenarist.models.events import Event
        from scenarist.models.acts import Act
        from scenarist.models.dramas import Drama
        from scenarist.models.epics import Epic
        events = Event.objects.all()
        acts = Act.objects.all()
        dramas = Drama.objects.all()
        epics = Epic.objects.all()
        self.stories_count += self.count_cast(events)
        self.stories_count += self.count_cast(acts)
        self.stories_count += self.count_cast(dramas)
        self.stories_count += self.count_cast(epics)
        return self.stories_count

    def update_game_parameters(self):
        self.physical = (self.PA_STR + self.PA_BOD + self.PA_MOV + self.PA_CON)/4
        self.mental = (self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE)/4
        self.combat = (self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA)/4
        # Check for racial tods
        from collector.models.tourofduty import TourOfDutyRef, TourOfDuty
        ra_tod = None
        br_tod = None
        if self.specie.ra_tod_name:
            ra_tod = TourOfDutyRef.objects.get(reference=self.specie.ra_tod_name)
        if self.specie.br_tod_name:
            br_tod = TourOfDutyRef.objects.get(reference=self.specie.br_tod_name)
        for tod in self.tourofduty_set.all():
            if ra_tod != None:
                if ra_tod.reference == tod.tour_of_duty_ref.reference:
                    ra_tod = None
            if br_tod != None:
                if br_tod.reference == tod.tour_of_duty_ref.reference:
                    br_tod = None
        if ra_tod != None:
            t = TourOfDuty()
            t.character = self
            t.tour_of_duty_ref = ra_tod
            t.save()
            logger.info(f'    => Added ToD {t} to {self.rid}')
        if br_tod != None:
            t = TourOfDuty()
            t.character = self
            t.tour_of_duty_ref = br_tod
            t.save()
            logger.info(f'    => Added ToD {t} to {self.rid}')
        logger.debug(f'    => Updating Game parameters... ({self.specie.species}, {self.specie.race})')