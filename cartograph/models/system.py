# Cartograph Classes
from django.db import models
from django.contrib import admin
from colorfield.fields import ColorField
from collector.models.alliance_ref import AllianceRef
from cartograph.utils.fics_references import ORBITAL_ITEMS
from collector.utils.helper import refix
from collector.mixins.ridded_mixin import RiddedMixin
import logging
import random

logger = logging.getLogger(__name__)


class System(RiddedMixin):
    class Meta:
        ordering = ['name']
        verbose_name = 'Cartograph: System'

    name = models.CharField(max_length=200, blank=True)
    alliance = models.CharField(max_length=200, default="",  blank=True)
    alliance_rid = models.CharField(max_length=200, default="", blank=True)
    sector = models.CharField(max_length=200, default="Empire", blank=True)
    notes = models.CharField(max_length=200, default="", blank=True)
    jumproads = models.ManyToManyField('self', blank=True)
    x = models.IntegerField(default=0, blank=True)
    y = models.IntegerField(default=0, blank=True)
    jump = models.IntegerField(default=0, blank=True)
    group = models.IntegerField(default=0, blank=True)
    color = ColorField(default="#CCC", blank=True)
    dtj = models.FloatField(default=69, blank=True)
    garrison = models.IntegerField(default=1, blank=True)
    tech = models.IntegerField(default=3, blank=True)
    population = models.IntegerField(default=0, blank=True)
    discovery = models.IntegerField(default=6000, blank=True)
    symbol = models.CharField(max_length=1, default="9", blank=True)
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
        # for o in self.orbitalitem_set.all():
        #     all.append("%s (%.2f AU)" % (o.name, o.distance))
        return ", ".join(all)

    @property
    def allianceref(self):
        return AllianceRef.fromRID(self.alliance_rid)

    def fix(self):
        self.toRID(f"{self.name}")
        # ois = self.orbitalitem_set.all()
        # for o in ois:
        #     if o.azimut == 0:
        #         o.azimut = random.randint(0, 999) / 1000
        #         o.save()
        # main_world = ois.filter(name=self.name).first()
        # jumpgate = ois.filter(category="5").first()
        # if jumpgate and main_world:
        #     self.dtj = jumpgate.distance - main_world.distance
        # else:
        #     print(f"No computable DTF with {jumpgate} {main_world}")


class OrbitalItem(RiddedMixin):
    class Meta:
        ordering = ['system_rid', 'distance']
        verbose_name = 'Cartograph: Orbital Item'

    name = models.CharField(max_length=200, default="", blank=True)
    system_rid = models.CharField(max_length=128,default="", blank=True)
    category = models.CharField(max_length=20, choices=ORBITAL_ITEMS, default="Telluric")
    color = ColorField(default="#FFF", blank=True)
    azimut = models.FloatField(default=0, blank=True)
    distance = models.FloatField(default=0.0, blank=True)
    tilt = models.FloatField(default=0.0, blank=True)
    size = models.PositiveIntegerField(default=10, blank=True)
    qualifier = models.CharField(max_length=64, default='', blank=True, null=True)
    moon = models.TextField(max_length=1024, blank=True, null=True, default='')
    description = models.TextField(max_length=1024, blank=True, null=True, default='')
    rings = models.TextField(max_length=1024, blank=True, null=True, default='')

    def __str__(self):
        return self.nameid

    @property
    def nameid(self):
        return f'[{self.system_rid}] {self.name}'

    def fix(self):
        s = System.fromRID(self.system_rid)
        if s:
            sys = s.name+" "
        else:
          sys = "na "
        self.toRID(f"{sys}{self.name}")
        logger.info(f'Object {self.name} saved.')


# class OrbitalItemInline(admin.TabularInline):
#     model = OrbitalItem
#     ordering = ('distance',)




class SystemAdmin(admin.ModelAdmin):
    ordering = ['name', 'alliance']
    list_display = ['name','rid' ,'alliance', 'discovery', 'sector', 'dtj', 'notes',
                    'group', 'color', 'x', 'y']
    #inlines = [OrbitalItemInline]
    list_filter = ['group', 'alliance', 'sector']
    search_fields = ['name', 'alliance', 'sector']
    list_editable = ["x","y", "discovery","notes"]
    actions = [refix]


class OrbitalItemAdmin(admin.ModelAdmin):
    ordering = ['system_rid', 'distance', 'name']
    list_display = ['name', 'rid', 'color', 'azimut', 'distance', 'tilt', 'size', 'qualifier',
                    'rings', 'moon', 'description']
    list_filter = ['category', 'system_rid', 'distance', 'tilt']
    search_fields = ['name', 'qualifier', 'system']
    actions = [refix]