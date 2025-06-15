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
        ordering = ['-is_wildcard', 'group', 'reference']
        verbose_name = "FICS: Degree"

    class Level(models.TextChoices):
        COMMON = "CO", "(1)"
        RESTRICTED = "RE", "(2)"
        ELITE = "EL", "(3)"
        OBSCURE = "OB", "(4)"
        FORBIDDEN = "FO", "(5)"

    reference = models.CharField(default="", max_length=200, blank=True)
    group = models.CharField(default="GENE", max_length=4, choices=fics_references.DEGREE_GROUPS, blank=True)
    subgroup = models.CharField(default="", max_length=100, blank=True)
    level = models.CharField(default=Level.COMMON, max_length=2, choices=Level, blank=True)
    is_wildcard = models.BooleanField(default=False, blank=True)
    group_wildcard = models.BooleanField(default=False, blank=True)
    refval = models.CharField(default="", max_length=200, blank=True)
    description = models.TextField(max_length=1024, default='', blank=True)
    as_wildcard_of = models.CharField(default="", max_length=512, blank=True)

    def __str__(self):
        return f"[{self.get_group_display()}] {self.reference}"

    def fix(self):
        # self.toRID(f"{self.reference}_{self.group}")
        self.toRID(f"{self.level}_{self.is_wildcard}_{self.group}_{self.reference}", False, "DEG_", cypher=True)
        if self.is_wildcard:
            self.refval = self.reference
            if self.group_wildcard:
                candidates = DegreeRef.objects.filter(is_wildcard=False).filter(group=self.group)
                items = []
                for candidate in candidates:
                    items.append(candidate.reference)
                self.as_wildcard_of = ", ".join(items)
        else:
            k = 4
            self.refval = ""
            if len(self.reference) > 20:
                words = self.reference.split(" ")
                for word in words:
                    if len(word) < k:
                        self.refval += word
                    else:
                        self.refval += word[:k]
            else:
                words = self.reference.split(" ")
                for word in words:
                    self.refval += word


class DegreeModificator(models.Model):
    """
    A degree-modificator is linked to a ToD and can be a wildcard
    """

    class Meta:
        ordering = ['-degree_ref__is_wildcard', 'degree_ref__group', 'degree_ref__reference']

    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    degree_ref = models.ForeignKey(DegreeRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)

    def __str__(self):
        return '%s %s' % (self.tour_of_duty_ref.reference, self.degree_ref.reference)

    def fix(self):
        pass


class DegreeCusto(models.Model):
    """
    A degree-custo is linked to the customizer, cannot be a wild card and all the d-custo should fullfill the
    d-modificators of the ToDs
    """

    class Meta:
        ordering = ['degree_ref__group', 'degree_ref']

    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    degree_ref = models.ForeignKey(DegreeRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=1)


class Degree(RiddedMixin):
    class Meta:
        ordering = ['degree_ref', ]
        verbose_name = "Degree"

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    degree_ref = models.ForeignKey(DegreeRef, on_delete=models.CASCADE)
    skill_ref_rid = RidField()
    character_rid = RidField()
    value = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.degree_ref.reference)

    def fix(self):
        # ch = Character.rid
        # dr = DegreeRef.rid
        # if (ch and dr):
        #     self.toRID(f"{ch}_{dr}")
        self.toRID(f"{self.character.full_name}={self.degree_ref.reference}")


class DegreeInline(admin.TabularInline):
    model = Degree
    extras = 10
    ordering = ('degree_ref',)




class DegreeModificatorInline(admin.TabularInline):
    model = DegreeModificator
    extras = 1
    ordering = ('-degree_ref__is_wildcard', 'degree_ref__group', 'degree_ref__reference')


class DegreeCustoInline(admin.TabularInline):
    model = DegreeCusto
    extras = 3
    ordering = ('degree_ref', 'character_custo')


class DegreeRefAdmin(admin.ModelAdmin):
    ordering = ['-is_wildcard', 'group', 'reference']
    list_display = ['reference', 'level', 'refval', 'is_wildcard', 'group_wildcard', 'group', 'subgroup', 'as_wildcard_of']
    list_filter = ['group', 'subgroup', 'is_wildcard', 'level']
    list_editable = ['group', 'subgroup', 'level']
    search_fields = ['reference']
    actions = [refix]
