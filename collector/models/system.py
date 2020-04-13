'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from datetime import datetime
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
import hashlib
from scenarist.models.epics import Epic
from collector.models.fics_models import Specie
from collector.models.combattant import Combattant
from collector.utils import fs_fics7
from collector.utils.basic import write_pdf

import logging
logger = logging.getLogger(__name__)

class System(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=200, unique=True)
    alliance = models.CharField(max_length=200)
    sector = models.CharField(max_length=200, default="Empire")
    jumproads = models.ManyToManyField('self', blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    jump = models.IntegerField(default=0)
    group = models.IntegerField(default=0)
    color = models.CharField(max_length=16,default="#CCC")
    dtj = models.FloatField(default=69)
    garrison = models.IntegerField(default=1)
    tech = models.IntegerField(default=3)
    population = models.IntegerField(default=0)
    #discovered = models.BooleanField(default=False)
    discovery = models.IntegerField(default=6000)
    symbol = models.CharField(max_length=1,default="9")

    def __str__(self):
        return "%s"%(self.name)

    @property
    def routes(self):
        return self.jumproads.all().count()

class SystemAdmin(admin.ModelAdmin):
  ordering = ['discovery','name','alliance']
  list_display = ('name', 'alliance', 'discovery', 'sector', 'routes', 'group', 'color', 'x', 'y')
