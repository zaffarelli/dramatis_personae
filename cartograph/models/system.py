"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
from colorfield.fields import ColorField
from collector.models.alliance_ref import AllianceRef
from cartograph.utils.fics_references import ORBITAL_ITEMS
import logging
import random

logger = logging.getLogger(__name__)


class System(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Cartograph: System'

    name = models.CharField(max_length=200, unique=True)
    alliance = models.CharField(max_length=200)
    allianceref = models.ForeignKey(AllianceRef, on_delete=models.SET_NULL, blank=True, null=True)
    sector = models.CharField(max_length=200, default="Empire")
    jumproads = models.ManyToManyField('self', blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    jump = models.IntegerField(default=0)
    group = models.IntegerField(default=0)
    color = ColorField(default="#CCC")
    dtj = models.FloatField(default=69)
    garrison = models.IntegerField(default=1)
    tech = models.IntegerField(default=3)
    population = models.IntegerField(default=0)
    discovery = models.IntegerField(default=6000)
    symbol = models.CharField(max_length=1, default="9")
    zoom_val = models.IntegerField(null=True, blank=True, default=0)
    zoom_factor = models.IntegerField(null=True, blank=True, default=0)
    description = models.TextField(max_length=1024, blank=True, null=True, default='')

    def __str__(self):
        return "%s" % (self.name)

    @property
    def routes(self):
        return self.jumproads.all().count()

    @property
    def routes_list(self):
        all = []
        for r in self.jumproads.all():
            all.append(f'{self.name}_{r.name} ')
        return ", ".join(all)

    @property
    def orbital_map(self):
        all = []
        for o in self.orbitalitem_set.all():
            all.append("%s (%.2f AU)" % (o.name, o.distance))
        return ", ".join(all)

    def fix(self):
        ois = self.orbitalitem_set.all()
        for o in ois:
            if o.azimut == 0:
                o.azimut = random.randint(0, 999) / 1000
                o.save()
        main_world = ois.filter(name=self.name)
        jumpgate = ois.filter(category="5").first()
        if jumpgate and main_world:
            self.dtj = jumpgate.distance - main_world.distance


class OrbitalItem(models.Model):
    class Meta:
        ordering = ['system', 'distance']
        verbose_name = 'Cartograph: Orbital Item'

    name = models.CharField(max_length=200, default="", blank=True)
    system = models.ForeignKey(System, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=20, choices=ORBITAL_ITEMS, default="Telluric")
    color = ColorField(default="#FFF")
    # speed = models.FloatField(default=1.0)
    azimut = models.FloatField(default=0)
    distance = models.FloatField(default=0.0)
    tilt = models.FloatField(default=0.0)
    size = models.PositiveIntegerField(default=10)
    qualifier = models.CharField(max_length=64, default='', blank=True, null=True)
    moon = models.TextField(max_length=1024, blank=True, null=True, default='')
    description = models.TextField(max_length=1024, blank=True, null=True, default='')
    rings = models.TextField(max_length=1024, blank=True, null=True, default='')

    def __str__(self):
        return self.nameid

    @property
    def nameid(self):
        return f'[{self.system}] {self.name} ({self.get_category_display()})'

    def fix(self):
        logger.info(f'Object {self.name} saved.')


class OrbitalItemInline(admin.TabularInline):
    model = OrbitalItem
    ordering = ('distance',)


class SystemAdmin(admin.ModelAdmin):
    ordering = ['name', 'alliance']
    list_display = ['name', 'alliance', 'allianceref', 'discovery', 'sector', 'orbital_map', 'dtj', 'routes',
                    'routes_list', 'group',
                    'color', 'x', 'y']
    inlines = [OrbitalItemInline]
    list_filter = ['group', 'alliance', 'allianceref', 'sector']
    search_fields = ['name', 'alliance', 'sector']


class OrbitalItemAdmin(admin.ModelAdmin):
    ordering = ['system', 'distance', 'name']
    list_display = ['nameid', 'color', 'azimut', 'distance', 'tilt', 'size', 'qualifier',
                    'rings', 'moon', 'description']
    list_filter = ['category', 'system', 'distance', 'tilt']
    search_fields = ['name', 'qualifier', 'system']
