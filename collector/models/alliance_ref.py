'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from colorfield.fields import ColorField
from django.db import models
from django.contrib import admin


ALLIANCE_CATEGORIES = (
    ('nobility',"Nobility"),
    ('church',"Church"),
    ('guild',"Guild"),
    ('other',"Other"),
)

class AllianceRef(models.Model):
    class Meta:
        verbose_name = "FICS: Alliance"
        ordering = ['reference', 'category', ]
    reference = models.CharField(max_length=128,default='')
    category = models.CharField(max_length=10,choices=ALLIANCE_CATEGORIES,default='other')
    color_front = ColorField(default='#AAAAAA')
    color_back = ColorField(default='#666666')

    def _str_(self):
        return f'{self.reference} ({self.get_category_display})'

class AllianceRefAdmin(admin.ModelAdmin):
    ordering = ['category', 'reference']
    list_display = ['reference', 'category', 'color_front', 'color_back']
    list_filter = ['category']
    search_fields = ['category']
