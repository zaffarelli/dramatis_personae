from django.db import models
from django.contrib import admin
from collector.models.character import Character
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from collector.utils import fics_references
from collector.utils.helper import refix
from collector.models.character_custo import CharacterCusto
from collector.models.tourofduty import TourOfDutyRef
from collector.mixins.ridded_mixin import RiddedMixin, RidField


class SkillRef(RiddedMixin):
    class Meta:
        ordering = ['group', 'reference']
        verbose_name = "FICS: Skill"

    reference = models.CharField(default="", max_length=200, blank=True)
    is_common = models.BooleanField(default=True, blank=True)
    is_wildcard = models.BooleanField(default=False, blank=True)
    group_wildcard = models.BooleanField(default=False, blank=True)
    group = models.CharField(default="EDU", max_length=3, choices=fics_references.GROUPCHOICES, blank=True)
    linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=1024, default='', blank=True)
    acro = models.CharField(default="", max_length=7, blank=True)

    as_wildcard_of = models.CharField(default="", max_length=512, blank=True)

    @property
    def common_specialities(self):
        list = []
        specialities = SkillRef.objects.all()
        for s in specialities:
            name = s.reference
            if s.description:
                str = f'<em>{name}</em>: {s.description}'
            else:
                str = f'<em>{name}</em>'
            list.append(f'<li>{str}</li>')
        res = "\n".join(list)
        return res

    def __str__(self):
        return f"{self.reference} [{self.group}]"

    def fix(self):
        if self.is_wildcard:
            #self.refval = self.reference
            if self.group_wildcard:
                candidates = SkillRef.objects.filter(is_wildcard=False).filter(group=self.group)
                items = []
                for candidate in candidates:
                    items.append(candidate.reference)
                self.as_wildcard_of = ", ".join(items)
            else:
                self.as_wildcard_of = "*"
            print(self.as_wildcard_of)
        else:
            self.as_wildcard_of = ""
        self.toRID(self.reference, True, "sk")
        if self.is_wildcard:
            self.acro = ("WC_" + self.reference[:3]).upper()
        else:
            self.acro = ("SK_" + self.reference[:3]).upper()

class Skill(RiddedMixin):
    class Meta:
        ordering = ['skill_ref', ]
        verbose_name = "Skill"
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
    skill_ref_rid = RidField()
    character_rid = RidField()
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.character.full_name}={self.skill_ref.reference}"

    def fix(self):
        # character_rid = ""
        # skill_ref_rid = ""
        # ch = Character.fromRID(self.character_rid)
        # sr = SkillRef.fromRID(self.skill_ref_rid)
        # if (ch and sr):
        #     character_rid = ch.rid
        #     skill_ref_rid = sr.rid
        #self.toRID(f"{self.skill_ref.reference}_{character_rid}_{skill_ref_rid}")



        self.toRID(f"{self.character.full_name}={self.skill_ref.reference}")


class SkillInline(admin.TabularInline):
    model = Skill
    extras = 10
    ordering = ('skill_ref',)


class SkillModificator(models.Model):
    # SkillModificator is something that comes from an "history" template
    class Meta:
        ordering = ['skill_ref']

    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.tour_of_duty_ref.reference, self.skill_ref.reference)

    def fix(self):
        if self.tour_of_duty_ref:
            if self.tour_of_duty_ref.category in ["10","20"]:
                if self.value > 1:
                    self.value = 1


class SkillCusto(models.Model):
    class Meta:
        ordering = ['character_custo']

    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)
    fromTOD = models.BooleanField(default=False, blank=True)

# Inlines

class SkillModificatorInline(admin.TabularInline):
    model = SkillModificator
    extras = 3
    ordering = ('skill_ref', 'tour_of_duty_ref')


class SkillCustoInline(admin.TabularInline):
    model = SkillCusto
    extras = 3
    ordering = ('skill_ref', 'character_custo')


class SkillRefAdmin(admin.ModelAdmin):
    ordering = ['-is_wildcard','reference']
    list_display = ['reference', 'acro', 'is_common', 'group', 'is_wildcard','group_wildcard',"as_wildcard_of",'rid']
    actions = [refix]
    list_filter = ['is_common', 'is_wildcard']
    search_fields = ['reference', 'group']
    list_editable = ['group']
    actions = [refix]
