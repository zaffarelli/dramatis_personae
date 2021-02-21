"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
from collector.models.character import Character
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from collector.utils import fics_references
from collector.models.character_custo import CharacterCusto
from collector.models.tourofduty import TourOfDutyRef
from collector.mixins.uuid_class import UUIDClass


class SkillRef(UUIDClass):
    class Meta:
        ordering = ['is_speciality', 'is_wildcard', 'reference']
        verbose_name = "FICS: Skill"

    reference = models.CharField(max_length=200, unique=True)
    is_root = models.BooleanField(default=False)
    is_speciality = models.BooleanField(default=False)
    is_common = models.BooleanField(default=True)
    is_wildcard = models.BooleanField(default=False)
    group = models.CharField(default="EDU", max_length=3, choices=fics_references.GROUPCHOICES)
    linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s %s [%s]' % (
        self.reference, self.group, "(R)" if self.is_root else "", "(S)" if self.is_speciality else "",
        self.linked_to.reference if self.linked_to else "-")

    def fix(self):
        super().fix()


class Skill(models.Model):
    class Meta:
        ordering = ['skill_ref', ]
        verbose_name = "Skill"

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.skill_ref.reference)

    def fix(self):
        pass




# Inlines
class SkillInline(admin.TabularInline):
    model = Skill
    extras = 10
    ordering = ('skill_ref',)


class SkillModificator(models.Model):
    class Meta:
        ordering = ['skill_ref']

    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.tour_of_duty_ref.reference, self.skill_ref.reference)

    def fix(self):
        pass





class SkillCusto(models.Model):
    class Meta:
        ordering = ['character_custo', 'skill_ref']

    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(SkillRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)


# Inlines

class SkillModificatorInline(admin.TabularInline):
    model = SkillModificator
    extras = 3
    ordering = ('skill_ref', 'tour_of_duty_ref')


class SkillCustoInline(admin.TabularInline):
    model = SkillCusto
    extras = 3
    ordering = ('skill_ref', 'character_custo')


# Admins

def change_to_awa(modeladmin, request, queryset):
    queryset.update(group='AWA')
    short_description = "Change skills to the AWA group"


def change_to_bod(modeladmin, request, queryset):
    queryset.update(group='BOD')
    short_description = "Change skills to the BOD group"


def change_to_edu(modeladmin, request, queryset):
    queryset.update(group='EDU')
    short_description = "Change skills to the EDU group"


def change_to_per(modeladmin, request, queryset):
    queryset.update(group='PER')
    short_description = "Change skills to the PER group"


def change_to_fig(modeladmin, request, queryset):
    queryset.update(group='FIG')
    short_description = "Change skills to the FIG group"


def change_to_con(modeladmin, request, queryset):
    queryset.update(group='CON')
    short_description = "Change skills to the CON group"


def change_to_soc(modeladmin, request, queryset):
    queryset.update(group='SOC')
    short_description = "Change skills to the SOC group"


def change_to_tin(modeladmin, request, queryset):
    queryset.update(group='TIN')
    short_description = "Change skills to the TIN group"


def change_to_spi(modeladmin, request, queryset):
    queryset.update(group='SPI')
    short_description = "Change skills to the SPI group"


def change_to_und(modeladmin, request, queryset):
    queryset.update(group='UND')
    short_description = "Change skills to the UND group"


def change_to_dip(modeladmin, request, queryset):
    queryset.update(group='DIP')
    short_description = "Change skills to the DIP group"


def set_common(modeladmin, request, queryset):
    queryset.update(is_common=True)
    short_description = "Change skills to common"


def set_uncommon(modeladmin, request, queryset):
    queryset.update(is_common=False)
    short_description = "Change skills to uncommon"

def refix(modeladmin, request, queryset):
    for skill_ref in queryset:
        skill_ref.save()
    short_description = "Do fix"


class SkillRefAdmin(admin.ModelAdmin):
    ordering = ['is_speciality', 'is_wildcard', 'reference']
    list_display = ['reference','uuid', 'is_root', 'is_speciality', 'is_wildcard', 'is_common', 'group', 'linked_to']
    actions = [refix,change_to_awa, change_to_soc, change_to_edu, change_to_fig, change_to_con, change_to_tin, change_to_per,
               change_to_bod, set_common, set_uncommon]
    list_filter = ['is_root', 'is_speciality', 'is_wildcard', 'is_common', 'linked_to']
    search_fields = ('reference',)
