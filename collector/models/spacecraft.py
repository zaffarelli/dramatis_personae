'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
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
from django.contrib import admin

import logging
logger = logging.getLogger(__name__)

class Spacecraft(models.Model):
    full_name = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    ship_class = models.CharField(max_length=200)
    ship_grade = models.CharField(max_length=200)
    engines_type = models.CharField(max_length=200)
    shields_type = models.CharField(max_length=200)
    size_rating = models.PositiveIntegerField(default=1)
    dim_length = models.PositiveIntegerField(default=1)
    dim_width = models.PositiveIntegerField(default=1)
    dim_height = models.PositiveIntegerField(default=1)

class SpacecraftAdmin(admin.ModelAdmin):
  ordering = ['full_name','model','size_rating']
  list_display = ('full_name','model','size_rating')
