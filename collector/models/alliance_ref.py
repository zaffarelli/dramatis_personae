"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from colorfield.fields import ColorField
from django.db import models
from django.contrib import admin
from collector.mixins.ridded_mixin import RiddedMixin
from collector.utils.helper import refix

ALLIANCE_CATEGORIES = (
    ('nobility', "Royale Nobility"),
    ('minor_nobility', "Nobility"),
    ('church', "Church"),
    ('minor_sects', "Minor Sects of the Church"),
    ('guild', "Guild"),
    ('minor_guild', "Minor Guilds"),
    ('outlaw', "Terrorist Groups"),
    ('foes', "Enemies of the Crown"),
    ('other', "Other"),
)

class AllianceRef(RiddedMixin):
    class Meta:
        verbose_name = "FICS: Alliance"
        ordering = ['reference', 'category', ]

    reference = models.CharField(max_length=128, default='')
    category = models.CharField(max_length=20, choices=ALLIANCE_CATEGORIES, default='other')
    color_front = ColorField(default='#AAAAAA',format="hexa")
    color_back = ColorField(default='#666666',format="hexa")
    color_highlight = ColorField(default='#111111',format="hexa")
    faction = models.CharField(max_length=128, default='', blank=True)
    icon_simple = models.CharField(max_length=3, default='', blank=True)
    icon_complex = models.CharField(max_length=258, default='', blank=True)
    color_icon_stroke = ColorField(default='#888888',format="hexa")
    color_icon_fill = ColorField(default='#333333',format="hexa")
    common_occult_pathes = models.CharField(max_length=256, default='', blank=True)
    internal_index = models.IntegerField(default=0,blank=True)


    def __str__(self):
        return f'{self.reference} ({self.get_category_display()})'

    def fix(self):
        self.toRID(f"{self.reference}")


class AllianceRefAdmin(admin.ModelAdmin):
    ordering = ['category', 'reference']
    list_display = ['reference','r_i_d','internal_index', 'faction', 'category', 'common_occult_pathes', 'color_front', 'color_back',
                    'color_highlight']
    list_filter = ['category']
    list_editable = ['internal_index']
    search_fields = ['category']
    actions = [refix]
