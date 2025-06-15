from django.db import models
from collector.utils import fics_references
from django.contrib import admin
from collector.models.character import Character
from datetime import datetime
from collector.mixins.ridded_mixin import RiddedMixin, RidField
import json


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


class TourOfDutyRef(RiddedMixin):
    class Meta:
        ordering = ['category', 'caste', 'reference']
        verbose_name = "FICS: ToD"

    reference = models.CharField(max_length=64, default='')
    category = models.CharField(max_length=20, choices=fics_references.LIFEPATH_CATEGORY, default='Tour of Duty')
    caste = models.CharField(max_length=20, choices=fics_references.LIFEPATH_CASTE, default='Other')
    topic = models.CharField(max_length=64, default='', blank=True)
    subtopic = models.CharField(max_length=64, default='', blank=True)
    source = models.CharField(max_length=32, default='FS2CRB', choices=fics_references.SOURCE_REFERENCES)
    is_custom = models.BooleanField(default=True)
    need_fix = models.BooleanField(default=False, blank=True)
    AP = models.IntegerField(default=0)
    SK = models.IntegerField(default=0)
    DE = models.IntegerField(default=0)
    BC = models.IntegerField(default=0)
    BA = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
    WP = models.IntegerField(default=0)
    SWP = models.IntegerField(default=0, blank=True) # Skill Wilcard Points
    DWP = models.IntegerField(default=0, blank=True) # Skill Degree Points
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
    PA_DEX = models.IntegerField(default=0)
    PA_TEC = models.IntegerField(default=0)
    PA_AGI = models.IntegerField(default=0)
    PA_AWA = models.IntegerField(default=0)
    PA_OCC = models.IntegerField(default=0, blank=True)
    PA_DRK = models.IntegerField(default=0, blank=True)

    value = models.IntegerField(default=0)
    description = models.TextField(max_length=1024, default='', blank=True)
    notes = models.TextField(max_length=1024, default='', blank=True)
    valid = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField('Date published', default=datetime.now)
    core = models.BooleanField(default=True)
    is_kit = models.BooleanField(default=False, blank=True)
    is_public = models.BooleanField(default=True, blank=True)
    skill_modificators_summary = models.TextField(max_length=1024, default="", blank=True)
    degree_modificators_summary = models.TextField(max_length=1024, default="", blank=True)
    beneficeaffliction_modificators_summary = models.TextField(max_length=1024, default="", blank=True)
    blessingcurse_modificators_summary = models.TextField(max_length=1024, default="", blank=True)
    degrees_wp_choices = models.TextField(max_length=2048, default="{}", blank=True)
    skills_wp_choices = models.TextField(max_length=2048, default="{}", blank=True)

    @classmethod
    def validity(cls):
        import math
        all = cls.objects.all()
        valid_ones = cls.objects.filter(valid=True)
        return f'INFO: Valid ToDs = {len(valid_ones)} of {len(all)} [{math.floor(len(valid_ones) / len(all) * 1000) / 10}%]'

    def __str__(self):
        return f'[{self.get_category_display()} / {self.get_caste_display()}] {self.reference} '

    def fix(self):
        def getAttribute(suffix, report_list):
            val = getattr(self, "PA_" + suffix.upper())
            if self.category in ["10", "20"]:
                if val > 1:
                    val = 1
                    setattr(self, "PA_" + suffix.upper(), val)
            if val != 0:
                report_list.append(f'{suffix}{val:+}'.upper())
            return val

        def getFromList(items, report_list, ref):
            total = 0
            wp_total = 0
            for item in items:
                r = getattr(item, ref)
                if r:
                    if hasattr(item, "value"):
                        report_list.append(f'{r.reference}{item.value:+}')
                        if hasattr(r, "is_wildcard"):
                            if getattr(r, "is_wildcard"):
                                wp_total += item.value
                            else:
                                total += item.value
                        else:
                            total += item.value
                    else:
                        if hasattr(r, "value"):
                            report_list.append(f'{r.reference}{r.value:+}')
                            total += r.value
                        else:
                            report_list.append(f'{r.reference}')
            return total, wp_total

        self.toRID(f"{self.caste}_{self.category}_{self.reference}", prefix="TOD_", cypher=True)

        if self.is_custom:
            # All skills and degrees are wildcards in a custom ToD...
            if self.DWP == 0 and self.DE > 0:
                self.DWP = self.DE
                self.DE = 0
            if self.SWP == 0 and self.SK > 0:
                self.SWP = self.SK
                self.SK = 0
            self.OP = self.DWP + self.SWP + self.BC + self.BA
            self.value = self.AP * 3 + self.OP
            self.WP = self.DWP + self.SWP
        else:
            self.AP = 0
            self.OP = 0
            self.WP = 0
            self.SK = 0
            self.DE = 0
            self.BA = 0
            self.BC = 0
            self.SWP = 0
            self.DWP = 0
            texts = []
            # Attributes
            attributes = ["str", "con", "bod", "mov", "int", "wil", "tem", "pre", "dex", "tec", "agi", "awa", "occ",
                          "drk"]
            hrlist_attributes = []
            for attribute in attributes:
                self.AP += getAttribute(attribute, hrlist_attributes)
            # if len(hrlist_attributes) == 0:
            #     hrlist_attributes = ["Attributes: None"]
            if len(hrlist_attributes) > 0:
                texts.append("Attributes: " + ", ".join(hrlist_attributes))

            # SKILLS
            hrlist_skills = []
            items = self.skillmodificator_set.all()
            self.SK, self.SWP = getFromList(items, hrlist_skills, "skill_ref")
            #print(hrlist_skills, self.SP)
            self.skill_modificators_summary = "Skills: "
            if len(hrlist_skills) > 0:
                hrlist_skills.sort()
                self.skill_modificators_summary += ", ".join(hrlist_skills)
            else:
                self.skill_modificators_summary = ""

            # DEGREES
            hrlist_degrees = []
            items = self.degreemodificator_set.all()
            self.DE, self.DWP = getFromList(items, hrlist_degrees, "degree_ref")
            self.degree_modificators_summary = "Degrees: "
            if len(hrlist_degrees) > 0:
                hrlist_degrees.sort()
                self.degree_modificators_summary += ", ".join(hrlist_degrees)
            else:
                self.degree_modificators_summary = ""
            degrees_wp_choices = {}
            for dm in items:
                if dm.degree_ref.is_wildcard:
                    if dm.degree_ref.reference not in degrees_wp_choices:
                        degrees_wp_choices[dm.degree_ref.reference] = {'value':0,'list':[],"fulfilled":0}

                    wclist = dm.degree_ref.as_wildcard_of.split(", ")
                    for x in wclist:
                        if x not in degrees_wp_choices[dm.degree_ref.reference]['list']:
                            degrees_wp_choices[dm.degree_ref.reference]['list'].append(x)
                    degrees_wp_choices[dm.degree_ref.reference]['value'] += dm.value
                else:
                    print(f"Forget about {dm.degree_ref}, this is no wildcard.")
            print(f"WILDCARDS: [ToD={self.reference}]: {degrees_wp_choices}")
            self.degrees_wp_choices = json.dumps(degrees_wp_choices)

            self.WP = self.SWP + self.DWP

            # BLESSINGS/CURSES
            hrlist_bc = []
            items = self.blessingcursemodificator_set.all()
            self.BC, _ = getFromList(items, hrlist_bc, "blessing_curse_ref")
            self.blessingcurse_modificators_summary = "Blessing/Curses: "
            if len(hrlist_bc) > 0:
                hrlist_bc.sort()
                self.blessingcurse_modificators_summary += ", ".join(hrlist_bc)
            else:
                self.blessingcurse_modificators_summary = ""
            # BENEFICES/AFFLICTIONS
            hrlist_ba = []
            items = self.beneficeafflictionmodificator_set.all()
            self.BA, _ = getFromList(items, hrlist_ba, "benefice_affliction_ref")
            self.beneficeaffliction_modificators_summary = "Benefices/Afflictions: "
            if len(hrlist_ba) > 0:
                hrlist_ba.sort()
                self.beneficeaffliction_modificators_summary += ", ".join(hrlist_ba)
            else:
                self.beneficeaffliction_modificators_summary = ""
            # BUILD DESCRIPTION
            if len(self.skill_modificators_summary) > 0:
                texts.append(self.skill_modificators_summary)
            if len(self.degree_modificators_summary) > 0:
                texts.append(self.degree_modificators_summary)
            if len(self.beneficeaffliction_modificators_summary) > 0:
                texts.append(self.beneficeaffliction_modificators_summary)
            if len(self.blessingcurse_modificators_summary) > 0:
                texts.append(self.blessingcurse_modificators_summary)
            self.OP = self.SK + self.DE + self.BC + self.BA + self.WP
            self.value = (self.AP + self.balance_AP) * 3 + (self.OP + self.balance_OP)
            #texts.append(f"AP:{self.AP}({self.AP*3}) OP:{self.OP} WP:{self.WP}  SK:{self.SK} DE:{self.DE}  BC:{self.BC} BA:{self.BA} SWP:{self.SWP} DWP:{self.DWP} = {self.value}")
            self.description = "; ".join(texts)
            self.check_value()
            print(self.__class__.validity())
        self.need_fix = False

    # def fix75(self):
    #     """ Fixing skills for the 7.5 version of the rules
    #     """
    #     changes = [
    #         {'skill': 'Surveillance', 'mixes_with': 'Security'},
    #         {'skill': 'Oratory', 'mixes_with': 'Persuasion'},
    #         {'skill': 'Cryptography', 'mixes_with': 'Security'},
    #         {'skill': 'Bribery', 'mixes_with': 'Knavery'},
    #         {'skill': 'Local Expert (undefined)', 'mixes_with': 'Lore (undefined)'}
    #     ]
    #     for s in self.skillmodificator_set.all():
    #         for c in changes:
    #             if c['skill'] == s.skill_ref.reference:
    #                 print("found skill", s.skill_ref)
    #                 found = False
    #                 for m in self.skillmodificator_set.all():
    #                     if c['mixes_with'] == m.skill_ref.reference:
    #                         print("found mixes_with:", s.skill_ref)
    #                         print(" --- skill value is ........ ", s.value)
    #                         print(" --- mixes_with value is ... ", m.value)
    #                         m.value += s.value
    #                         s.value = 0
    #                         m.save()
    #                         s.save()
    #                         s.delete()
    #                         found = True
    #                 if not found:
    #                     from collector.models.skill import SkillModificator, SkillRef
    #                     m = SkillModificator()
    #                     m.tour_of_duty_ref = self
    #                     m.value = s.value
    #                     m.skill_ref = SkillRef.objects.get(reference=c['mixes_with'])
    #                     m.save()
    #                     s.delete()
    #
    #     print("done")

    def check_value(self):
        self.valid = False
        if self.category == '0':  # Birthright
            self.balance = 120 - self.value
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
            elif self.caste in ['Nobility','Alien']:
                self.valid = self.value == 20
            else:
                self.valid = self.value in [15, 5]
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
        json_string = json.dumps(self, default=json_default, sort_keys=True, indent=4)
        json_data = json.loads(json_string)
        return json_data, json_string

    def to_json_data(self):
        from collector.utils.basic import json_default
        import json
        json_string = json.dumps(self, default=json_default, sort_keys=True, indent=4)
        json_data = json.loads(json_string)
        shortcut_words = self.get_category_display().split(" ")
        shortcut = "".join([z[0] for z in shortcut_words]).upper()
        json_data["category_text"] = shortcut
        return json_data

    def to_json_str(self):
        from collector.utils.basic import json_default
        import json
        json_string = json.dumps(self, default=json_default, sort_keys=True, indent=4)
        # json_data = json.loads(json_string)
        return json_string


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
        SK = 0
        DE = 0
        BC = 0
        BA = 0
        SWP = 0
        DWP = 0
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
            ch.PA_DEX += tod.PA_DEX
            ch.PA_TEC += tod.PA_TEC
            ch.PA_AGI += tod.PA_AGI
            ch.PA_AWA += tod.PA_AWA
            ch.PA_OCC += tod.PA_OCC
            ch.PA_DRK += tod.PA_DRK
            # All AP
            AP = tod.PA_STR + tod.PA_CON + tod.PA_BOD + tod.PA_MOV
            AP += tod.PA_INT + tod.PA_WIL + tod.PA_TEM + tod.PA_PRE
            AP += tod.PA_DEX + tod.PA_TEC + tod.PA_AGI + tod.PA_AWA
            AP += tod.PA_OCC - tod.PA_DRK
            # Skills Modificators
            for sm in tod.skillmodificator_set.all():
                if not sm.skill_ref.is_wildcard:
                    ch.add_or_update_skill(sm.skill_ref, sm.value)
                    SK += sm.value
                else:
                    SWP += sm.value
            # Degrees Modificators
            for dm in tod.degreemodificator_set.all():
                if not dm.degree_ref.is_wildcard:
                    ch.add_or_update_degree(dm.degree_ref, dm.value)
                    DE += dm.value
                else:
                    DWP += dm.value
            # Blessings/Curses
            for bc in tod.blessingcursemodificator_set.all():
                ch.add_bc(bc.blessing_curse_ref)
                BC += bc.blessing_curse_ref.value
            # Benefices/Afflictions
            for ba in tod.beneficeafflictionmodificator_set.all():
                ch.add_ba(ba.benefice_affliction_ref)
                BA += ba.benefice_affliction_ref.value
        #AP += tod.balance_AP
        #OP += tod.balance_OP
            OP = SK + DE + BC + BA

        return AP, OP, SWP, DWP, SK, DE, BC, BA


class TourOfDutyInline(admin.TabularInline):
    model = TourOfDuty
    extras = 3
    ordering = ['tour_of_duty_ref']
