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
# from django.urls import reverse
# import hashlib
# from scenarist.models.epics import Epic
# from collector.models.fics_models import Specie
# from collector.models.combattant import Combattant
# from collector.utils import fs_fics7
# from collector.utils.basic import write_pdf

import logging

logger = logging.getLogger(__name__)

ORBITAL_ITEMS = (
    ("0", "Sun"),
    ("1", "Gas Giant"),
    ("2", "Telluric"),
    ("3", "Asteroids Belt"),
    ("4", "Space Station"),
    ("5", "Jumpgate"),
)


class System(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = "Jumpweb: System"

    name = models.CharField(max_length=200, unique=True)
    alliance = models.CharField(max_length=200)
    sector = models.CharField(max_length=200, default="Empire")
    jumproads = models.ManyToManyField('self', blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    jump = models.IntegerField(default=0)
    group = models.IntegerField(default=0)
    color = models.CharField(max_length=16, default="#CCC")
    dtj = models.FloatField(default=69)
    garrison = models.IntegerField(default=1)
    tech = models.IntegerField(default=3)
    population = models.IntegerField(default=0)
    # discovered = models.BooleanField(default=False)
    discovery = models.IntegerField(default=6000)
    symbol = models.CharField(max_length=1, default="9")

    def __str__(self):
        return "%s" % (self.name)

    @property
    def routes(self):
        return self.jumproads.all().count()

    @property
    def orbital_map(self):
        all = []
        for o in self.orbitalitem_set.all():
            all.append("%s (%.2f AU)" % (o.name, o.distance))
        return ", ".join(all)


class OrbitalItem(models.Model):
    class Meta:
        ordering = ['system', 'distance']
        verbose_name = "Jumpweb: Orbital Item"

    name = models.CharField(max_length=200)
    system = models.ForeignKey(System, on_delete=models.CASCADE, blank=True)
    category = models.CharField(max_length=20, choices=ORBITAL_ITEMS, default="Telluric")
    distance = models.FloatField(default=0.0)
    tilt = models.FloatField(default=0.0)
    size = models.PositiveIntegerField(default=10)
    qualifier = models.CharField(max_length=64, default='', blank=True, null=True)
    moon = models.TextField(max_length=1024, blank=True, null=True, default='')
    description = models.TextField(max_length=1024, blank=True, null=True, default='')

    def __str__(self):
        return "%s (%s)" % (self.name, self.system.name)

    def fix(self):
        from django.core.exceptions import ObjectDoesNotExist
        """ After saving, update relevant System DTJ """
        try:
            relevant_system = System.objects.get(name=self.system)
            main_world = OrbitalItem.objects.get(name=self.system)
            jumpgate = OrbitalItem.objects.get(system=self.system, category="5")
            relevant_system.dtj = jumpgate.distance - main_world.distance
            relevant_system.save()
        except ObjectDoesNotExist:
            logger.warning("[%s] Unable to fix system due to missing system and/or orbital items." % (self.system))


@receiver(post_save, sender=OrbitalItem, dispatch_uid='propagate_orbital_data')
def propagate_orbital_data(sender, instance, **kwargs):
    instance.fix()


class OrbitalItemInline(admin.TabularInline):
    model = OrbitalItem
    ordering = ('distance',)


class SystemAdmin(admin.ModelAdmin):
    ordering = ['name', 'alliance']
    list_display = (
    'name', 'alliance', 'discovery', 'sector', 'orbital_map', 'dtj', 'routes', 'group', 'color', 'x', 'y')
    inlines = [OrbitalItemInline]
    list_filter = ('alliance', 'sector')


class OrbitalItemAdmin(admin.ModelAdmin):
    ordering = ['system', 'distance', 'name']
    list_display = ('name', 'category', 'system', 'distance', 'tilt', 'size', 'qualifier')
    list_filter = ('system',)
    search_fields = ('name', 'qualifier', 'system')
