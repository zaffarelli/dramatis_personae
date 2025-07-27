from django.db import models
from collector.utils import fics_references
from django.contrib import admin
from collector.models.character import Character
from datetime import datetime
from collector.mixins.ridded_mixin import RiddedMixin, RidField
from collector.utils.allocator import Allocator
import json

GLOBAL_WILDCARDS = "Global Wildcards"


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
    AP = models.IntegerField(default=0, blank=True)
    SP = models.IntegerField(default=0, blank=True)
    DP = models.IntegerField(default=0, blank=True)
    BC = models.IntegerField(default=0, blank=True)
    BA = models.IntegerField(default=0, blank=True)
    OP = models.IntegerField(default=0, blank=True)

    AWP = models.IntegerField(default=0, blank=True)  # Attribute wildcard point C1P, etc...
    SWP = models.IntegerField(default=0, blank=True)  # Skill Wilcard Points
    DWP = models.IntegerField(default=0, blank=True)  # Degree Wildcard Points
    BCW = models.IntegerField(default=0, blank=True)
    BAW = models.IntegerField(default=0, blank=True)
    balance_AP = models.IntegerField(default=0)
    balance_OP = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)
    PA_STR = models.IntegerField(default=0, blank=True)
    PA_CON = models.IntegerField(default=0, blank=True)
    PA_BOD = models.IntegerField(default=0, blank=True)
    PA_MOV = models.IntegerField(default=0, blank=True)
    PA_INT = models.IntegerField(default=0, blank=True)
    PA_WIL = models.IntegerField(default=0, blank=True)
    PA_TEM = models.IntegerField(default=0, blank=True)
    PA_PRE = models.IntegerField(default=0, blank=True)
    PA_DEX = models.IntegerField(default=0, blank=True)
    PA_TEC = models.IntegerField(default=0, blank=True)
    PA_AGI = models.IntegerField(default=0, blank=True)
    PA_AWA = models.IntegerField(default=0, blank=True)
    PA_OCC = models.IntegerField(default=0, blank=True)
    PA_DRK = models.IntegerField(default=0, blank=True)

    # Meeaning: Choose 1 from Physical, Mental, Combat and Full
    PA_C1P = models.IntegerField(default=0, blank=True)
    PA_C1M = models.IntegerField(default=0, blank=True)
    PA_C1C = models.IntegerField(default=0, blank=True)
    PA_C1F = models.IntegerField(default=0, blank=True)

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
    degrees_wp_choices = models.TextField(max_length=4096, default="{}", blank=True)
    skills_wp_choices = models.TextField(max_length=4096, default="{}", blank=True)
    ba_wp_choices = models.TextField(max_length=4096, default="{}", blank=True)
    bc_wp_choices = models.TextField(max_length=4096, default="{}", blank=True)
    stored_allocator = models.TextField(max_length=1024, default='', blank=True)

    @classmethod
    def validity(cls):
        import math
        all = cls.objects.all()
        valid_ones = cls.objects.filter(valid=True)
        return f'INFO: Valid ToDs = {len(valid_ones)} of {len(all)} [{math.floor(len(valid_ones) / len(all) * 1000) / 10}%]'

    def get_wildcard_choices(self, kind):
        data = f"{kind}_wp_choices"
        if hasattr(self, data):
            return json.loads(getattr(self, data))
        else:
            return {}

    def set_wildcard_choices(self, kind, x):
        data = f"{kind}_wp_choices"
        if hasattr(self, data):
            setattr(self, data, json.dumps(x, indent=4, sort_keys=True))

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

        def create_choices_list(self, stored_choices, items, source_prop):
            choice_list = {}
            for item in items:
                if hasattr(item, source_prop):
                    it = getattr(item, source_prop)
                    if it.is_wildcard:
                        if it.group_wildcard:
                            if it.reference not in choice_list:
                                choice_list[it.reference] = {'value': 0, 'list': [], "fulfilled": 0}
                            wclist = it.as_wildcard_of.split(", ")
                            for x in wclist:
                                if x not in choice_list[it.reference]['list']:
                                    choice_list[it.reference]['list'].append(x)
                            choice_list[it.reference]['value'] += item.value
                        else:
                            if GLOBAL_WILDCARDS in choice_list:
                                choice_list[GLOBAL_WILDCARDS]['value'] += item.value
                            else:
                                choice_list[GLOBAL_WILDCARDS] = {'value': item.value, "list": [], "fulfilled": 0}
            setattr(self, stored_choices, json.dumps(choice_list))

        self.toRID(f"{self.caste}_{self.category}_{self.reference}", prefix="TOD_", cypher=True)
        self.OP = 0
        self.AP = 0
        self.SP = 0
        self.DP = 0
        self.BA = 0
        self.BC = 0
        self.value = 0
        if self.is_custom:
            # All skills and degrees are wildcards in a custom ToD...
            self.value = self.AWP + self.SWP + self.DWP + self.BAW + self.BCW
            self.OP = 0
            items = self.skillmodificator_set.all()
            if len(items) != 1:
                from collector.models.skill import SkillModificator, SkillRef
                self.skillmodificator_set.all().delete()
                skill = SkillModificator()
                skill.tour_of_duty_ref = self
                skill.skill_ref = SkillRef.objects.filter(is_wildcard=True, group_wildcard=False).first()
                skill.value = self.SWP
                skill.save()
            items = self.degreemodificator_set.all()
            if len(items) != 1:
                from collector.models.degree import DegreeModificator, DegreeRef
                self.degreemodificator_set.all().delete()
                deg = DegreeModificator()
                deg.tour_of_duty_ref = self
                deg.degree_ref = DegreeRef.objects.filter(is_wildcard=True, group_wildcard=False).first()
                deg.value = self.DWP
                deg.save()
            # # SKILLS
            # hrlist_skills = []
            # items = self.skillmodificator_set.all()
            # self.SK, self.SWP = getFromList(items, hrlist_skills, "skill_ref")
            # # print(hrlist_skills, self.SP)
            # self.skill_modificators_summary = "Skills: "
            # if len(hrlist_skills) > 0:
            #     hrlist_skills.sort()
            #     self.skill_modificators_summary += ", ".join(hrlist_skills)
            # else:
            #     self.skill_modificators_summary = ""
            #
            # # SKILL CHOICES
            # skills_wp_choices = {}
            # for sm in items:
            #     if sm.skill_ref.is_wildcard:
            #         if sm.skill_ref.reference not in skills_wp_choices:
            #             skills_wp_choices[sm.skill_ref.reference] = {'value': 0, 'list': [], "fulfilled": 0}
            #         wclist = sm.skill_ref.as_wildcard_of.split(", ")
            #         for x in wclist:
            #             if x not in skills_wp_choices[sm.skill_ref.reference]['list']:
            #                 skills_wp_choices[sm.skill_ref.reference]['list'].append(x)
            #         skills_wp_choices[sm.skill_ref.reference]['value'] += sm.value
            #     else:
            #         print(f"Forget about {sm.skill_ref}, this is no wildcard.")
            # # print(f"WILDCARDS (Skills): [ToD={self.reference}]: {skills_wp_choices}")
            # self.skills_wp_choices = json.dumps(skills_wp_choices)
            #
            # # DEGREES
            # hrlist_degrees = []
            # items = self.degreemodificator_set.all()
            # self.DE, self.DWP = getFromList(items, hrlist_degrees, "degree_ref")
            # self.degree_modificators_summary = "Degrees: "
            # if len(hrlist_degrees) > 0:
            #     hrlist_degrees.sort()
            #     self.degree_modificators_summary += ", ".join(hrlist_degrees)
            # else:
            #     self.degree_modificators_summary = ""
            #
            # # DEGREE CHOICES
            # degrees_wp_choices = {}
            # for dm in items:
            #     if dm.degree_ref.is_wildcard:
            #         if dm.degree_ref.reference not in degrees_wp_choices:
            #             degrees_wp_choices[dm.degree_ref.reference] = {'value': 0, 'list': [], "fulfilled": 0}
            #         wclist = dm.degree_ref.as_wildcard_of.split(", ")
            #         for x in wclist:
            #             if x not in degrees_wp_choices[dm.degree_ref.reference]['list']:
            #                 degrees_wp_choices[dm.degree_ref.reference]['list'].append(x)
            #         degrees_wp_choices[dm.degree_ref.reference]['value'] += dm.value
            #     else:
            #         print(f"Forget about {dm.degree_ref}, this is no wildcard.")
            # #print(f"WILDCARDS (Degrees): [ToD={self.reference}]: {degrees_wp_choices}")
            # self.degrees_wp_choices = json.dumps(degrees_wp_choices)
        else:
            self.AWP = 0
            self.SWP = 0
            self.DWP = 0
            self.BAW = 0
            self.BCW = 0

            texts = []
            # ATTRIBUTES
            attributes = ["str", "con", "bod", "mov", "int", "wil", "tem", "pre", "dex", "tec", "agi", "awa", "occ",
                          "drk"]
            hrlist_attributes = []
            for attribute in attributes:
                self.AP += getAttribute(attribute, hrlist_attributes)
            if len(hrlist_attributes) > 0:
                texts.append("Attributes: " + ", ".join(hrlist_attributes))

            # BLESSINGS/CURSES (BCW should not be affected by lists)
            hrlist_bc = []
            items = self.blessingcursemodificator_set.all()
            self.BC, _ = getFromList(items, hrlist_bc, "blessing_curse_ref")
            self.blessingcurse_modificators_summary = "Blessing/Curses: "
            if len(hrlist_bc) > 0:
                hrlist_bc.sort()
                self.blessingcurse_modificators_summary += ", ".join(hrlist_bc)
            else:
                self.blessingcurse_modificators_summary = ""
            # BENEFICES/AFFLICTIONS (BAW should not be affected by lists)
            hrlist_ba = []
            items = self.beneficeafflictionmodificator_set.all()
            self.BA, _ = getFromList(items, hrlist_ba, "benefice_affliction_ref")
            self.beneficeaffliction_modificators_summary = "Benefices/Afflictions: "
            if len(hrlist_ba) > 0:
                hrlist_ba.sort()
                self.beneficeaffliction_modificators_summary += ", ".join(hrlist_ba)
            else:
                self.beneficeaffliction_modificators_summary = ""
            # SKILLS
            hrlist_skills = []
            items = self.skillmodificator_set.all()
            self.SP, self.SWP = getFromList(items, hrlist_skills, "skill_ref")
            self.skill_modificators_summary = "Skills: "
            if len(hrlist_skills) > 0:
                hrlist_skills.sort()
                self.skill_modificators_summary += ", ".join(hrlist_skills)
            else:
                self.skill_modificators_summary = ""
            create_choices_list(self, "skills_wp_choices", items, "skill_ref")
            # DEGREES
            hrlist_degrees = []
            items = self.degreemodificator_set.all()
            self.DP, self.DWP = getFromList(items, hrlist_degrees, "degree_ref")
            self.degree_modificators_summary = "Degrees: "
            if len(hrlist_degrees) > 0:
                hrlist_degrees.sort()
                self.degree_modificators_summary += ", ".join(hrlist_degrees)
            else:
                self.degree_modificators_summary = ""
            create_choices_list(self, "degrees_wp_choices", items, "degree_ref")
            # Common ground custom or not
            self.AWP = self.PA_C1P + self.PA_C1M + self.PA_C1C + self.PA_C1F
            # BUILD DESCRIPTION
            if len(self.skill_modificators_summary) > 0:
                texts.append(self.skill_modificators_summary)
            if len(self.degree_modificators_summary) > 0:
                texts.append(self.degree_modificators_summary)
            if len(self.beneficeaffliction_modificators_summary) > 0:
                texts.append(self.beneficeaffliction_modificators_summary)
            if len(self.blessingcurse_modificators_summary) > 0:
                texts.append(self.blessingcurse_modificators_summary)
            self.description = "&#013;".join(texts)

        # self.value = (self.AP + self.AWP) * 3 \
        #              + self.DWP + self.DP \
        #              + self.SWP + self.SP \
        #              + self.BC + self.BCW \
        #              + self.BA + self.BAW
        # self.OP = self.DP + self.SP + self.BC + self.BA + self.AP * 3
        # Allocations
        a = Allocator()
        # a.restore(self.stored_allocator)
        a.set(self.AP, "fixed", "AP")
        a.set(self.DP, "fixed", "DP")
        a.set(self.SP, "fixed", "SP")
        a.set(self.BA, "fixed", "BA")
        a.set(self.BC, "fixed", "BC")
        a.set(self.AWP, "wildcard", "AP")
        a.set(self.DWP, "wildcard", "DP")
        a.set(self.SWP, "wildcard", "SP")
        a.set(self.BAW, "wildcard", "BA")
        a.set(self.BCW, "wildcard", "BC")
        a.check()
        self.stored_allocator = a.as_string
        self.OP = self.SP + self.DP + self.BC + self.BA + self.AP * 3
        self.value = self.OP + self.AWP * 3 + self.BAW + self.BCW + self.DWP + self.SWP
        self.check_value()
        print(self.__class__.validity())
        self.need_fix = False

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
            elif self.caste in ['Nobility', 'Alien']:
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
        ordering = ['character', 'ref']

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    OP = models.IntegerField(default=0, blank=True)

    def push(self, ch):
        cc = self.character.cc
        tod = self.ref
        AP = SP = DP = BA = BC = 0
        AWP = SWP = DWP = BAW = BCW = 0
        self.OP = tod.OP
        if tod.is_custom:
            AWP = tod.AWP
            SWP = tod.SWP
            DWP = tod.DWP
            BAW = tod.BAW
            BCW = tod.BCW
        else:
            # All AP
            AP = tod.PA_STR + tod.PA_CON + tod.PA_BOD + tod.PA_MOV
            AP += tod.PA_INT + tod.PA_WIL + tod.PA_TEM + tod.PA_PRE
            AP += tod.PA_DEX + tod.PA_TEC + tod.PA_AGI + tod.PA_AWA
            AP += tod.PA_OCC + tod.PA_DRK

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

            AWP += tod.PA_C1P + tod.PA_C1M + tod.PA_C1C + tod.PA_C1F

            # Skills Modificators
            for sm in tod.skillmodificator_set.all():
                if not sm.skill_ref.is_wildcard:
                    SP += sm.value
                    ch.add_or_update_skill(sm.skill_ref, sm.value)
                else:
                    SWP += sm.value
            # Degrees Modificators
            for dm in tod.degreemodificator_set.all():
                if not dm.degree_ref.is_wildcard:
                    DP += dm.value
                    ch.add_or_update_degree(dm.degree_ref, dm.value)
                else:
                    DWP += dm.value
            # Benefices/Afflictions
            for ba in tod.beneficeafflictionmodificator_set.all():
                if not ba.benefice_affliction_ref.is_wildcard:
                    BA += ba.benefice_affliction_ref.value
                else:
                    BAW += ba.benefice_affliction_ref.value
            # Blessings/Curses
            for bc in tod.blessingcursemodificator_set.all():
                if not bc.blessing_curse_ref.is_wildcard:
                    BC += bc.blessing_curse_ref.value
                else:
                    BCW += bc.blessing_curse_ref.value

        TOD_VALUE = (AP + AWP) * 3 + SP + DP + BA + BC + SWP + DWP + BCW + BAW
        a = Allocator()
        a.restore(cc.stored_allocator)
        a.stack(AP, "fixed", "AP")
        a.stack(SP, "fixed", "SP")
        a.stack(DP, "fixed", "DP")
        a.stack(BA, "fixed", "BA")
        a.stack(BC, "fixed", "BC")
        a.stack(AWP, "wildcard", "AP")
        a.stack(SWP, "wildcard", "SP")
        a.stack(DWP, "wildcard", "DP")
        a.stack(BAW, "wildcard", "BA")
        a.stack(BCW, "wildcard", "BC")
        a.stack(AP, "allocated", "AP")
        a.stack(SP, "allocated", "SP")
        a.stack(DP, "allocated", "DP")
        a.stack(BA, "allocated", "BA")
        a.stack(BC, "allocated", "BC")
        a.check()
        cc.AP += AP
        cc.SP += SP
        cc.DP += DP
        cc.BA += BA
        cc.BC += BC
        cc.stored_allocator = a.as_string
        # Check all wildcard systems
        systems = ["degrees", "skills", "ba", "bc"]
        for system in systems:
            cc_data = cc.get_wildcard_choices(system)
            elements = tod.get_wildcard_choices(system)
            for k, v in elements.items():
                if k in cc_data:
                    cc_data[k]['value'] += v["value"]
                    cc_data[k]['fulfilled'] = 0
                else:
                    cc_data[k] = {"value": v["value"], "list": v["list"], "fulfilled": 0}
            cc.set_wildcard_choices(system, cc_data)

        trace_str = ""
        trace_str += f"{tod.PA_STR}>{ch.PA_STR:02} "
        trace_str += f"{tod.PA_CON}>{ch.PA_CON:02} "
        trace_str += f"{tod.PA_BOD}>{ch.PA_BOD:02} "
        trace_str += f"{tod.PA_MOV}>{ch.PA_MOV:02} "
        trace_str += f"{tod.PA_INT}>{ch.PA_INT:02} "
        trace_str += f"{tod.PA_WIL}>{ch.PA_WIL:02} "
        trace_str += f"{tod.PA_TEM}>{ch.PA_TEM:02} "
        trace_str += f"{tod.PA_PRE}>{ch.PA_PRE:02} "
        trace_str += f"{tod.PA_TEC}>{ch.PA_TEC:02} "
        trace_str += f"{tod.PA_DEX}>{ch.PA_DEX:02} "
        trace_str += f"{tod.PA_AGI}>{ch.PA_AGI:02} "
        trace_str += f"{tod.PA_AWA}>{ch.PA_AWA:02} "

        print(f"{tod.reference:30} OP={self.OP:3}/{TOD_VALUE}")
        print(f'=> {tod.reference:30} {trace_str}')
        return tod.value

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.tour_of_duty_ref.reference)


class TourOfDutyInline(admin.TabularInline):
    model = TourOfDuty
    extras = 3
    ordering = ['ref']
