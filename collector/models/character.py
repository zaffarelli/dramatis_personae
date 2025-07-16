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
from collector.utils.fics_references import BLOKES, DRAMA_SEATS
from django.utils.timezone import get_current_timezone
import itertools
import logging
import json
from colorfield.fields import ColorField
from operator import itemgetter

logger = logging.getLogger(__name__)


class Character(Combattant):
    class Meta:
        ordering = ['full_name']
        verbose_name = "FICS: Character"

    page_num = 0
    alias = models.CharField(max_length=200, default='', blank=True)
    # alliance = models.CharField(max_length=200, default='', blank=True)

    fief_rid = models.CharField(max_length=200, default="", blank=True)
    alliance_rid = models.CharField(max_length=200, default="", blank=True)
    specie_rid = models.CharField(max_length=200, default="", blank=True)
    current_fielf_rid = models.CharField(max_length=200, default="", blank=True)
    bookmark_tag = models.CharField(max_length=200, default="", blank=True)

    faction = models.CharField(max_length=200, default='', blank=True)
    alliance_ref = models.ForeignKey(AllianceRef, blank=True, null=True, on_delete=models.SET_NULL)
    specie = models.ForeignKey(Specie, default=31, blank=True, null=True, on_delete=models.SET_NULL)
    race = models.CharField(max_length=256, default='', blank=True)
    native_fief = models.CharField(max_length=200, default='none', blank=True)
    fief = models.ForeignKey(System, blank=True, null=True, on_delete=models.SET_NULL, related_name='fief')
    current_fief = models.ForeignKey(System, blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name='current_fief')
    caste = models.CharField(max_length=100, default='Freefolk', blank=True)
    rank = models.CharField(max_length=100, default='', blank=True)
    build_log = models.TextField(default='', blank=True)
    lifepath_status = models.CharField(max_length=100, default='', blank=True)
    PA_STR = models.PositiveIntegerField(default=1, blank=True)
    PA_CON = models.PositiveIntegerField(default=1, blank=True)
    PA_BOD = models.PositiveIntegerField(default=1, blank=True)
    PA_MOV = models.PositiveIntegerField(default=1, blank=True)
    PA_INT = models.PositiveIntegerField(default=1, blank=True)
    PA_WIL = models.PositiveIntegerField(default=1, blank=True)
    PA_TEM = models.PositiveIntegerField(default=1, blank=True)
    PA_PRE = models.PositiveIntegerField(default=1, blank=True)
    PA_DEX = models.PositiveIntegerField(default=1, blank=True)
    PA_TEC = models.PositiveIntegerField(default=1, blank=True)
    PA_AGI = models.PositiveIntegerField(default=1, blank=True)
    PA_AWA = models.PositiveIntegerField(default=1, blank=True)
    SA_REC = models.IntegerField(default=0, blank=True)
    SA_STA = models.IntegerField(default=0, blank=True)
    SA_END = models.IntegerField(default=0, blank=True)
    SA_STU = models.IntegerField(default=0, blank=True)
    SA_RES = models.IntegerField(default=0, blank=True)
    SA_DMG = models.IntegerField(default=0, blank=True)
    SA_TOL = models.IntegerField(default=0, blank=True)
    SA_HUM = models.IntegerField(default=0, blank=True)
    SA_PAS = models.IntegerField(default=0, blank=True)
    SA_WYR = models.IntegerField(default=0, blank=True)
    SA_SPD = models.IntegerField(default=0, blank=True)
    SA_RUN = models.IntegerField(default=0, blank=True)
    PA_TOTAL = models.IntegerField(default=0, blank=True)
    SK_TOTAL = models.IntegerField(default=0, blank=True)
    DE_TOTAL = models.IntegerField(default=0, blank=True)
    TA_TOTAL = models.IntegerField(default=0, blank=True)
    BC_TOTAL = models.IntegerField(default=0, blank=True)
    BA_TOTAL = models.IntegerField(default=0, blank=True)
    physical = models.IntegerField(default=0, blank=True)
    mental = models.IntegerField(default=0, blank=True)
    combat = models.IntegerField(default=0, blank=True)
    tod_count = models.IntegerField(default=0, blank=True)
    weapon_cost = models.IntegerField(default=0, blank=True)
    armor_cost = models.IntegerField(default=0, blank=True)
    shield_cost = models.IntegerField(default=0, blank=True)
    AP = models.IntegerField(default=0, blank=True)
    OP = models.IntegerField(default=0, blank=True)

    development_points = models.IntegerField(default=0, blank=True)

    experience_balance = models.IntegerField(default=0, blank=True)
    xp_pool = models.IntegerField(default=0, blank=True)
    xp_spent = models.IntegerField(default=0, blank=True)
    xp_earned = models.IntegerField(default=0, blank=True)
    score = models.IntegerField(default=0, blank=True)
    gm_shortcuts = models.TextField(default='', blank=True)
    gm_shortcuts_pdf = models.TextField(default='', blank=True)
    PA_OCC = models.PositiveIntegerField(default=0, blank=True)
    PA_DRK = models.PositiveIntegerField(default=0, blank=True)
    occult_fire_power = models.PositiveIntegerField(default=0, blank=True)
    occult = models.CharField(max_length=50, default='', blank=True)
    challenge_value = models.IntegerField(default=0, blank=True)
    cast_figure = models.CharField(max_length=256, default='', blank=True)
    path = models.CharField(max_length=256, default='', blank=True)
    stigma = models.CharField(max_length=256, default='', blank=True)
    use_history_creation = models.BooleanField(default=False)
    picture = models.CharField(max_length=1024,
                               default='https://drive.google.com/open?id=15hdubdMt1t_deSXkbg9dsAjWi5tZwMU0', blank=True)
    alliance_picture = models.CharField(max_length=256, default='', blank=True)

    life_path_total = models.IntegerField(default=0, blank=True)
    overhead = models.IntegerField(default=0, blank=True)
    stories_count = models.PositiveIntegerField(default=0, blank=True)
    balanced = models.BooleanField(default=False, blank=True)
    selected = models.BooleanField(default=False, blank=True)
    historical_figure = models.BooleanField(default=False, blank=True)
    nameless = models.BooleanField(default=False, blank=True)
    incognito = models.BooleanField(default=False, blank=True)
    error = models.BooleanField(default=False, blank=True)
    ranking = models.IntegerField(default=0, blank=True)
    group_color = ColorField(default='#888888', blank=True)
    color = ColorField(default='#CCCCCC', blank=True)
    team = models.CharField(max_length=128, choices=DRAMA_SEATS, default='06-neutral', blank=True)
    wealth = models.IntegerField(default=0, blank=True)
    challenge = models.TextField(default='', blank=True)
    custo_descs = models.TextField(default='', blank=True)
    storytelling_note = models.TextField(default='', blank=True)
    stories = models.TextField(max_length=1024, default='', blank=True)
    todo_list = models.TextField(default='', blank=True)
    experience_details = models.TextField(max_length=1024, default='', blank=True)
    azurites = models.PositiveIntegerField(default=0, blank=True)
    diamonds = models.PositiveIntegerField(default=0, blank=True)
    rubies = models.PositiveIntegerField(default=0, blank=True)
    incomp = models.PositiveIntegerField(default=0, blank=True)
    sanity = models.PositiveIntegerField(default=0, blank=True)

    skills_options = []
    degrees_options = []
    ba_options = []
    bc_options = []
    skills_options_not = []
    degrees_options_not = []
    ba_options_not = []
    bc_options_not = []
    AP_tod_pool = 0
    OP_tod_pool = 0
    SK_tod_pool = 0
    DE_tod_pool = 0
    BC_tod_pool = 0
    BA_tod_pool = 0
    SWP_tod_pool = 0
    DWP_tod_pool = 0
    weapon_options = []
    weapon_options_not = []
    armor_options = []
    armor_options_not = []
    shield_options = []
    shield_options_not = []

    # degrees_wp_choices = {}

    @property
    def ghostmark_data(self):
        if self.alliance_ref:
            alliance_ref = AllianceRef.objects.get(reference=self.alliance_ref.reference)
        else:
            alliance_ref = AllianceRef.objects.get(reference='None')
        x = self.id
        from collector.templatetags.fics_filters import as_roman
        if self.tod_count > 0:
            roman_tod_count = as_roman(self.tod_count)
        else:
            roman_tod_count = '-'
        data = {
            'id': x,
            'character': {
                'rid': self.rid,
                'id': x,
                'full_name': self.full_name,
                'gender': self.gender,
                'race': self.specie.species,
                'PA_OCC': self.PA_OCC,
                'PA_DRK': self.PA_DRK,
                'occult': self.occult,
                'ranking': self.ranking,
                'physical': self.physical,
                'mental': self.mental,
                'combat': self.combat,
                'tod_count': roman_tod_count,
                'fencing_league': self.fencing_league,
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
    def info_dex(self):
        return self.get_pa("PA_DEX")

    @property
    def info_agi(self):
        return self.get_pa("PA_AGI")

    @property
    def info_awa(self):
        return self.get_pa("PA_AWA")

    @property
    def info_occ(self):
        return self.get_pa("PA_OCC")

    @property
    def info_drk(self):
        return self.get_pa("PA_DRK")

    def get_absolute_url(self):
        return reverse('recalc_avatar', kwargs={'id': self.id})

    def get_pa(self, str):
        context = {"attribute": str, "value": getattr(self, str), "id": self.id}
        return context

    # def to_json(self):
    #     """ Returns JSON of object """
    #     return json.dumps(self, default=json_default,sort_keys=True, indent=4)

    def tod_done(self):
        ready = True
        tods_cnt = 0
        if self.use_history_creation:
            tod_rep = {
                'RA': 0,
                'UP': 0,
                'AP': 0,
                'EC': 0,
                'TO': 0,
                'WB': 0,
            }
            for tod in self.tourofduty_set.all():
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
                    tods_cnt += 1
                elif tod.tour_of_duty_ref.category == '50':
                    tod_rep['WB'] += tod.tour_of_duty_ref.value
            ready = tod_rep['RA'] > 0 and tod_rep['UP'] == 20 and tod_rep['AP'] == 25 and tod_rep['EC'] == 48 and \
                    tod_rep['WB'] == 7
        return ready, tods_cnt

    def custocheck(self):
        from collector.models.character_custo import CharacterCusto
        found_custo = CharacterCusto.objects.filter(character=self).first()
        if found_custo is None:
            self.charactercusto = CharacterCusto.objects.create(character=self)
        # else:
        #     self.audit_log(f"Character custo found: {found_custo}")
        print("RFL: Complete character clean up")

    def rebuild_from_lifepath(self):
        """ Historical Creation """
        old_op = self.OP
        self.build_log = ''
        self.custocheck()
        self.resetPA()
        self.purge_skills()
        self.purge_degrees()
        self.purge_bc()
        self.purge_ba()
        self.purge_weapons()
        self.purge_armors()
        self.purge_shields()
        self.purge_rituals()
        self.AP_tod_pool = 0
        self.OP_tod_pool = 0
        self.SK_tod_pool = 0
        self.DE_tod_pool = 0
        self.BC_tod_pool = 0
        self.BA_tod_pool = 0
        self.SWP_tod_pool = 0
        self.DWP_tod_pool = 0
        self.life_path_total = 0
        self.race = self.specie.species
        self.charactercusto.prune("allocated")
        self.charactercusto.prune("fixed")
        self.charactercusto.prune("wildcard")
        self.charactercusto.prune("fulfilled")
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
        self.audit_log("<strong>Applying Lifepath</strong>")
        # self.audit_log("<ul>")
        for tod in self.tourofduty_set.all():
            AP, SK, DE, BC, BA,AWP, SWP, DWP, BCW, BAW, OP = tod.push(self)
            #self.charactercusto.register_tod_wp(tod.tour_of_duty_ref.degrees_wp_choices)
            self.charactercusto.register_tod(tod)
            todname = f"{tod.tour_of_duty_ref.reference:.<30}"
            todcat = f"{tod.tour_of_duty_ref.get_category_display()[:2]}"
            todval = f"{tod.tour_of_duty_ref.value:_>3}"
            self.audit_log(f"- {todname} [{todcat}] {todval} OP s:{SK:_>2}/{SWP:_>2} d:{DE:_>2}/{DWP:_>2}")

            # self.mix_degree_wp_choices(tod.tour_of_duty_ref.degrees_wp_choices)

            self.AP_tod_pool += AP
            self.OP_tod_pool += OP
            self.SK_tod_pool += SK
            self.DE_tod_pool += DE
            self.BC_tod_pool += BC
            self.BA_tod_pool += BA
            self.SWP_tod_pool += SWP
            self.DWP_tod_pool += DWP
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
        if self.life_path_total < 200 and not self.nameless:
            self.archive_level = 'WKS'
            self.audit_log("Archive level is WKS: Lifepath total is less than 200.")
        # print("MIX Results",self.degrees_wp_choices)
        # Flatten
        # doubles_all_wp_roots = list(itertools.chain(*all_tod_wp_roots))
        # Remove multi
        # all_wp_roots = list(dict.fromkeys(doubles_all_wp_roots))
        # if self.charactercusto:
        self.charactercusto.comment = self.full_name
        self.charactercusto.push(self)
        #self.charactercusto.save()
        pa_total = self.sumPA
        po_total = 0
        ps_total = 0
        pd_total = 0
        for s in self.skill_set.all():
            ps_total += s.value
        for d in self.degree_set.all():
            pd_total += d.value
        ba_total = 0
        for ba in self.beneficeaffliction_set.all():
            ba_total += ba.benefice_affliction_ref.value
        bc_total = 0
        for bc in self.blessingcurse_set.all():
            bc_total += bc.blessing_curse_ref.value
        bl.append("")
        fs_fics7.check_secondary_attributes(self)
        self.prepare_display()
        self.audit_log("<b>Option Points Summary</b>")
        self.reset_total()
        self.checkOverhead()
        self.balanced = (self.life_path_total == self.OP - self.experience_balance) and (self.OP > 0)
        all_op = pa_total * 3 + ps_total + pd_total + ba_total + bc_total
        self.audit_log(f"OP lifepath (sum of previous)... {self.life_path_total:.>3} OP")
        self.audit_log(f"OP total ....................... {all_op:.>3} OP")
        self.audit_log(f"OP experience Balance .......... {self.experience_balance:.>3} OP")
        equilibrium = all_op - self.life_path_total - self.experience_balance
        if equilibrium != 0:
            self.audit_log(f"................................ {equilibrium:.>3} OP")
        else:
            self.audit_log(f"................................ <b>{equilibrium:.>3} OP</b>")
        self.audit_log(f"Skills ......................... {ps_total:.>3} OP (swp:{self.SWP_tod_pool} OP)")
        self.audit_log(f"Degrees ........................ {pd_total:.>3} OP (dwp:{self.DWP_tod_pool} OP)")
        self.audit_log(f"CharacterCusto Value ........... {self.charactercusto.value:.>3} OP")
        self.audit_log(f"XP (earned) .................... {self.xp_earned:.>3} XP")
        self.audit_log(f"XP (remaining) ................. {self.xp_pool:.>3} XP")
        self.audit_log(f"XP (spent) ..................... {self.xp_spent:.>3} XP")
        self.priority = (abs(self.life_path_total - self.OP) < 8) and (self.OP > 0) and (
                abs(self.life_path_total - self.OP) > 0)
        self.build_log = "\n".join(bl)
        self.charactercusto.save()
        if self.historical_figure:
            self.balanced = True
        # Randomize color
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
        if self.PA_DEX > 10:
            overhead += 10 - self.PA_DEX
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
        self.refresh_degrees_options()
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
        # self.add_missing_root_skills()
        self.reset_total()

    def fix(self, conf=None):
        if self.need_fix:
            self.audit = ""
        super().fix(conf)
        print(f'Fixing {self.full_name}...')
        # self.degrees_wp_choices = {}

        if len(self.bookmark_tag) == 0:
            full_name = self.full_name.replace("'", " ")
            bookmark_tag = ""
            words = full_name.split(" ")
            for word in words:
                if len(word) > 3:
                    bookmark_tag += word[:3]
                else:
                    bookmark_tag += word
            self.bookmark_tag = bookmark_tag.upper()

        if len(self.player) > 0:
            self.audit_log(f"<em>Played by {self.player}</em>")
        from collector.models.profile import Profile
        profiles = Profile.objects.all()
        for p in profiles:
            if p.main_character == self:
                self.player = p.user.username
        if conf is None:
            if self.birthdate < 1000:
                self.birthdate = 5017 - self.birthdate
                self.age = 5017 - self.birthdate
        else:
            if self.birthdate < 1000:
                self.birthdate = conf.epic.era - self.birthdate
                self.age = conf.epic.era - self.birthdate
            if self.birthdate > 4800:
                self.age = conf.epic.era - self.birthdate
        self.fencing_league_special()
        self.occult_special()
        if self.full_name == self.rid:
            self.audit_log("Name is a RID. Everything has to be done on this character.")
        if self.use_history_creation:
            self.audit_log("<strong>History creation</strong>")
            # logger.info('rebuild from lifepath')
            self.rebuild_from_lifepath()
            self.computeDevelopmentPoints()
        else:
            self.audit_log("<strong>Free form</strong>")
            self.rebuild_free_form()
        if self.nameless:
            self.audit_log("<strong>Nameless</strong>")
        a, b = self.tod_done()
        self.lifepath_status = f"{'READY' if a else 'WIP'} / tours_count={b}"
        # Experience check
        self.xp_spent, self.experience_balance = self.check_experience_details()
        self.xp_pool = self.xp_earned - self.xp_spent
        self.calculate_shortcuts()
        self.rank = self.update_ranking()
        self.race = self.specie.species
        if self.PA_BOD != 0:
            if self.height == 0:
                if "urthish" in self.specie.species.lower():
                    self.height = 2.39473 * (self.PA_BOD / 2 + self.PA_STR * 2 + self.PA_CON + 2)  # 145
                    if self.gender == 'male':
                        self.height = self.height + 140
                        self.weight = self.height / (2.8 - 0.07 * (
                                self.PA_BOD + self.PA_STR + self.PA_CON - self.PA_AGI - self.PA_MOV))
                    else:
                        self.height = self.height + 138
                        self.weight = self.height / (2.8 - 0.04 * (
                                self.PA_BOD * 2 - self.PA_STR + 2 * self.PA_CON - self.PA_AGI - 2 * self.PA_MOV))
                    # if self.PA_MOV != self.PA_CON:
                    #     self.weight *= 1 + (self.PA_CON - self.PA_MOV) * 0.1
                    print("Height/Weight Experiment 1: %s --> %0.2f %0.2f BODY:%d CONSTITUTION:%d" % (
                        self.full_name, self.height, self.weight, self.PA_BOD, self.PA_CON))
        self.update_challenge()
        self.update_stories_count()
        self.race = self.specie.species
        self.incomp = 0
        for cyb in self.cyberware_set.all():
            self.incomp += cyb.cyberware_ref.incompatibility
        self.sanity = self.SA_HUM - self.incomp
        if self.historical_figure:
            self.audit_log("Historical figure")
        self.need_fix = False
        logger.info(f'    => Done fixing ...: {self.full_name} NeedFIX:{self.need_fix}')
        self.update_game_parameters()
        print(f'...{self.full_name} fixed.')

    def computeDevelopmentPoints(self):
        total = 0
        for d in self.charactercusto.degreecusto_set.all():
            if d.degree_ref.level == "CO":
                coef = 3
            elif d.degree_ref.level == "RE":
                coef = 4
            elif d.degree_ref.level == "EL":
                coef = 5
            elif d.degree_ref.level == "OB":
                coef = 6
            elif d.degree_ref.level == "FO":
                coef = 7
            else:
                coef = 1000
            total += coef * d.value
            # self.audit_log(f"{d.degree_ref} = {d.value} [{coef * d.value}]")
            # self.audit_log(f"Total Development Points: {total} ")
        self.development_points = total

    def fix75(self):
        """ Fixing skills for the 7.5 version of the rules
        """
        changes = [
            {'skill': 'Surveillance', 'mixes_with': 'Security'},
            {'skill': 'Oratory', 'mixes_with': 'Persuasion'},
            {'skill': 'Cryptography', 'mixes_with': 'Security'},
            {'skill': 'Bribery', 'mixes_with': 'Knavery'},
            {'skill': 'Local Expert (undefined)', 'mixes_with': 'Lore (undefined)'}
        ]
        logger.debug(f"Starting Fix 7.5")
        for s in self.charactercusto.skillcusto_set.all():
            logger.debug(f"SkillCustos: {len(self.charactercusto.skillcusto_set.all())}")
            for c in changes:
                if c['skill'] == s.skill_ref.reference:
                    logger.debug(f"Found skill: {s.skill_ref}")
                    found = False
                    for m in self.charactercusto.skillcusto_set.all():
                        if c['mixes_with'] == m.skill_ref.reference:
                            logger.debug(f"found mixes_with: {m.skill_ref}")
                            logger.debug(f" --- skill value is ........ {s.value}")
                            logger.debug(f" --- mixes_with value is ... {m.value}")
                            m.value += s.value
                            s.value = 0
                            m.save()
                            s.save()
                            s.delete()
                            found = True
                    if not found:
                        from collector.models.skill import SkillCusto, SkillRef
                        m = SkillCusto()
                        m.character_custo = self.charactercusto
                        m.value = s.value
                        m.skill_ref = SkillRef.objects.get(reference=c['mixes_with'])
                        m.save()
                        s.delete()

        logger.info("done")

    def update_challenge(self):
        res = ''
        res += '<i class="fas fa-th-large" title="primary attributes"></i> %d ' % (self.AP)
        res += f'<i class="fas fa-th-list" title="skills"></i> {self.SK_TOTAL}/{self.SWP_tod_pool} '
        res += f'<i class="fas fa-th-list" title="degrees"></i> {self.DE_TOTAL}/{self.DWP_tod_pool} '
        res += '<i class="fas fa-th" title="BC/BA"></i> %d ' % (self.BC_TOTAL + self.BA_TOTAL)
        res += '<i class="fas fa-star" title="wildcards skills"></i> %d ' % (self.SWP_tod_pool)
        res += '<i class="fas fa-star" title="wildcards degrees"></i> %d ' % (self.DWP_tod_pool)
        res += '<i class="fas fa-newspaper" title="OP -vs- LifePath"></i> %d/%d ' % (self.OP, self.life_path_total)
        res += '<i class="fas fa-square" title="exp_bal/xp_spent"></i> %d/%d ' % (
            self.experience_balance, self.xp_spent)
        res += '<i class="fas fa-circle" title="Adjusted"></i> %d ' % (self.OP - self.experience_balance)
        self.challenge_value = self.AP * 3 + self.SK_TOTAL + self.DE_TOTAL + self.BC_TOTAL + self.BA_TOTAL - self.experience_balance
        self.challenge = res

    def update_challenge_pdf(self):
        res = ''
        res += f"Attributes:         {self.AP} (={self.AP * 3} OP); "
        res += f"Skills:                {self.SK_TOTAL} OP; "
        res += f"Degrees:               {self.DE_TOTAL} OP; "
        res += f"Blessings/Curses:      {self.BC_TOTAL} OP; "
        res += f"Benefices/Afflictions: {self.BA_TOTAL}; "
        res += f"OP Difference over Lifepath: {self.OP - self.life_path_total}; "
        res += f"Experience Balance: {self.experience_balance} [{self.xp_earned} | {self.xp_spent} | {self.xp_pool}]"
        return res

    def calculate_shortcuts(self):
        """ Calculate shortcuts for the avatar skills. A shortcut appears if skill.value>0  """
        shortcuts = []
        shortcuts_pdf = []
        shortcuts_json = []
        best_shortcuts_pdf = []
        skills = self.skill_set.all()
        for s in skills:
            sc, pdf = fs_fics7.check_gm_shortcuts(self, s)
            if sc != '':
                shortcuts.append(sc)
                shortcuts_pdf.append(
                    "{:03d}|{:s} ({:s} = {:d})".format(pdf['score'], pdf['rationale'], pdf['label'], pdf['score']))
                shortcuts_json.append({'score': pdf['score'], 'rationale': pdf['rationale'], 'label': pdf['label']})
        self.gm_shortcuts = ''.join(shortcuts)
        shortcuts_pdf.sort(reverse=True)
        shortcuts_pdf_clean = []
        for s in shortcuts_pdf:
            shortcuts_pdf_clean.append(s.split("|")[1])
        self.gm_shortcuts_pdf = "<ul><li>" + '</li><li>'.join(shortcuts_pdf_clean) + "</li></ul>"
        logger.warning(self.gm_shortcuts_pdf)
        result = sorted(shortcuts_json, key=itemgetter('score'), reverse=True)
        # print(result)
        return result

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
                # print(item)
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
        all = SkillRef.objects.exclude(is_wildcard=True).order_by('linked_to', 'reference')
        for s in all:
            if s in sr:
                self.skills_options_not.append(s)
            else:
                self.skills_options.append(s)

    def refresh_degrees_options(self):
        """ This one is special: it only reflects degrees that are not in the character """
        from collector.models.degree import DegreeRef
        self.degrees_options = []
        self.degrees_options_not = []
        ss = self.degree_set.all()
        sr = []
        for x in ss:
            sr.append(x.degree_ref)
        all = DegreeRef.objects.exclude(is_wildcard=True).order_by('group', 'reference')
        for s in all:
            if s in sr:
                self.degrees_options_not.append(s)
            else:
                self.degrees_options.append(s)

    def add_or_update_skill(self, sref, modifier=1):
        from collector.models.skill import Skill
        found_skills = self.skill_set.all().filter(skill_ref=sref)
        if len(found_skills) == 1:
            found_skill = found_skills.first()
            found_skill.value += modifier
            skill = found_skill
        else:
            skill = Skill()
            skill.character = self
            skill.skill_ref = sref
            skill.value = modifier
        skill.save()
        return skill

    def add_or_update_degree(self, dref, modifier=1):
        from collector.models.degree import Degree
        if modifier > 0:
            found_degrees = self.degree_set.all().filter(degree_ref=dref)
            if len(found_degrees) == 1:
                found_degree = found_degrees.first()
                found_degree.value += modifier
                degree = found_degree
            else:
                degree = Degree()
                degree.character = self
                degree.degree_ref = dref
                degree.value = modifier
            degree.save()
            return degree
        else:
            return None

    def remove_or_update_skill(self, askill, modifier=0, stack=False):
        found_skill = self.skill_set.all().filter(skill_ref=askill).first()
        if found_skill:  # There is no reason not to find the skill...
            found_skill.value -= modifier
            found_skill.save()
            if found_skill.value == 0:
                found_skill.delete()

    def remove_or_update_degree(self, adegree, modifier=0, stack=False):
        found_degree = self.degree_set.all().filter(degree_ref=adegree).first()
        if found_degree:  # There is no reason not to find the skill...
            found_degree.value -= modifier
            found_degree.save()
            if found_degree.value == 0:
                found_degree.delete()

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
            item.fix()
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
        return self.rank_name()

    def rank_name(self):
        rank = "Subject of the Empire"
        if self.caste.lower() == "nobility":
            occurences = {}
            for tod in self.tourofduty_set.all():
                for x in ["Li Halan", "Al-Malik", "Decados", "D'Rouge-Glace", "Masseri",
                          "Justinian", "Juandaastas", "Hazat", "Hawkwood", "Torenson",
                          "Van Gelder", "Trusnikron", "Keddah", "Shelit", "Thana", "Xanthippe"
                          ]:
                    if x in tod.tour_of_duty_ref.reference:
                        if x in occurences:
                            occurences[x] += 1
                        else:
                            occurences[x] = 1
            max = -1
            choice = ""
            for k, v in occurences.items():
                if v > max:
                    choice = k
            if self.ranking <= 1:
                rank = "Squire" if not self.gender else "Damsel"
            elif self.ranking <= 3:
                rank = "Knight" if not self.gender else "Consoror"
            elif self.ranking <= 5:
                rank = "Baronnet" if not self.gender else "Baronnet"
            elif self.ranking <= 7:
                rank = "Baron" if not self.gender else "Baronness"
            elif self.ranking <= 9:
                rank = "Marquis" if not self.gender else "Marquise"
            elif self.ranking <= 11:
                rank = "Count" if not self.gender else "Countess"
            elif self.ranking <= 13:
                rank = "Duke" if not self.gender else "Duchess"
            elif self.ranking <= 14:
                rank = "Archduke" if not self.gender else "Archduchess"
            elif self.ranking <= 15:
                rank = "Prince" if not self.gender else "Princess"
        elif self.caste.lower() == "freefolk":
            occurences = {}
            for tod in self.tourofduty_set.all():
                for x in ["Eskatonic Order", "Temple Avesti", "Orthodox", "Sanctuary Aeon", "Brother Battle",
                          "Charioteer", "Scraver", "Reeve", "Engineer", "Muster"
                          ]:
                    if x in tod.tour_of_duty_ref.reference:
                        if x in occurences:
                            occurences[x] += 1
                        else:
                            occurences[x] = 1
            max = -1
            choice = ""
            for k, v in occurences.items():
                if v > max:
                    choice = k
            if choice.lower() == "charioteer":
                if self.ranking <= 3:
                    rank = "Ensign"
                elif self.ranking <= 5:
                    rank = "Lieutenant"
                elif self.ranking <= 7:
                    rank = "Commander"
                elif self.ranking <= 9:
                    rank = "Captain"
                elif self.ranking <= 11:
                    rank = "Consul"
                elif self.ranking <= 13:
                    rank = "Dean"
            elif choice.lower() == "engineer":
                if self.ranking <= 3:
                    rank = "Apprentice"
                elif self.ranking <= 5:
                    rank = "Entered"
                elif self.ranking <= 7:
                    rank = "Fellow"
                elif self.ranking <= 9:
                    rank = "Crafter"
                elif self.ranking <= 11:
                    rank = "Engineer"
                elif self.ranking <= 13:
                    rank = "Master"
            elif choice.lower() == "scraver":
                if self.ranking <= 3:
                    rank = "Associate"
                elif self.ranking <= 5:
                    rank = "Genin"
                elif self.ranking <= 7:
                    rank = "Boss"
                elif self.ranking <= 9:
                    rank = "Jonin"
                elif self.ranking <= 11:
                    rank = "Consul"
                elif self.ranking <= 13:
                    rank = "Dean"
            elif choice.lower() == "muster":
                if self.ranking <= 3:
                    rank = "Private"
                elif self.ranking <= 5:
                    rank = "Sergeant"
                elif self.ranking <= 7:
                    rank = "Lieutenant"
                elif self.ranking <= 9:
                    rank = "Captain"
                elif self.ranking <= 11:
                    rank = "Major"
                elif self.ranking <= 13:
                    rank = "Colonel"
            elif choice.lower() == "reeves":
                if self.ranking <= 3:
                    rank = "Associate"
                elif self.ranking <= 5:
                    rank = "Chief"
                elif self.ranking <= 7:
                    rank = "Manager"
                elif self.ranking <= 9:
                    rank = "Director"
                elif self.ranking <= 11:
                    rank = "Consul"
                elif self.ranking <= 13:
                    rank = "Dean"
            elif choice.lower() == "eskatonic order":
                if self.ranking <= 3:
                    rank = "Novitiate"
                elif self.ranking <= 5:
                    rank = "Provost"
                elif self.ranking <= 7:
                    rank = "Illuminatus"
                elif self.ranking <= 9:
                    rank = "Philosophus"
                elif self.ranking <= 11:
                    rank = "Magister"
                elif self.ranking <= 13:
                    rank = "Presbuteros"
            elif choice.lower() == "brother battle":
                if self.ranking <= 3:
                    rank = "Apprentice"
                elif self.ranking <= 5:
                    rank = "Oblate"
                elif self.ranking <= 7:
                    rank = "Acolyte"
                elif self.ranking <= 9:
                    rank = "Adept"
                elif self.ranking <= 11:
                    rank = "Master"
                elif self.ranking <= 13:
                    rank = "Grand Master"
            elif choice.lower() in ["orthodox", "temple avesti", "sanctuary aeon"]:
                if self.ranking <= 3:
                    rank = "Novitiate"
                elif self.ranking <= 5:
                    rank = "Canon"
                elif self.ranking <= 7:
                    rank = "Deacon"
                elif self.ranking <= 9:
                    rank = "Priest"
                elif self.ranking <= 11:
                    rank = "Bishop"
                elif self.ranking <= 13:
                    rank = "Archbishop"
        return choice + " " + rank

    def add_ba(self, aref, adesc=''):
        from collector.models.benefice_affliction import BeneficeAffliction
        ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref, description=adesc).first()
        if ba:
            return ba
        else:
            desc_list = self.custo_descs.split(';')
            ba = BeneficeAffliction()
            ba.character = self
            ba.benefice_affliction_ref = aref
            desc = adesc
            for d in desc_list:
                if desc == '':
                    w = d.split(':')
                    if str(aref) == w[0]:
                        desc = w[1]
            ba.description = desc
            ba.save()
            return ba

    def remove_ba(self, aref):
        found_ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref).first()
        if found_ba:
            found_ba.delete()

    def add_missing_root_skills(self):
        from collector.models.skill import SkillRef
        roots_list = []
        # for skill in self.skill_set.all():
        #     # if skill.skill_ref.is_speciality:
        #         if not skill.skill_ref.is_wildcard:
        #             roots_list.append(skill.skill_ref.linked_to)
        # for skill in self.skill_set.all():
        #     if skill.skill_ref.is_root:
        #         skill.delete()
        for skill_ref in SkillRef.objects.all():
            if skill_ref in roots_list:
                self.add_or_update_skill(skill_ref, roots_list.count(skill_ref))

    def resetPA(self):
        self.PA_STR = self.PA_CON = self.PA_BOD = self.PA_MOV = self.PA_INT = self.PA_WIL = self.PA_TEM = self.PA_PRE = self.PA_TEC = self.PA_DEX = self.PA_AGI = self.PA_AWA = self.PA_OCC = self.PA_DRK = 0

    @property
    def sumPA(self):
        return self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + self.PA_TEC + self.PA_DEX + self.PA_AGI + self.PA_AWA + self.PA_OCC - self.PA_DRK

    def purge_skills(self):
        for skill in self.skill_set.all():
            skill.delete()

    def purge_degrees(self):
        self.charactercusto.set_degrees_wp_choices({})
        for degree in self.degree_set.all():
            degree.delete()

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
        self.DE_TOTAL = 0
        self.BC_TOTAL = 0
        self.BA_TOTAL = 0
        self.weapon_cost = 0
        self.armor_cost = 0
        self.shield_cost = 0
        self.PA_TOTAL = \
            self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + \
            self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + \
            self.PA_TEC + self.PA_DEX + self.PA_AGI + self.PA_AWA + self.PA_OCC - self.PA_DRK
        skills = self.skill_set.all()
        for s in skills:
            if not s.skill_ref.is_wildcard:
                self.SK_TOTAL += s.value
        degrees = self.degree_set.all()
        for d in degrees:
            if not d.degree_ref.is_wildcard:
                self.DE_TOTAL += d.value
        blessingcurses = self.blessingcurse_set.all()
        for bc in blessingcurses:
            self.BC_TOTAL += bc.blessing_curse_ref.value
        beneficeafflictions = self.beneficeaffliction_set.all()
        for ba in beneficeafflictions:
            self.BA_TOTAL += ba.benefice_affliction_ref.value
        self.AP = self.PA_TOTAL
        self.OP = self.PA_TOTAL * 3 + self.DE_TOTAL + self.SK_TOTAL + self.BC_TOTAL + self.BA_TOTAL
        weapons = self.weapon_set.all()
        for w in weapons:
            self.weapon_cost += w.weapon_ref.cost
        armors = self.armor_set.all()
        for a in armors:
            self.armor_cost += a.armor_ref.price
        shields = self.shield_set.all()
        for s in shields:
            self.shield_cost += s.shield_ref.cost
        return "ok"

    @property
    def extended_skills(self):
        from collector.models.skill import SkillRef
        extended_list = []
        all_skills = SkillRef.objects.filter(is_wildcard=False).values('reference')
        for skill in all_skills:
            extended_list.append({"reference": skill['reference'], "value": 0})
        for s in self.skill_set.all():
            if not s.skill_ref.is_wildcard:
                for extended_skill in extended_list:
                    if extended_skill["reference"] == s.skill_ref.reference:
                        extended_skill["value"] = f"{s.value}"
        print(extended_list)
        return extended_list

    def backup(self):
        proceed = False
        if self.need_pdf:
            from collector.utils.basic import write_pdf
            # try:
            context = dict(c=self, filename=f'{self.rid}', now=datetime.now(tz=get_current_timezone()))
            print(context)
            write_pdf('collector/character_roster.html', context)
            logger.info(f'=> PDF ROSTER created ...: {self.rid}')
            proceed = True
            self.need_pdf = False
            self.save()
            # except:
            #     logger.error(f'    => PDF ROSTER creation error !!! {self.rid}')
        return proceed

    def __str__(self):
        return self.aka

    @property
    def aka(self):
        if self.alias:
            return f'{self.full_name} aka "{self.alias}"'
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
        return round((self.PA_TEC + self.PA_AGI + self.PA_DEX + self.PA_AWA) / 4)

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
        if self.stories_count == 0:
            self.audit_log('Warning: character appears in no cast...')
        else:
            self.audit_log(f'Stories count: {self.stories_count}')
        return self.stories_count

    def update_game_parameters(self):
        self.audit_log("<strong>Others</strong>")
        # Nameless attributes
        self.physical = self.na_phy
        self.mental = self.na_men
        self.combat = self.na_com
        if self.nameless:
            self.audit_log(f"Nameless Attributes: PH:{self.physical}/ME:{self.mental}/CO:{self.combat}")

        # Check for racial tods
        if (self.player == None) and (self.is_locked == False):
            from collector.models.tourofduty import TourOfDutyRef, TourOfDuty
            ra_tod = None
            if self.specie.ra_tod_name:
                ra_tod = TourOfDutyRef.objects.get(reference=self.specie.ra_tod_name)
            for tod in self.tourofduty_set.all():
                if ra_tod != None:
                    if ra_tod.reference == tod.tour_of_duty_ref.reference:
                        ra_tod = None
            if ra_tod != None:
                t = TourOfDuty()
                t.character = self
                t.tour_of_duty_ref = ra_tod
                t.save()
                logger.info(f'    => Added ToD {t} to {self.rid}')
            logger.debug(f'    => Updating Game parameters... ({self.specie.species}, {self.specie.race})')

        self.tod_count = int((self.OP - 240) / 10) + 1
        if self.tod_count < 0:
            self.tod_count = 0

        # Armor stopping power
        SP_grid = {"HE": 0, "TO": 0, "WA": 0, "SA": 0, "WL": 0, "SL": 0, "LW": 0, "RW": 0, "enc": 0}
        for a in self.armor_set.all():
            if a.armor_ref.head:
                SP_grid["HE"] += a.armor_ref.stopping_power
            if a.armor_ref.torso:
                SP_grid["TO"] += a.armor_ref.stopping_power
            if a.armor_ref.weak_leg:
                SP_grid["WL"] += a.armor_ref.stopping_power
            if a.armor_ref.strong_leg:
                SP_grid["WL"] += a.armor_ref.stopping_power
            if a.armor_ref.weak_arm:
                SP_grid["WA"] += a.armor_ref.stopping_power
            if a.armor_ref.strong_arm:
                SP_grid["SA"] += a.armor_ref.stopping_power
            SP_grid["enc"] += a.armor_ref.encumbrance
        # logger.info(SP_grid)
        if len(self.armor_set.all()) == 0:
            self.audit_log("- Warning: character has no armor")
        if len(self.weapon_set.all()) == 0:
            self.audit_log("- Warning: character has no weapon")

    def fencing_league_special(self):
        if self.fencing_league:
            self.audit_log('Fencing league combattant!')
            found_rapier = None
            from collector.models.character_custo import CharacterCusto
            found_custo = CharacterCusto.objects.get(character=self)
            for w in found_custo.weaponcusto_set.filter(weapon_ref__category='MELEE'):
                if w.weapon_ref.meta_type == 'Rapier':
                    found_rapier = w
            if not found_rapier:
                from collector.models.weapon import WeaponCusto, WeaponRef
                found_rapier = WeaponCusto()
                found_rapier.character_custo = found_custo
                found_rapier.weapon_ref = WeaponRef.objects.get(reference='Rapier')
                found_rapier.save()
            found_rapier.weapon_of_choice = True
            found_rapier.save()

            from collector.models.character_custo import CharacterCusto
            found_custo = CharacterCusto.objects.get(character=self)
            armors = found_custo.armorcusto_set.all()
            if len(armors) == 0:
                from collector.models.armor import ArmorCusto, ArmorRef
                found_armor = ArmorCusto()
                found_armor.character_custo = found_custo
                found_armor.armor_ref = ArmorRef.objects.get(reference='Leather Jerkin')
                found_armor.save()

    def occult_special(self):
        if self.PA_OCC > 0:
            self.audit_log('Occultist!')
            from collector.models.ritual import RitualCusto, RitualRef
            from collector.models.character_custo import CharacterCusto
            pathes = []
            total_ritual_levels = 0
            rituals_per_path = self.ritual_set.all().order_by('ritual_ref__path')

            if not len(rituals_per_path):
                if self.caste == 'Church':
                    self.occult = "Theurgy"
                    main_path = self.alliance_ref.common_occult_pathes.split(', ').first()
                else:
                    self.occult = "Psi"
                    common_psi_pathes = ['FarHand', 'Psyche', 'Soma', 'Sixth Sense', 'Vis Craft']
                import random
                main_path = random.choice(common_psi_pathes)
                # found_custo = CharacterCusto.objects.get(character=self)
                # for x in range(self.PA_OCC):
                #     new_power = RitualCusto()
                #     new_power.character_custo = found_custo
                #     new_power.ritual_ref = RitualRef.objects.filter(path=main_path, level=x + 1).first()
                #     new_power.save()
                # @todo

            for r in rituals_per_path:
                if not r.ritual_ref.path in pathes:
                    pathes.append(r.ritual_ref.path)
                total_ritual_levels += r.ritual_ref.level
            self.path = ", ".join(pathes)
            self.occult_fire_power = total_ritual_levels

    def get_specialities(self):
        return []

    def get_shortcuts(self):
        return []

    def to_json(self):
        from collector.utils.basic import json_default
        # self.guideline = self.stats_template
        jstr = json.dumps(self, default=json_default, sort_keys=True, indent=4)
        return jstr

    def to_jsonFICS(self):
        """
        That's what we use to send characters to the front for session_sheet and fics_sheet
        :return: the json structure for the character
        """
        from collector.models.skill import SkillRef
        import datetime
        j = self.to_json()
        # skills

        idx1 = 0
        idx2 = 0
        skills_list = []
        # 1) Add the one you have
        for skill in self.skill_set.order_by('skill_ref'):
            if (skill.skill_ref.is_wildcard == False):
                skills_list.append({'skill': skill.skill_ref.reference, 'value': skill.value, 'idx1': 0, 'idx2': 0})
        # 2) Add the missing one
        for skill in SkillRef.objects.order_by('reference'):
            if (skill.is_wildcard == False):
                if skill.reference not in [value for elem in skills_list for value in elem.values()]:
                    skills_list.append({'skill': skill.reference, 'value': '-', 'idx1': 0, 'idx2': 0})
        skills_list = sorted(skills_list, key=itemgetter('skill'))
        for d in skills_list:
            d['idx1'] = idx1
            idx1 += 1

        # Degrees
        # Add Only the ones you have
        degrees_list = []
        idx = 0
        for degree in self.degree_set.order_by('degree_ref__group', "degree_ref__reference"):
            if not degree.degree_ref.is_wildcard:
                if degree.value > 0:
                    degrees_list.append(
                        {'degree': degree.degree_ref.reference, 'group': degree.degree_ref.get_group_display(),
                         'grp': degree.degree_ref.group,
                         'value': degree.value, 'level': degree.degree_ref.get_level_display(),
                         'lvl': degree.degree_ref.level, 'idx': 0, 'refval': degree.degree_ref.refval,
                         "owner": self.full_name.split(" ")[0]})
        degrees_list = sorted(degrees_list, key=itemgetter('group', 'degree'))
        for d in degrees_list:
            d['idx'] = idx
            d["owner"] = d["owner"] + " " + str(idx)
            idx += 1
        print(degrees_list)

        # Weapons
        weapons = []
        for weapon in self.weapon_set.all():
            weapons.append(weapon.weapon_ref.to_json())
        # Armors
        armors = []
        for armor in self.armor_set.all():
            armors.append(armor.armor_ref.to_json())
        # Shields
        shields = []
        for shield in self.shield_set.all():
            shields.append(shield.shield_ref.to_json())
        # TODS
        tods = []
        for tod in self.tourofduty_set.all():
            tods.append(tod.tour_of_duty_ref.to_json_data())
        # Cyberware
        cyberwares = []
        for cyberware in self.cyberware_set.all():
            cyberwares.append(cyberware.cyberware_ref.to_json_data())

        bcs = []
        # Blessing Curses
        for bc in self.blessingcurse_set.all():
            bcs.append(bc.blessing_curse_ref.to_json())
        bas = []
        # Benefice Affliction
        for ba in self.beneficeaffliction_set.all():
            bas.append(ba.to_json())
        rituals = []
        # Rituals
        for ritual in self.ritual_set.all().order_by('ritual_ref__path', 'ritual_ref__level'):
            rituals.append(ritual.to_json())

        k = json.loads(j)
        k["creature"] = "mortal"
        k["date"] = datetime.datetime.now().strftime('%Y%m%d')
        # from collector.models.alliance_ref import AllianceRef
        a = AllianceRef.fromRID(self.alliance_rid)
        if a:
            alliance = a.reference
        else:
            alliance = "n/a"
        k["alliance"] = alliance
        k["skills_list"] = skills_list
        k["degrees_list"] = degrees_list
        k["pdf_challenge"] = self.update_challenge_pdf()
        k["armors"] = armors
        k["shields"] = shields
        k["weapons"] = weapons
        k["rituals"] = rituals
        k["cyberwares"] = cyberwares
        k["tods"] = sorted(tods, key=itemgetter('category'))
        k["BC"] = bcs
        k["BA"] = bas
        k["shortcuts"] = self.calculate_shortcuts()
        j = json.dumps(k)
        return j

    def to_jsonDECK(self):
        if self.incognito:
            k = {'full_name': self.alias, 'alliance': '?',
                 'alliance_color1': '#ccc', 'alliance_color2': '#ccc',
                 'entrance': self.entrance,
                 'rid': self.rid}
        else:
            k = {'full_name': self.full_name, 'alliance': self.alliance_ref.reference,
                 'alliance_color1': self.alliance_ref.color_front, 'alliance_color2': self.alliance_ref.color_back,
                 'entrance': self.entrance, 'rid': self.rid}
        j = json.dumps(k)
        return j

    @property
    def tod_list_str(self):
        list = []
        for tod in self.tourofduty_set.all().order_by('tour_of_duty_ref__category'):
            list.append(tod.tour_of_duty_ref.reference)
        return ", ".join(list)

    def check_experience_details(self):
        # self.audit_log((f'Experience Computation for {self.full_name}')
        experience = 0
        op = 0
        if self.experience_details:
            self.audit_log(f'<strong>Experience Details</strong>')
            list = self.experience_details.split("; ")
            for entry in list:
                exp = 0
                items = entry.split("=")
                coeff = 1
                coeff_o = 1
                if items[0] == 'PA':
                    coeff = 5
                    coeff_o = 3
                steps = items[2].split(">")
                start = int(steps[0])
                stop = int(steps[1])
                diff = stop - start
                op += diff * coeff_o
                for x in range(start, stop, 1):
                    exp += (x + 1) * coeff
                st = items[2].split(">")
                self.audit_log(
                    f'{items[1]:.>10} from {st[0]} to {st[1]} for {exp:.>3} XP matching {diff * coeff_o:.>3} OP ')
                experience += exp
            self.audit_log(f'Total of {experience} XP matching {op} OP.')
        return experience, op

    @classmethod
    def collect_keywords(cls):
        all = cls.objects.all().values_list("keyword")
        keywords = {}
        for c in all:
            words = c[0].split(",")
            for word in words:
                sanitized_word = word.lstrip().rstrip()
                if sanitized_word not in keywords:
                    keywords[sanitized_word] = 1
                else:
                    keywords[sanitized_word] += 1
        return keywords
