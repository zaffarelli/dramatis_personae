"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.models.avatar import Avatar
from django.contrib import admin
from collector.utils.rpg import *


class Denizen(Avatar):
    class Meta:
        abstract = True
    nature = models.CharField(default='', max_length=64, blank=True)
    demeanor = models.CharField(default='', max_length=64, blank=True)
    concept = models.CharField(default='', max_length=64, blank=True)
    W_STR = models.IntegerField(default=0)
    W_DEX = models.IntegerField(default=0)
    W_STA = models.IntegerField(default=0)
    W_CHA = models.IntegerField(default=0)
    W_MAN = models.IntegerField(default=0)
    W_APP = models.IntegerField(default=0)
    W_PER = models.IntegerField(default=0)
    W_INT = models.IntegerField(default=0)
    W_WIT = models.IntegerField(default=0)
    W_WILLPOWER = models.IntegerField(default=0)


class Mortal(Denizen):
    class Meta:
        verbose_name = "WaWWoD: Mortal"


class Kindred(Mortal):
    class Meta:
        verbose_name = "WaWWoD: Kindred"

    clan = models.CharField(default='', max_length=64, blank=True)
    generation = models.PositiveIntegerField(default=13)


class Ghoul(Mortal):
    class Meta:
        verbose_name = "WaWWoD: Ghoul"







