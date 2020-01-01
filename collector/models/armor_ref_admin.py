'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from django.contrib import admin

class ArmorRefAdmin(admin.ModelAdmin):
  ordering = ('category','-cost','reference','-stopping_power')
  list_display = ['reference','category','stopping_power','tech_level','encumbrance','head','torso','right_arm','left_arm','right_leg','left_leg','cost','description']
