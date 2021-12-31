"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
from collector.models.skill import SkillRef
from collector.utils import fics_references
import logging
logger = logging.getLogger(__name__)


class RitualRef(models.Model):
    class Meta:
        ordering = ['category', 'path', 'level', 'reference']
        verbose_name = "FICS: Ritual"

    reference = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=32, choices=fics_references.OCCULT_ARTS)
    level = models.IntegerField(default=1)
    attribute = models.CharField(max_length=6, default='PA_TEM')
    skill = models.ForeignKey(SkillRef, on_delete=models.SET_NULL, null=True, blank=True)
    range = models.CharField(max_length=32, choices=fics_references.RANGE, default='tou')
    duration = models.CharField(max_length=32, choices=fics_references.DURATION, default='ins')
    path = models.CharField(default="", max_length=64)
    wyrd_cost = models.IntegerField(default=1)
    description = models.TextField(null=True, max_length=2048, blank=True)
    modus_operandi = models.TextField(default='', max_length=2048, blank=True)
    drawbacks = models.TextField(default='', max_length=2048, blank=True)
    liturgy = models.BooleanField(default=False)
    gesture = models.BooleanField(default=False)
    prayer = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.reference} ({self.path}, {self.level})'

    def to_json(self):
        from collector.utils.basic import json_default
        import json
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr

class RitualCusto(models.Model):
    from collector.models.character_custo import CharacterCusto
    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    ritual_ref = models.ForeignKey(RitualRef, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ritual_ref.reference} ({self.ritual_ref.path} {self.ritual_ref.level})'


class Ritual(models.Model):
    from collector.models.character import Character
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    ritual_ref = models.ForeignKey(RitualRef, on_delete=models.CASCADE)
    attribute_value = models.PositiveIntegerField(default=0)
    skill_value = models.IntegerField(default=0)
    value = models.IntegerField(default=0)

    def fix(self):
        self.attribute_value = getattr(self.character,self.ritual_ref.attribute)
        found_skills = self.character.skill_set.filter(skill_ref=self.ritual_ref.skill)
        if not len(found_skills):
            self.skill_value = -2
        else:
            self.skill_value = found_skills.first().value

        self.value = self.attribute_value + self.skill_value


    def __str__(self):
        return f'{self.character.rid} > {self.ritual_ref.reference} ({self.ritual_ref.path} {self.ritual_ref.level})'


class RitualInline(admin.TabularInline):
    model = Ritual


class RitualCustoInline(admin.TabularInline):
    model = RitualCusto


class RitualRefAdmin(admin.ModelAdmin):
    ordering = ['category', 'path', 'level', 'reference']
    list_display = ('reference', 'level', 'category', 'path', 'attribute', 'skill', 'range', 'duration', 'wyrd_cost')
    list_filter = ('category', 'path', 'level',)
    search_fields = ('reference', 'description', 'modus_operandi', 'drawbacks')
