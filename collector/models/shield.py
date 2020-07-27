'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character


class ShieldRef(models.Model):
    class Meta:
        ordering = ['cost', 'reference']
        verbose_name = "References: Shield"

    reference = models.CharField(max_length=16, default='', blank=True, unique=True)
    protection_min = models.PositiveIntegerField(default=10, blank=True)
    protection_max = models.PositiveIntegerField(default=20, blank=True)
    hits = models.PositiveIntegerField(default=10, blank=True)
    cost = models.PositiveIntegerField(default=500, blank=True)
    is_compatible_with_medium_armor = models.BooleanField(default=False)
    is_compatible_with_hard_armor = models.BooleanField(default=False)
    description = models.TextField(max_length=128, default='', blank=True)

    def __str__(self):
        return '%s' % (self.reference)


class Shield(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    shield_ref = models.ForeignKey(ShieldRef, on_delete=models.CASCADE)
    charges = models.PositiveIntegerField(default=10, blank=True)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.shield_ref.reference)


class ShieldRefAdmin(admin.ModelAdmin):
    ordering = ('reference',)


class ShieldCusto(models.Model):
    class Meta:
        ordering = ['character_custo', 'shield_ref']

    from collector.models.character_custo import CharacterCusto
    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    shield_ref = models.ForeignKey(ShieldRef, on_delete=models.CASCADE)


class ShieldCustoInline(admin.TabularInline):
    model = ShieldCusto


class ShieldInline(admin.TabularInline):
    model = Shield
