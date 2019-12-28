'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
import hashlib
from scenarist.models.epics import Epic
from collector.models.fics_models import Role, Profile, Specie
from collector.utils import fs_fics7
from collector.utils.basic import write_pdf
#from collector.models.character_custo import CharacterCusto
import logging

logger = logging.getLogger(__name__)


class Character(models.Model):
    pagenum = 0
    full_name = models.CharField(max_length=200)
    rid = models.CharField(max_length=200, default='none')
    alliance = models.CharField(max_length=200, blank=True, default='')
    alliancehash = models.CharField(max_length=200, blank=True, default='none')
    player = models.CharField(max_length=200, default='', blank=True)
    specie = models.ForeignKey(Specie, null=True, default=31, blank=True,
                               on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, null=True, blank=True, default=1,
                             on_delete=models.SET_NULL)
    profile = models.ForeignKey(Profile, null=True, default=1, blank=True,
                                on_delete=models.SET_NULL)
    birthdate = models.IntegerField(default=0)
    gender = models.CharField(max_length=30, default='female')
    native_fief = models.CharField(max_length=200, default='none', blank=True)
    caste = models.CharField(max_length=100, default='Freefolk', blank=True)
    rank = models.CharField(max_length=100, default='', blank=True)
    height = models.IntegerField(default=150)
    weight = models.IntegerField(default=50)
    narrative = models.TextField(default='', blank=True)
    entrance = models.CharField(max_length=100, default='', blank=True)
    keyword = models.CharField(max_length=32, blank=True, default='other')
    stars = models.CharField(max_length=256, blank=True, default='')
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
    age = models.IntegerField(default=0)
    occult_level = models.PositiveIntegerField(default=0)
    occult_darkside = models.PositiveIntegerField(default=0)
    occult = models.CharField(max_length=50, default='', blank=True)
    challenge = models.TextField(default='', blank=True)
    is_exportable = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    is_dead = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    is_partial = models.BooleanField(default=True)
    use_history_creation = models.BooleanField(default=False)
    use_only_entrance = models.BooleanField(default=False)
    epic = models.ForeignKey(Epic, null=True, blank=True, on_delete=models.SET_NULL)
    picture = models.CharField(max_length=256, blank=True, default='')
    alliance_picture = models.CharField(max_length=256, blank=True, default='')
    onsave_reroll_attributes = models.BooleanField(default=False)
    onsave_reroll_skills = models.BooleanField(default=False)
    lifepath_total = models.IntegerField(default=0)
    skills_options = []
    ba_options = []
    bc_options = []
    skills_options_not = []
    ba_options_not = []
    bc_options_not = []
    AP_tod_pool = 0
    OP_tod_pool = 0

    def get_absolute_url(self):
        return reverse('view_character', kwargs={'pk': self.pk})

    def rebuild_from_lifepath(self):
        """ Historical Creation """
        self.resetPA()
        self.purgeSkills()
        self.purgeBC()
        self.purgeBA()
        self.purgeTalents()
        self.AP_tod_pool = 0
        self.OP_tod_pool = 0
        for tod in self.tourofduty_set.all():
            AP, OP = tod.push(self)
            self.AP_tod_pool += AP
            self.OP_tod_pool += OP
        if self.charactercusto:
            self.charactercusto.comment = self.full_name
            self.charactercusto.push(self)
            self.charactercusto.save()
        fs_fics7.check_secondary_attributes(self)
        self.add_missing_root_skills()
        self.lifepath_total = 0
        for tod in self.tourofduty_set.all():
            self.lifepath_total += tod.tour_of_duty_ref.value
        self.refresh_skills_options()
        self.refresh_ba_options()
        self.refresh_bc_options()
        self.charactercusto.save()

    def rebuild_free_form(self):
        """ Freeform Creation """
        self.resetTotal()
        if self.onsave_reroll_attributes:
            fs_fics7.check_primary_attributes(self)
            fs_fics7.check_secondary_attributes(self)
        if self.onsave_reroll_skills:
            fs_fics7.check_skills(self)
        else:
            self.add_missing_root_skills()
            self.resetTotal()

    def fix(self, conf=None):
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
        if self.player == 'none':
            self.player = ''

        if self.use_history_creation:
            self.rebuild_from_lifepath()
        else:
            self.rebuild_free_form()
        gm_shortcuts = ''
        tmp_shortcuts = []
        skills = self.skill_set.all()
        for s in skills:
            sc = fs_fics7.check_gm_shortcuts(self, s)
            if sc != '':
                tmp_shortcuts.append(sc)
        gm_shortcuts = ''.join(tmp_shortcuts)
        gm_shortcuts += fs_fics7.check_attacks(self)
        gm_shortcuts += fs_fics7.check_health(self)
        gm_shortcuts += fs_fics7.check_defense(self)
        if not self.player:
            gm_shortcuts += fs_fics7.check_nameless_attributes(self)
        self.gm_shortcuts = gm_shortcuts
        self.is_exportable = self.check_exportable()
        logger.info('>>> %s %s' % (self.rid, self.is_exportable))

    def apply_racial_pa_mods(self):
        attr_mods = self.specie.get_racial_attr_mod()
        for am in attr_mods:
            v = getattr(self, am)
            setattr(self, am, v+attr_mods[am])

    def refresh_ba_options(self):
        from collector.models.benefice_affliction_ref import BeneficeAfflictionRef
        self.ba_options = []
        self.ba_options_not = []
        ss = self.beneficeaffliction_set.all()
        bar = []
        for x in ss:
            bar.append(x.benefice_affliction_ref)
        all = BeneficeAfflictionRef.objects.all()
        for s in all:
            if s in bar:
                #print("Discarded: "+s.reference)
                self.ba_options_not.append(s)
            else:
                #print(s.reference)
                self.ba_options.append(s)


    def refresh_bc_options(self):
        from collector.models.blessing_curse_ref import BlessingCurseRef
        self.bc_options = []
        self.bc_options_not = []
        bcs = self.blessingcurse_set.all()
        bcr = []
        for x in bcs:
            bcr.append(x.blessing_curse_ref)
        print(bcr)
        all = BlessingCurseRef.objects.all()
        print(all)
        for bc in all:
            if bc in bcr:
                #print("BC Options not...... "+bc.reference)
                self.bc_options_not.append(bc)
            else:
                #print("BC Options.......... "+bc.reference)
                self.bc_options.append(bc)

    def refresh_skills_options(self):
        from collector.models.skill_ref import SkillRef
        self.skills_options = []
        self.skills_options_not = []
        ss = self.skill_set.all()
        sr = []
        for x in ss:
            sr.append(x.skill_ref)
        all = SkillRef.objects.all().exclude(is_root=True)
        for s in all:
            if s in sr:
                #print("Discarded: "+s.reference)
                self.skills_options_not.append(s)
            else:
                self.skills_options.append(s)
                #print(s.reference)


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
        from collector.models.skill import Skill
        found_skill = self.skill_set.all().filter(skill_ref=askill).first()
        if found_skill: # There is no reason not to find the skill...
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
      from collector.models.blessing_curse import BlessingCurse
      found_bc = self.blessingcurse_set.all().filter(blessing_curse_ref=aref).first()
      if found_bc:
        found_bc.delete()


    def add_ba(self, aref):
      from collector.models.benefice_affliction import BeneficeAffliction
      found_ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref).first()
      if found_ba:
        return found_ba
      else:
        ba = BeneficeAffliction()
        ba.character = self
        ba.benefice_affliction_ref = aref
        ba.save()
        return ba

    def remove_ba(self,aref):
      from collector.models.benefice_affliction import BeneficeAffliction
      found_ba = self.beneficeaffliction_set.all().filter(benefice_affliction_ref=aref).first()
      if found_ba:
        found_ba.delete()

    def add_missing_root_skills(self):
        """ According to the character specialities, fixing the root skills """
        #from collector.models.skills import Skill
        from collector.models.skill_ref import SkillRef
        roots_list = []
        for skill in self.skill_set.all():
            if skill.skill_ref.is_speciality:
                roots_list.append(skill.skill_ref.linked_to)
        for skill in self.skill_set.all():
            if skill.skill_ref.is_root:
                skill.delete()
        #self.build_log += (roots_list)
        for skillref in SkillRef.objects.all():
            if skillref in roots_list:
                self.add_or_update_skill(skillref, roots_list.count(skillref))
        for item in roots_list:
            logger.debug('ROOT_LIST:%s' % (item.reference))

    def resetPA(self):
        self.PA_STR = self.PA_CON = self.PA_BOD = self.PA_MOV = self.PA_INT = self.PA_WIL = self.PA_TEM = self.PA_PRE = self.PA_TEC = self.PA_REF = self.PA_AGI = self.PA_AWA =0

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

    def resetTotal(self):
        """ Compute all sums for all stats """
        self.SK_TOTAL = 0
        self.TA_TOTAL = 0
        self.BC_TOTAL = 0
        self.BA_TOTAL = 0
        self.weapon_cost = 0
        self.armor_cost = 0
        self.shield_cost = 0
        self.PA_TOTAL = \
            self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + \
            self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + \
            self.PA_TEC + self.PA_REF + self.PA_AGI + self.PA_AWA
        skills = self.skill_set.all()
        for s in skills:
            if not s.skill_ref.is_root:
                self.SK_TOTAL += s.value
        talents = self.talent_set.all()
        for t in talents:
            self.TA_TOTAL += t.value
        blessingcurses = self.blessingcurse_set.all()
        for bc in blessingcurses:
            self.BC_TOTAL += bc.blessing_curse_ref.value
        beneficeafflictions = self.beneficeaffliction_set.all()
        for ba in beneficeafflictions:
            self.BA_TOTAL += ba.benefice_affliction_ref.value
        self.AP = self.PA_TOTAL
        self.OP = self.PA_TOTAL*3 + self.SK_TOTAL + self.TA_TOTAL + \
            self.BC_TOTAL + self.BA_TOTAL
        weapons = self.weapon_set.all()
        for w in weapons:
            self.weapon_cost += w.weapon_ref.cost
        self.OP += int(self.weapon_cost / 100)
        armors = self.armor_set.all()
        for a in armors:
            self.armor_cost += a.armor_ref.cost
        self.OP += int(self.armor_cost / 100)
        shields = self.shield_set.all()
        for s in shields:
            self.shield_cost += s.shield_ref.cost
        self.OP += int(self.shield_cost / 100)
        return 'ok'

    def check_exportable(self, conf=None):
        """ Is that avatar finished according to the role and profile? """
        exportable = True
        comment = ''
        self.stars = ''
        #self.build_log = ''
        for x in range(1, int(self.role.value)+1):
            self.stars += '<i class="fas fa-star fa-xs"></i>'
        comment += self.resetTotal()
        roleok = fs_fics7.check_role(self)
        self.challenge = fs_fics7.update_challenge(self)
        if not roleok:
            exportable = False
        if self.player != '':
            comment += 'Warning: Players avatars are always exportable...\n'
            exportable = True
        #if comment != '':
        #  self.build_log += comment
        if self.is_exportable != exportable:
            self.is_exportable = exportable
            self.rid = 'none'
        if self.use_history_creation:
            self.is_exportable = True
        return self.is_exportable

    def backup(self):
        """ Transform to PDF if exportable"""
        proceed = self.is_exportable
        if proceed:
            item = self
            context = {'c': item, 'filename': '%s' % (item.rid)}
            write_pdf('collector/character_roster.html', context)
        return proceed

    def __str__(self):
        return '%s' % self.full_name

    def get_rid(self, s):
        self.rid = fs_fics7.find_rid(s)

    # Auto build character
    def autobuild(self):
        if self.role.value == 0 and not self.profile:
            return False
        else:
            return True

    # Save overrride to create custo
    def save(self, force_insert=False, force_update=False):
        from collector.models.character_custo import CharacterCusto
        is_new = self.id is None
        super(Character, self).save(force_insert, force_update)
        if is_new:
            self.custo = CharacterCusto.objects.create(character=self)
        else:
            found_custo = CharacterCusto.objects.filter(character=self).first()
            if found_custo is None:
                self.custo = CharacterCusto.objects.create(character=self)

@receiver(pre_save, sender=Character, dispatch_uid='update_character')
def update_character(sender, instance, conf=None, **kwargs):
    """ Before saving, fix() and  get_RID() for the character """
    if instance.rid != 'none':
        instance.fix(conf)
    instance.get_rid(instance.full_name)
    instance.alliancehash = hashlib.sha1(
            bytes(instance.alliance, 'utf-8')
            ).hexdigest()
    logger.debug('Fix .........: %s' % (instance.full_name))

@receiver(post_save, sender=Character, dispatch_uid='backup_character')
def backup_character(sender, instance, **kwargs):
    """ After saving, create PDF for the character """
    if instance.rid != 'none':
        instance.backup()
