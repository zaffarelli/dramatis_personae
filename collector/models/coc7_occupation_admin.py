"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
from collector.models.coc7_skill import Coc7SkillModificatorInline


def refix(modeladmin, request, queryset):
    for item in queryset:
        item.save()
    short_description = "Refix by forced save'()"


class Coc7OccupationAdmin(admin.ModelAdmin):
    list_display = ['reference', 'smart_code', 'is_classic', 'is_lovecraftian', 'credit_min', 'credit_max',
                    'occupation_points']
    list_filter = ['is_classic', 'is_lovecraftian', 'occupation_points', ]
    actions = [refix]
    inlines = [Coc7SkillModificatorInline]