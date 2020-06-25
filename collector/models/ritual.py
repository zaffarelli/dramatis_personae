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

from collector.models.skill import SkillRef
from collector.utils import fs_fics7
from collector.utils.basic import write_pdf

import logging
logger = logging.getLogger(__name__)

RANGE = (
    ("0","Touch"),
    ("1","Sight"),
    ("2","Sensory"),
    ("3","Distance"),
)

DURATION = (
    ("0","Instant"),
    ("1","Temporary"),
    ("2","Prolonged"),
    ("2","Perpetual"),
)

OCCULT_ARTS = (
    ("0","Psi"),
    ("1","Theurgy"),
    ("2","Symbiosis"),
    ("3","Runecasting"),
)


class RitualRef(models.Model):
    class Meta:
        ordering = ['category','path','level','reference']
        verbose_name = "References: Ritual"
    reference = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=32,choices=OCCULT_ARTS)
    level = models.IntegerField(default=1)
    attribute = models.CharField(max_length=6,default='PA_TEM')
    skill = models.ForeignKey(SkillRef, on_delete=models.SET_NULL, null=True, blank=True)
    range = models.CharField(max_length=32,choices=RANGE,default='tou',blank=True)
    duration = models.CharField(max_length=32,choices=DURATION,default='ins',blank=True)
    path = models.CharField(default="", max_length=64, blank=True, null=True)
    wyrd_cost = models.IntegerField(default=1)
    description = models.TextField(null=True,blank=True,max_length=2048)
    modus_operandi = models.TextField(null=True,blank=True,max_length=2048)
    drawbacks = models.TextField(null=True,blank=True,max_length=2048)
    liturgy = models.BooleanField(default=False)
    gesture = models.BooleanField(default=False)
    prayer = models.BooleanField(default=False)
    def __str__(self):
        return "%s [%d](%s)"%(self.reference,self.level, self.path)

class RitualCusto(models.Model):
    from collector.models.character_custo import CharacterCusto
    character_custo = models.ForeignKey(CharacterCusto,on_delete=models.CASCADE)
    ritual_ref = models.ForeignKey(RitualRef,on_delete=models.CASCADE)

class Ritual(models.Model):
    from collector.models.character import Character
    character = models.ForeignKey(Character,on_delete=models.CASCADE)
    ritual_ref = models.ForeignKey(RitualRef,on_delete=models.CASCADE)

class RitualInline(admin.TabularInline):
    model = Ritual

class RitualCustoInline(admin.TabularInline):
    model = RitualCusto

class RitualRefAdmin(admin.ModelAdmin):
    ordering = ['category','path','level','reference']
    list_display = ('reference', 'level', 'category', 'path', 'attribute', 'skill', 'range', 'duration','wyrd_cost')
    list_filter = ('category','path','level',)
    search_fields = ('reference','description','modus_operandi','drawbacks')
