"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.models.character import Character
from django.contrib import admin
import json


class ArmorRef(models.Model):
    class Meta:
        ordering = ['reference']
        verbose_name = "FICS: Armor"

    reference = models.CharField(max_length=64, default='', unique=True)
    category = models.CharField(max_length=6,
                                choices=(('Soft', "Soft Armor"), ('Medium', "Medium Armor"), ('Hard', "Hard Armor")),
                                default='Soft')
    head = models.BooleanField(default=False)
    torso = models.BooleanField(default=True)
    left_arm = models.BooleanField(default=True)
    right_arm = models.BooleanField(default=True)
    left_leg = models.BooleanField(default=False)
    right_leg = models.BooleanField(default=False)
    stopping_power = models.PositiveIntegerField(default=2)
    cost = models.PositiveIntegerField(default=2)
    encumbrance = models.PositiveIntegerField(default=0)
    meta_type = models.CharField(max_length=64, default='', blank=True)
    tech_level = models.PositiveIntegerField(default=3)
    description = models.TextField(max_length=1024, default='', blank=True)

    def __str__(self):
        return '%s (%s, SP:%s)' % (self.reference, self.category, self.stopping_power)

    def toJSON(self):
        from collector.utils.basic import json_default
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class Armor(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.armor_ref.reference)


class ArmorCusto(models.Model):
    class Meta:
        ordering = ['character_custo', 'armor_ref']

    from collector.models.character_custo import CharacterCusto
    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    armor_ref = models.ForeignKey(ArmorRef, on_delete=models.CASCADE)


class ArmorRefAdmin(admin.ModelAdmin):
    ordering = ['-category','-stopping_power', 'encumbrance', 'reference']
    list_display = ['reference', 'category', 'stopping_power', 'encumbrance', 'head', 'torso', 'right_arm', 'left_arm',
                    'right_leg', 'left_leg', 'cost', 'description', 'tech_level']
    list_filter = ['category', 'meta_type']
    search_fields = ['reference','meta_type','category',]


class ArmorInline(admin.TabularInline):
    model = Armor


class ArmorCustoInline(admin.TabularInline):
    model = ArmorCusto
