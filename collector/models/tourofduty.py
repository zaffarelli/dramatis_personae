"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.utils import fics_references
from django.contrib import admin
from collector.models.character import Character
from datetime import datetime
from django.utils import timezone


# LIFEPATH_CATEGORY = (
#     ('0', "Birthright"),
#     ('10', "Upbringing"),
#     ('20', "Apprenticeship"),
#     ('30', "Early Career"),
#     ('40', "Tour of Duty"),
#     ('50', "Worldly Benefits"),
#     ('60', "Nameless Kit"),
#     ('70', "Build"),
#     ('80', "Special"),
# )
#
# LIFEPATH_CASTE = (
#     ('Nobility', "Nobility"),
#     ('Church', "Church"),
#     ('Guild', "Guild"),
#     ('Alien', "Alien"),
#     ('Other', "Other"),
#     ('Freefolk', "Freefolk"),
#     ('Think Machine', "Think Machine"),
#     ('Caliphate (PO)', "Kurgan (Planetary Origin)"),
#     ('Caliphate (E)', "Kurgan (Environment)"),
#     ('Caliphate (U)', "Kurgan (Usun)"),
#     ('Barbarian', "Barbarian"),
#     ('Empire', "Empire"),
#     ('Supernatural', "Supernatural"),
# )


class TourOfDutyRef(models.Model):
    class Meta:
        ordering = ['-core','category', 'caste', 'reference']
        verbose_name = "FICS: ToD"

    reference = models.CharField(max_length=64, default='')
    category = models.CharField(max_length=20, choices=fics_references.LIFEPATH_CATEGORY, default='Tour of Duty')
    caste = models.CharField(max_length=20, choices=fics_references.LIFEPATH_CASTE, default='Other')
    topic = models.CharField(max_length=64, default='', blank=True)
    source = models.CharField(max_length=32, default='FS2CRB', choices=fics_references.SOURCE_REFERENCES)
    is_custom = models.BooleanField(default=False)
    need_fix = models.BooleanField(default=False, blank=True)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
    balance_AP = models.IntegerField(default=0)
    balance_OP = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    PA_STR = models.IntegerField(default=0)
    PA_CON = models.IntegerField(default=0)
    PA_BOD = models.IntegerField(default=0)
    PA_MOV = models.IntegerField(default=0)
    PA_INT = models.IntegerField(default=0)
    PA_WIL = models.IntegerField(default=0)
    PA_TEM = models.IntegerField(default=0)
    PA_PRE = models.IntegerField(default=0)
    PA_REF = models.IntegerField(default=0)
    PA_TEC = models.IntegerField(default=0)
    PA_AGI = models.IntegerField(default=0)
    PA_AWA = models.IntegerField(default=0)
    OCC_LVL = models.IntegerField(default=0)
    OCC_DRK = models.IntegerField(default=0)
    WP = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    description = models.TextField(max_length=1024, default='', blank=True)
    valid = models.BooleanField(default=False)
    # pub_date = models.DateTimeField('Date published', default=timezone.now)
    core = models.BooleanField(default=True)

    def __str__(self):
        # str = f'[{self.get_category_display()}][{self.value}] ({self.get_caste_display()}|{self.topic}) {self.reference} '
        str = f'[{self.get_category_display()}: {self.value}] {self.reference} {"(C)" if self.core else ""}'
        return str

    def fix(self):
        self.WP = 0
        if self.is_custom:
            self.value = self.AP * 3 + self.OP
        else:
            self.fix75()
            self.AP = self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + self.PA_REF + self.PA_TEC + self.PA_AGI + self.PA_AWA + self.OCC_LVL - self.OCC_DRK
            self.OP = 0
            texts = []
            if self.PA_STR != 0:
                texts.append("STR %+d" % (self.PA_STR))
            if self.PA_CON != 0:
                texts.append("CON %+d" % (self.PA_CON))
            if self.PA_BOD != 0:
                texts.append("BOD %+d" % (self.PA_BOD))
            if self.PA_MOV != 0:
                texts.append("MOV %+d" % (self.PA_MOV))
            if self.PA_INT != 0:
                texts.append("INT %+d" % (self.PA_INT))
            if self.PA_WIL != 0:
                texts.append("WIL %+d" % (self.PA_WIL))
            if self.PA_TEM != 0:
                texts.append("TEM %+d" % (self.PA_TEM))
            if self.PA_PRE != 0:
                texts.append("PRE %+d" % (self.PA_PRE))
            if self.PA_REF != 0:
                texts.append("REF %+d" % (self.PA_REF))
            if self.PA_TEC != 0:
                texts.append("TEC %+d" % (self.PA_TEC))
            if self.PA_AGI != 0:
                texts.append("AGI %+d" % (self.PA_AGI))
            if self.PA_AWA != 0:
                texts.append("AWA %+d" % (self.PA_AWA))
            if self.OCC_LVL != 0:
                texts.append("OCC %+d" % (self.OCC_LVL))
            if self.OCC_DRK != 0:
                texts.append("DRK %+d" % (self.OCC_DRK))
            for s in self.skillmodificator_set.all():
                texts.append("{%s %+d}" % (s.skill_ref.reference, s.value))
                if s.skill_ref.is_wildcard:
                    self.WP += s.value
                if not s.skill_ref.is_root:
                    self.OP += s.value
            for bc in self.blessingcursemodificator_set.all():
                texts.append("(%s %+d)" % (bc.blessing_curse_ref.reference, bc.blessing_curse_ref.value))
                self.OP += bc.blessing_curse_ref.value
            for ba in self.beneficeafflictionmodificator_set.all():
                texts.append("(%s %+d)" % (ba.benefice_affliction_ref.reference, ba.benefice_affliction_ref.value))
                self.OP += ba.benefice_affliction_ref.value
            self.description = " ".join(texts)
            self.value = (self.AP + self.balance_AP) * 3 + (self.OP + self.balance_OP)
            self.check_value()

        self.need_fix = False

    def fix75(self):
        """ Fixing skills for the 7.5 version of the rules
        """
        changes = [
            {'skill': 'Surveillance', 'mixes_with': 'Security', 'exclude': []},
            {'skill': 'Oratory', 'mixes_with': 'Persuasion', 'exclude': []},
            {'skill': 'Cryptography', 'mixes_with': 'Security', 'exclude': []},
            {'skill': 'Bribery', 'mixes_with': 'Knavery', 'exclude': []},
            {'skill': 'Local Expert (undefined)', 'mixes_with': 'Lore (undefined)', 'exclude': []},
            {'skill': 'Linguistics (Urthish)', 'mixes_with': 'Linguistics (undefined)', 'exclude': ['0']}
        ]
        for s in self.skillmodificator_set.all():
            print(f"Category: {self.category}")
            for c in changes:
                print(f"Found change {c['skill']}")
                if self.category not in c['exclude']:
                    if c['skill'] == s.skill_ref.reference:

                        found = False
                        for m in self.skillmodificator_set.all():
                            if c['mixes_with'] == m.skill_ref.reference:
                                print("found mixes_with:", s.skill_ref)
                                print(" --- skill value is ........ ", s.value)
                                print(" --- mixes_with value is ... ", m.value)
                                m.value += s.value
                                s.value = 0
                                m.save()
                                s.save()
                                s.delete()
                                found = True
                        if not found:
                            from collector.models.skill import SkillModificator, SkillRef
                            m = SkillModificator()
                            m.tour_of_duty_ref = self
                            m.value = s.value
                            m.skill_ref = SkillRef.objects.get(reference=c['mixes_with'])
                            m.save()
                            s.delete()
                else:
                    print(f"--> Change NOT Applicable")
        print("done")

    def check_value(self):
        self.valid = False
        if self.category == '0':  # Birthright
            self.balance = 200 - self.value
            self.valid = True
        elif self.category == '5':  # Balance
            self.valid = True
        elif self.category == '10':  # Upbringing
            if self.caste == 'Caliphate (PO)':
                self.valid = self.value == 3
                self.topic = ''
            elif self.caste == 'Caliphate (E)':
                self.valid = self.value == 8
                self.topic = ''
            elif self.caste == 'Caliphate (U)':
                self.valid = self.value == 9
                self.topic = ''
            else:
                self.valid = self.value in [5, 15, 20]
        elif self.category == '20':  # Apprenticeship
            self.valid = self.value == 25
        elif self.category == '30':  # Early Career
            self.valid = self.value == 48
        elif self.category == '40':  # Tour of Duty
            self.valid = (self.value % 10 == 0)
        elif self.category == '50':  # Worldly Benefits
            self.valid = (self.value == 7)
        elif self.category == '60':  # Nameless kit
            self.valid = True
        elif self.category == '70':  # Build
            self.valid = True
        elif self.category == '80':  # Custom
            self.valid = True
        else:
            self.valid = False

    def to_json(self):
        from collector.utils.basic import json_default
        import json
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class TourOfDuty(models.Model):
    class Meta:
        ordering = ['character', 'tour_of_duty_ref']

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.tour_of_duty_ref.reference)

    def push(self, ch):
        ranking = 0
        tod = self.tour_of_duty_ref
        AP = 0
        OP = 0
        WP = 0
        wp_roots = []
        if tod.is_custom:
            AP = tod.AP
            OP = tod.OP
        else:
            ch.PA_STR += tod.PA_STR
            ch.PA_CON += tod.PA_CON
            ch.PA_BOD += tod.PA_BOD
            ch.PA_MOV += tod.PA_MOV
            ch.PA_INT += tod.PA_INT
            ch.PA_WIL += tod.PA_WIL
            ch.PA_TEM += tod.PA_TEM
            ch.PA_PRE += tod.PA_PRE
            ch.PA_REF += tod.PA_REF
            ch.PA_TEC += tod.PA_TEC
            ch.PA_AGI += tod.PA_AGI
            ch.PA_AWA += tod.PA_AWA
            ch.OCC_LVL += tod.OCC_LVL
            ch.OCC_DRK += tod.OCC_DRK
            for sm in tod.skillmodificator_set.all():
                if not sm.skill_ref.is_wildcard:
                    ch.add_or_update_skill(sm.skill_ref, sm.value, True)
                else:
                    WP += sm.value
                    wp_roots.append(sm.skill_ref.linked_to.reference)
            # for bc in tod.blessingcursemodificator_set.all():
            #     ch.add_bc(bc.blessing_curse_ref)
            # print(tod)
            for ba in tod.beneficeafflictionmodificator_set.all():
                ch.add_ba(ba.benefice_affliction_ref)
        AP += tod.balance_AP
        OP += tod.balance_OP
        return AP, OP, WP, wp_roots


class TourOfDutyInline(admin.TabularInline):
    model = TourOfDuty
    extras = 3
    ordering = ['tour_of_duty_ref']
