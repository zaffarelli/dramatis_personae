'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character

BLOKE_LEVELS = (
    (-2, "Minimal"),  # Work colleagues
    (-1, "Light"),  # Usual coworker
    (0, "Mild"),  # Typical friend
    (1, "Strong"),  # Good friend
    (2, "Maximal"),  # Family / Lover
)


class Bloke(models.Model):
    class Meta:
        ordering = ['character', 'level', 'npc']

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character', blank=True, null=True)
    npc = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True, related_name='npc')
    level = models.IntegerField(choices=BLOKE_LEVELS, default=0)
    description = models.TextField(default='', max_length=1024, blank=True, null=True)

    def __str__(self):
        return f'{self.character.rid} > ({self.level}) > {self.npc.rid}'


class BlokeInline(admin.TabularInline):
    model = Bloke
    fk_name = 'character'


class BlokeAdmin(admin.ModelAdmin):
    list_display = ['character', 'level', 'npc', 'description']
    ordering = ['character', '-level', 'npc']
    search_fields = ['character', 'npc']
    list_filter = ['character', 'npc', 'level']

