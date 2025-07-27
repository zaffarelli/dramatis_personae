"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import json

from collector.utils.allocator import Allocator


class CharacterCusto(models.Model):
    class Meta:
        verbose_name = "FICS: Character Customization"

    from collector.models.character import Character
    character = models.OneToOneField(Character, related_name="cc", on_delete=models.CASCADE, primary_key=True)
    # value = models.IntegerField(default=0, blank=True)
    OP = models.IntegerField(default=0, blank=True)
    AP = models.IntegerField(default=0, blank=True)
    SP = models.IntegerField(default=0, blank=True)
    DP = models.IntegerField(default=0, blank=True)
    BA = models.IntegerField(default=0, blank=True)
    BC = models.IntegerField(default=0, blank=True)

    PA_STR = models.PositiveIntegerField(default=0)
    PA_CON = models.PositiveIntegerField(default=0)
    PA_BOD = models.PositiveIntegerField(default=0)
    PA_MOV = models.PositiveIntegerField(default=0)
    PA_INT = models.PositiveIntegerField(default=0)
    PA_WIL = models.PositiveIntegerField(default=0)
    PA_TEM = models.PositiveIntegerField(default=0)
    PA_PRE = models.PositiveIntegerField(default=0)
    PA_DEX = models.PositiveIntegerField(default=0)
    PA_TEC = models.PositiveIntegerField(default=0)
    PA_AGI = models.PositiveIntegerField(default=0)
    PA_AWA = models.PositiveIntegerField(default=0)
    summary = models.TextField(default='')
    PA_OCC = models.PositiveIntegerField(default=0)
    PA_DRK = models.PositiveIntegerField(default=0)

    PA_C1P = models.PositiveIntegerField(default=0)
    PA_C1M = models.PositiveIntegerField(default=0)
    PA_C1C = models.PositiveIntegerField(default=0)
    PA_C1F = models.PositiveIntegerField(default=0)

    comment = models.TextField(default="")
    watch_roots = models.TextField(default="", blank=True)
    wp_used = models.PositiveIntegerField(default=0)
    degree_wp_watch = {}

    degrees_wp_choices_str = models.TextField(default='{}', max_length=4096, blank=True)
    skills_wp_choices_str = models.TextField(default='{}', max_length=4096, blank=True)
    ba_wp_choices_str = models.TextField(default='{}', max_length=4096, blank=True)
    bc_wp_choices_str = models.TextField(default='{}', max_length=4096, blank=True)

    stored_allocator = models.TextField(max_length=4096, default='', blank=True)
    need_fix = models.BooleanField(default=False)

    def get_degrees_wp_choices(self):
        return json.loads(self.degrees_wp_choices_str)

    def set_degrees_wp_choices(self, x):
        self.degrees_wp_choices_str = json.dumps(x, indent=4, sort_keys=True)

    def get_skills_wp_choices(self):
        return json.loads(self.skills_wp_choices_str)

    def set_skills_wp_choices(self, x):
        self.skills_wp_choices_str = json.dumps(x, indent=4, sort_keys=True)

    def get_wildcard_choices(self, kind):
        data = f"{kind}_wp_choices_str"
        if hasattr(self, data):
            return json.loads(getattr(self, data))
        else:
            return {}

    def set_wildcard_choices(self, kind, x):
        data = f"{kind}_wp_choices_str"
        if hasattr(self, data):
            setattr(self, data, json.dumps(x, indent=4, sort_keys=True))

    def cleanup(self):
        self.OP = 0
        self.AP = 0
        self.SP = 0
        self.DP = 0
        self.BA = 0
        self.BC = 0
        self.set_degrees_wp_choices({})
        self.set_skills_wp_choices({})
        for s in self.skillcusto_set.all():
            if s.value <= 0:
                s.delete()
        for d in self.degreecusto_set.all():
            if d.value <= 0:
                d.delete()

    def fix(self):
        from collector.utils.allocator import Allocator
        self.cleanup()
        a = Allocator()
        a.restore(self.stored_allocator)
        # Attributes
        self.AP += self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV
        self.AP += self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE
        self.AP += self.PA_DEX + self.PA_TEC + self.PA_AGI + self.PA_AWA
        self.AP += self.PA_OCC + self.PA_DRK
        a.stack(self.AP, "allocated", "AP")
        self.OP += self.AP * 3
        # Skills
        for s in self.skillcusto_set.all():
            self.OP += s.value
            self.SP += s.value
        a.stack(self.SP, "allocated", "SP")
        # Degrees
        for d in self.degreecusto_set.all():
            self.OP += d.value
            self.DP += d.value
        a.stack(self.DP, "allocated", "DP")
        # Benefices/Afflictions
        for ba in self.beneficeafflictioncusto_set.all():
            self.OP += ba.benefice_affliction_ref.value
            self.BA += ba.benefice_affliction_ref.value
        a.stack(self.BA, "allocated", "BA")
        # Blessings/Curses
        for bc in self.blessingcursecusto_set.all():
            self.OP += bc.blessing_curse_ref.value
            self.BC += bc.blessing_curse_ref.value
        a.stack(self.BC, "allocated", "BC")
        a.check()
        self.stored_allocator = a.as_string
        self.rebuild_summary()
        self.need_fix = False

    def initialize_computation(self):
        """
        Set all metrics to 0.
        :return:
        """
        from collector.utils.allocator import Allocator
        a = Allocator()
        a.prune_all()
        self.stored_allocator = ""
        self.AP = 0
        self.SP = 0
        self.DP = 0
        self.BA = 0
        self.BC = 0


        self.OP = 0
        # Check all wildcard systems
        systems = ["degrees", "skills", "ba", "bc"]
        for system in systems:
            self.set_wildcard_choices(system, {})
        # self.need_fix = False
        # self.save()
        # self.need_fix = True

    def push(self, ch):
        """
        Push the CC data to the character
        :return:
        """
        # from collector.models.character import Character
        # ch = Character.objects.filter(id=self.character.id).first()
        # STR = ch.PA_STR + self.PA_STR
        # CON = ch.PA_CON + self.PA_CON
        # BOD = ch.PA_BOD + self.PA_BOD
        # MOV = ch.PA_MOV + self.PA_MOV
        # INT = ch.PA_INT + self.PA_INT
        # WIL = ch.PA_WIL + self.PA_WIL
        # TEM = ch.PA_TEM + self.PA_TEM
        # PRE = ch.PA_PRE + self.PA_PRE
        # DEX = ch.PA_DEX + self.PA_DEX
        # TEC = ch.PA_TEC + self.PA_TEC
        # AGI = ch.PA_AGI + self.PA_AGI
        # AWA = ch.PA_AWA + self.PA_AWA
        # OCC = ch.PA_OCC + self.PA_OCC
        # DRK = ch.PA_DRK + self.PA_DRK

        a = Allocator()
        a.restore(self.stored_allocator)

        ch.PA_STR += self.PA_STR
        ch.PA_CON += self.PA_CON
        ch.PA_BOD += self.PA_BOD
        ch.PA_MOV += self.PA_MOV
        ch.PA_INT += self.PA_INT
        ch.PA_WIL += self.PA_WIL
        ch.PA_TEM += self.PA_TEM
        ch.PA_PRE += self.PA_PRE
        ch.PA_DEX += self.PA_DEX
        ch.PA_TEC += self.PA_TEC
        ch.PA_AGI += self.PA_AGI
        ch.PA_AWA += self.PA_AWA
        ch.PA_OCC += self.PA_OCC
        ch.PA_DRK += self.PA_DRK

        self.AP = self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE + self.PA_DEX + self.PA_TEC + self.PA_AGI + self.PA_AWA + self.PA_OCC + self.PA_DRK

        # Skills Custo
        skills_wp_choices = self.get_skills_wp_choices()
        for sc in self.skillcusto_set.all():
            for k, v in skills_wp_choices.items():
                if sc.skill_ref.reference in v['list']:
                    v['fulfilled'] += sc.value
                if v['value'] < v['fulfilled']:
                    v['fulfilled'] = v['value']
            self.SP += sc.value
            ch.add_or_update_skill(sc.skill_ref, sc.value)
        # Degrees Custo
        degrees_wp_choices = self.get_degrees_wp_choices()
        for dc in self.degreecusto_set.all():
            for k, v in degrees_wp_choices.items():
                if dc.degree_ref.reference in v['list']:
                    v['fulfilled'] += dc.value
                if v['value'] < v['fulfilled']:
                    v['fulfilled'] = v['value']
            self.DP += dc.value
            ch.add_or_update_degree(dc.degree_ref, dc.value)
        self.set_degrees_wp_choices(degrees_wp_choices)

        # Blessings/Curses
        for bc in self.blessingcursecusto_set.all():
            self.BC += bc.blessing_curse_ref.value
            ch.add_bc(bc.blessing_curse_ref)
        # Benefices/Afflictions
        for ba in self.beneficeafflictioncusto_set.all():
            self.BA += ba.benefice_affliction_ref.value
            ch.add_ba(ba.benefice_affliction_ref, ba.description)
        # Weapons
        for weapon in self.weaponcusto_set.all():
            ch.add_weapon(weapon.weapon_ref)
        # Add a dirk to all Fencing League Participants
        if ch.fencing_league:
            if len(self.weaponcusto_set.all()) == 0:
                from collector.models.weapon import WeaponRef
                dirk = WeaponRef.objects.get(reference='Dirk')
                ch.add_weapon(dirk)
        # Armors
        for armor in self.armorcusto_set.all():
            ch.add_armor(armor.armor_ref)
        # Shields
        for shield in self.shieldcusto_set.all():
            ch.add_shield(shield.shield_ref)
        # Rituals
        for ritual in self.ritualcusto_set.all():
            ch.add_ritual(ritual.ritual_ref)

        ch.AP += self.AP
        ch.SP += self.SP
        ch.DP += self.DP
        ch.BA += self.BA
        ch.BC += self.BC
        ch.OP += self.AP * 3 + self.SP + self.DP + self.BA + self.BC
        trace_str = ""
        trace_str += f"{self.PA_STR}>{ch.PA_STR:02} "
        trace_str += f"{self.PA_CON}>{ch.PA_CON:02} "
        trace_str += f"{self.PA_BOD}>{ch.PA_BOD:02} "
        trace_str += f"{self.PA_MOV}>{ch.PA_MOV:02} "
        trace_str += f"{self.PA_INT}>{ch.PA_INT:02} "
        trace_str += f"{self.PA_WIL}>{ch.PA_WIL:02} "
        trace_str += f"{self.PA_TEM}>{ch.PA_TEM:02} "
        trace_str += f"{self.PA_PRE}>{ch.PA_PRE:02} "
        trace_str += f"{self.PA_TEC}>{ch.PA_TEC:02} "
        trace_str += f"{self.PA_DEX}>{ch.PA_DEX:02} "
        trace_str += f"{self.PA_AGI}>{ch.PA_AGI:02} "
        trace_str += f"{self.PA_AWA}>{ch.PA_AWA:02} "
        print(f'=> {"CC":30} {trace_str}')

    # return STR,CON,BOD,MOV,INT,WIL,TEM,PRE,TEC,DEX,AGI,AWA, OCC, DRK

    def rebuild_summary(self):
        from collector.utils.allocator import Allocator
        a = Allocator()
        a.restore(self.stored_allocator)
        self.summary = ""
        self.summary += "<b>Allocation</b><br/>"
        self.summary += a.toSummary()
        self.summary += "<hr/>"
        self.summary += "Attributes"
        self.summary += "<ul>"
        if self.PA_STR != 0:
            self.summary += "<li>STR %d</li>" % (self.PA_STR)
        if self.PA_CON != 0:
            self.summary += "<li>CON %d</li>" % (self.PA_CON)
        if self.PA_BOD != 0:
            self.summary += "<li>BOD %d</li>" % (self.PA_BOD)
        if self.PA_MOV != 0:
            self.summary += "<li>MOV %d</li>" % (self.PA_MOV)
        if self.PA_INT != 0:
            self.summary += "<li>INT %d</li>" % (self.PA_INT)
        if self.PA_WIL != 0:
            self.summary += "<li>WIL %d</li>" % (self.PA_WIL)
        if self.PA_TEM != 0:
            self.summary += "<li>TEM %d</li>" % (self.PA_TEM)
        if self.PA_PRE != 0:
            self.summary += "<li>PRE %d</li>" % (self.PA_PRE)
        if self.PA_DEX != 0:
            self.summary += "<li>DEX %d</li>" % (self.PA_DEX)
        if self.PA_TEC != 0:
            self.summary += "<li>TEC %d</li>" % (self.PA_TEC)
        if self.PA_AGI != 0:
            self.summary += "<li>AGI %d</li>" % (self.PA_AGI)
        if self.PA_AWA != 0:
            self.summary += "<li>AWA %d</li>" % (self.PA_AWA)
        self.summary += "</ul>"
        self.summary += "Occult"
        self.summary += "<ul>"
        if self.PA_OCC != 0:
            self.summary += "<li>Lightside %d</li>" % (self.PA_OCC)
        if self.PA_DRK != 0:
            self.summary += "<li>Darkside  %d</li>" % (self.PA_DRK)
        self.summary += "</ul>"
        self.summary += "<hr/>"
        self.summary += "Wildcards"
        self.summary += "<ul>"
        for system in ["skills", "degrees", "ba", "bc"]:
            self.summary += f'<li>{system.title()} Wildcards:</li>'
            data = self.get_wildcard_choices(system)
            if data != {}:
                self.summary += "<ul>"
                for k, v in data.items():
                    self.summary += f"<li>{k} => {v["fulfilled"]}/{v["value"]} pts</li>"
                self.summary += "</ul>"
        self.summary += "</ul>"
        self.summary += "<hr/>"
        self.summary += "Skills"
        self.summary += "<ul>"
        for s in self.skillcusto_set.all():
            self.summary += "<li>%s +%d</li>" % (s.skill_ref.reference, s.value)
        self.summary += "</ul>"
        self.summary += "Degrees"
        self.summary += "<ul>"
        for d in self.degreecusto_set.all():
            self.summary += f"<li>{d.degree_ref.reference} {d.value:+}</li>"
        self.summary += "</ul>"
        self.summary += "Blessings/Curses"
        self.summary += "<ul>"
        for bc in self.blessingcursecusto_set.all():
            self.summary += "<li>%s %+d</li>" % (bc.blessing_curse_ref.reference, bc.blessing_curse_ref.value)
        self.summary += "</ul>"
        self.summary += "Benefices/Afflictions"
        self.summary += "<ul>"
        for ba in self.beneficeafflictioncusto_set.all():
            self.summary += "<li>%s %+d</li>" % (ba.benefice_affliction_ref.reference, ba.benefice_affliction_ref.value)
        self.summary += "</ul>"
        self.summary += "Weapons"
        self.summary += "<ul>"
        for item in self.weaponcusto_set.all():
            self.summary += "<li>%s</li>" % (item.weapon_ref.reference)
        self.summary += "</ul>"
        self.summary += "Armors"
        self.summary += "<ul>"
        for item in self.armorcusto_set.all():
            self.summary += "<li>%s</li>" % (item.armor_ref.reference)
        self.summary += "</ul>"
        self.summary += "Shields"
        self.summary += "<ul>"
        for item in self.shieldcusto_set.all():
            self.summary += "<li>%s</li>" % (item.shield_ref.reference)
        self.summary += "</ul>"
        self.summary += "Rituals"
        self.summary += "<ul>"
        for item in self.ritualcusto_set.all():
            self.summary += "<li>%s</li>" % (item.ritual_ref.reference)
        self.summary += "</ul>"

    def add_or_update_skill(self, item, modifier=1):
        from collector.models.skill import SkillCusto
        elements = self.skillcusto_set.filter(skill_ref=item)
        if len(elements) == 1:
            element = elements.first()
        else:
            element = SkillCusto()
            element.character_custo = self
            element.skill_ref = item
            element.value = 0
        if 0 <= element.value + modifier < 21:
            element.value += modifier
            element.save()

    def add_or_update_degree(self, item, modifier=1):
        from collector.models.degree import DegreeCusto
        elements = self.degreecusto_set.filter(degree_ref=item)
        if len(elements) == 1:
            element = elements.first()
        else:
            element = DegreeCusto()
            element.character_custo = self
            element.degree_ref = item
            element.value = 0
        if 0 <= element.value + modifier < 4:
            element.value += modifier
            element.save()
