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


class DegreeRef(RiddedMixin):
    class Meta:
        ordering = ['group','reference']
        verbose_name = "FICS: Degree"

    class Level(models.TextChoices):
        COMMON = "CO", "0 - Common"
        RESTRICTED = "RE", "1 - Restricted"
        ELITE = "EL", "2 - Elite"
        OBSCURE = "OB", "3 - Obscure"
        FORBIDDEN = "FO", "4 - Forbidden"

    reference = models.CharField(default="", max_length=200, blank=True)
    group = models.CharField(default="GENE", max_length=4, choices=fics_references.DEGREE_GROUPS, blank=True)
    subgroup = models.CharField(default="", max_length=100, blank=True)
    level = models.CharField(default=Level.COMMON, max_length=2, choices=Level, blank=True)
    is_wildcard = models.BooleanField(default=False, blank=True)
    group_wildcard = models.BooleanField(default=False, blank=True)
    deprecated = models.BooleanField(default=False, blank=True)
    description = models.TextField(max_length=1024, default='', blank=True)
    as_wildcard_of = models.CharField(default="", max_length=512, blank=True)

    def __str__(self):
        return f"{self.get_group_display()}: {self.reference}"

    def fix(self):
        # self.toRID(f"{self.reference}_{self.group}")
        self.toRID(f"{self.level}_{self.is_wildcard}_{self.group}_{self.reference}", False, "DEG_", cypher=True)


class DegreeModificator(models.Model):
    class Meta:
        ordering = ['degree_ref']

    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    degree_ref = models.ForeignKey(DegreeRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.tour_of_duty_ref.reference, self.degree_ref.reference)

    def fix(self):
        pass


class DegreeCusto(models.Model):
    class Meta:
        ordering = ['character_custo']

    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    degree_ref = models.ForeignKey(DegreeRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

class Degree(RiddedMixin):
    class Meta:
        ordering = ['degree_ref', ]
        verbose_name = "Degree"

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    degree_ref = models.ForeignKey(DegreeRef, on_delete=models.CASCADE)
    skill_ref_rid = RidField()
    character_rid = RidField()
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.degree_ref.reference)

    def fix(self):
        ch = Character.rid
        dr = DegreeRef.rid
        if (ch and dr):
            self.toRID(f"{ch}_{dr}")


class DegreeModificatorInline(admin.TabularInline):
    model = DegreeModificator
    extras = 1
    ordering = ('degree_ref', 'tour_of_duty_ref')


class DegreeCustoInline(admin.TabularInline):
    model = DegreeCusto
    extras = 3
    ordering = ('degree_ref', 'character_custo')


class DegreeRefAdmin(admin.ModelAdmin):
    ordering = ['-is_wildcard', 'level', 'group', 'reference']
    list_display = ['reference', 'level', 'is_wildcard','group_wildcard', 'group','subgroup', 'deprecated', 'description', 'rid']
    list_filter = ['group','subgroup','is_wildcard', 'level']
    list_editable = ['subgroup', 'deprecated', 'level']
    search_fields = ['reference']
    actions = [refix]
