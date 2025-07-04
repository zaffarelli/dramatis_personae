"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import json


class CharacterCusto(models.Model):
    class Meta:
        verbose_name = "FICS: Character Customization"

    from collector.models.character import Character
    character = models.OneToOneField(Character, on_delete=models.CASCADE, primary_key=True)
    value = models.IntegerField(default=0)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
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
    comment = models.TextField(default="")
    watch_roots = models.TextField(default="", blank=True)
    wp_used = models.PositiveIntegerField(default=0)
    degree_wp_watch = {}
    degrees_wp_choices_str = models.TextField(default='{}', max_length=2048, blank=True)
    stored_allocator = models.TextField(max_length=1024, default='', blank=True)

    # attributes_to_allocate = models.PositiveIntegerField(default=0)
    # skills_to_allocate = models.PositiveIntegerField(default=0)
    # degrees_to_allocate = models.PositiveIntegerField(default=0)
    #
    # allocated_attributes = models.PositiveIntegerField(default=0)
    # allocated_skills = models.PositiveIntegerField(default=0)
    # allocated_degrees = models.PositiveIntegerField(default=0)


    def get_degrees_wp_choices(self):
        return json.loads(self.degrees_wp_choices_str)

    def set_degrees_wp_choices(self, x):
        self.degrees_wp_choices_str = json.dumps(x, indent=4, sort_keys=True)

    # def reset_allocated(self):
    #     self.allocated_attributes = 0
    #     self.allocated_degrees = 0
    #     self.allocated_skills = 0

    def recalculate(self):
        """
        All manually added changes are recalculated here.
        :return:
        """
        from collector.utils.allocator import Allocator
        # Clean ups
        for s in self.skillcusto_set.all():
            if s.value <= 0:
                s.delete()
        for d in self.degreecusto_set.all():
            if d.value <= 0:
                d.delete()
        a = Allocator()
        a.restore(self.stored_allocator)
        self.AP = 0
        self.OP = 0
        self.SP = 0
        self.DP = 0
        self.BA = 0
        self.BC = 0
        self.AP += (self.PA_STR + self.PA_CON + self.PA_BOD + self.PA_MOV
                    + self.PA_INT + self.PA_WIL + self.PA_TEM + self.PA_PRE
                    + self.PA_DEX + self.PA_TEC + self.PA_AGI + self.PA_AWA
                    )
        self.AP += (self.PA_OCC + self.PA_DRK)
        a.set(self.AP,"allocated","AP")
        for s in self.skillcusto_set.all():
            self.OP += s.value
            self.SP += s.value
        a.set(self.SP, "allocated", "SP")
        for d in self.degreecusto_set.all():
            self.OP += d.value
            self.DP += d.value
        a.set(self.DP, "allocated", "DP")
        for bc in self.blessingcursecusto_set.all():
            self.OP += bc.blessing_curse_ref.value
            self.BC += bc.blessing_curse_ref.value
        a.set(self.BC, "allocated", "BC")
        for ba in self.beneficeafflictioncusto_set.all():
            self.OP += ba.benefice_affliction_ref.value
            self.BA += bc.benefice_affliction_ref.value
        a.set(self.BA, "allocated", "BA")
        self.value = self.AP * 3 + self.OP
        self.stored_allocator = a.as_string
        self.rebuild_summary()

    def rebuild_summary(self):
        from collector.utils.allocator import Allocator
        a = Allocator()
        a.restore(self.stored_allocator)

        self.summary = ""
        self.summary += "<b>Allocation</b>"
        self.summary += "<ul>"
        self.summary += a.toSummary()
        self.summary += "</ul>"
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
        self.summary += "Wildcards"
        self.summary += "<ul>"
        self.summary += f'<li>WP used: {self.wp_used}</li>'
        self.summary += f'<li>ToD Skills WP: {self.character.SWP_tod_pool}</li>'
        self.summary += f'<li>ToD Degrees WP: {self.character.DWP_tod_pool}</li>'

        data = self.get_degrees_wp_choices()
        if data != {}:
            self.summary += "<ul>"
            for k, v in data.items():
                self.summary += f"<li>{k} => {v["fulfilled"]}/{v["value"]} pts</li>"
            self.summary += "</ul>"

        # self.summary += f'<li>WP roots: {self.watch_roots}</li>'
        self.summary += "</ul>"
        self.summary += "Skills"
        self.summary += "<ul>"
        for s in self.skillcusto_set.all():
            # if s.skill_ref.is_root == False:
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

    def push(self, ch):
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


        # Skills Custo
        for sc in self.skillcusto_set.all():
            ch.add_or_update_skill(sc.skill_ref, sc.value)
        # Degrees Custo
        # self.degree_wp_watch = {}
        degrees_wp_choices = self.get_degrees_wp_choices()
        for dc in self.degreecusto_set.all():
            for k, v in degrees_wp_choices.items():
                if dc.degree_ref.reference in v['list']:
                    v['fulfilled'] += dc.value
                if v['value'] < v['fulfilled']:
                    v['fulfilled'] = v['value']
            ch.add_or_update_degree(dc.degree_ref, dc.value)
        self.set_degrees_wp_choices(degrees_wp_choices)


        # Blessings/Curses
        for bc in self.blessingcursecusto_set.all():
            ch.add_bc(bc.blessing_curse_ref)
        # Benefices/Afflictions
        for ba in self.beneficeafflictioncusto_set.all():
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

    def add_or_update_skill(self, skill_ref_id, value):
        from collector.models.skill import SkillCusto, SkillRef
        found_in_custo = False
        found_cu = None
        for found_cu in self.skillcusto_set.all():
            if found_cu.skill_ref.id == skill_ref_id:
                found_in_custo = True
                break
        if found_in_custo:
            found_cu.value += int(value)
            found_cu.save()
        else:
            skill_custo = SkillCusto()
            skill_custo.skill_ref = SkillRef.objects.get(pk=skill_ref_id)
            if (int(value) > 0):
                skill_custo.value = int(value)
                skill_custo.character_custo = self
                skill_custo.save()

    def add_or_update_degree(self, degree_ref_id, value=1):
        """
        Used when interracting through the mobile form to add new degree custo to the custo
        :param degree_ref_id:
        :param value:
        :return:
        """
        from collector.models.degree import DegreeCusto, DegreeRef
        found_in_custo = False
        v = int(value)
        found_cu = None
        for found_cu in self.degreecusto_set.all():
            if found_cu.degree_ref.id == degree_ref_id:
                found_in_custo = True
                break
        if found_in_custo:
            found_cu.value += v
            found_cu.save()
        else:
            degree_custo = DegreeCusto()
            degree_custo.degree_ref = DegreeRef.objects.get(pk=degree_ref_id)
            degree_custo.value = v
            degree_custo.character_custo = self
            degree_custo.save()

    def register_tod_wp(self, str):
        import json
        degrees_wp_choices = self.get_degrees_wp_choices()
        tod_dwpc = json.loads(str)
        for k, v in tod_dwpc.items():
            if k in degrees_wp_choices:
                degrees_wp_choices[k]['value'] += v["value"]
                degrees_wp_choices[k]['fulfilled'] = 0
            else:
                degrees_wp_choices[k] = {"value": v["value"], "list": v["list"], "fulfilled": 0}
        self.set_degrees_wp_choices(degrees_wp_choices)

    def register_tod(self, tod):
        from collector.utils.allocator import Allocator
        a = Allocator()
        a.restore(tod.tour_of_duty_ref.stored_allocator)
        print(f"{tod.tour_of_duty_ref.reference} fulfillness: {"YES" if a.fulfilled else "NO"}")

