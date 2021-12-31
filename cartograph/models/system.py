"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
# from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from colorfield.fields import ColorField
from collector.models.alliance_ref import AllianceRef
# from django.urls import reverse
# import hashlib
# from scenarist.models.epics import Epic
# from cartograph.models.fics_models import Specie
# from cartograph.models.combattant import Combattant
# from cartograph.utils import fs_fics7
# from cartograph.utils.basic import write_pdf

import logging

logger = logging.getLogger(__name__)

ORBITAL_ITEMS = (
    ('0', 'Sun'),
    ('1', 'Gas Giant'),
    ('2', 'Telluric'),
    ('3', 'Asteroids Belt'),
    ('4', 'Space Station'),
    ('5', 'Jumpgate'),
    ('6', 'Allied Forces'),
    ('7', 'Hostiles'),
)


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
        return "%s (%s)" % (self.name, self.system.name)

    @property
    def nameid(self):
        return f'Item > {self.name}'

    def fix(self):
        logger.info(f'Object {self.name} saved.')

    def prepare(self):
        from django.core.exceptions import ObjectDoesNotExist
        """ After saving, update relevant System DTJ """
        try:
            relevant_system = System.objects.get(name=self.system)
            main_world = OrbitalItem.objects.get(name=self.system)
            jumpgate = OrbitalItem.objects.filter(system=self.system, category="5").first()
            if self.azimut == 0:
                import random
                self.azimut = random.randint(0, 999) / 1000
            if jumpgate and main_world:
                relevant_system.dtj = jumpgate.distance - main_world.distance
                relevant_system.save()
        except ObjectDoesNotExist:
            logger.info("[%s] Unable to fix system due to missing system and/or orbital items." % (self.system))


@receiver(pre_save, sender=OrbitalItem, dispatch_uid='prepare_orbital_data')
def prepare_orbital_data(sender, instance, **kwargs):
    instance.prepare()


@receiver(post_save, sender=OrbitalItem, dispatch_uid='propagate_orbital_data')
def propagate_orbital_data(sender, instance, **kwargs):
    instance.fix()


class OrbitalItemInline(admin.TabularInline):
    model = OrbitalItem
    ordering = ('distance',)


class SystemAdmin(admin.ModelAdmin):
    ordering = ['name', 'alliance']
    list_display = ['name', 'alliance', 'allianceref', 'discovery', 'sector', 'orbital_map', 'dtj', 'routes', 'routes_list', 'group',
                    'color', 'x', 'y']
    inlines = [OrbitalItemInline]
    list_filter = ['group', 'alliance','allianceref', 'sector']
    search_fields = ['name', 'alliance', 'sector']


class OrbitalItemAdmin(admin.ModelAdmin):
    ordering = ['system', 'distance', 'name']
    list_display = ['nameid', 'name', 'category', 'color', 'azimut', 'distance', 'tilt', 'size', 'qualifier', 'rings']
    list_filter = ['category', 'system', 'distance', 'tilt']
    search_fields = ['name', 'qualifier', 'system']
