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

import logging

logger = logging.getLogger(__name__)


class RpgSystem(models.Model):
    class Meta:
        ordering = ['name', 'game_mechanics']
        verbose_name = "References: RPG system"

    name = models.CharField(max_length=48, default='', blank=True, unique=True)
    game_mechanics = models.CharField(max_length=64, default='', blank=True)
    smart_code = models.CharField(max_length=16, default='', blank=True)
    description = models.TextField(max_length=1024, default='', blank=True)

    def __str__(self):
        return self.smart_code


class RpgSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'game_mechanics', 'smart_code', 'description']
