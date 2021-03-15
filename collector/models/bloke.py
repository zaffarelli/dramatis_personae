'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character

BLOKE_LEVELS = (
    (-2, "Minimal"),  # Work colleagues      XS
    (-1, "Light"),  # Usual coworker         S
    (0,  "Mild"),  # Typical friend          M
    (1,  "Important"),  # Good friend        L
    (2,  "Strong"),  # Family / Lover        XL
    (3,  "Maximal"),  # Family / Lover       XXL
)


class Bloke(models.Model):
    class Meta:
        ordering = ['character', 'level', 'npc']
        verbose_name = "FICS: Bloke"

    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character', blank=True, null=True)
    npc = models.ForeignKey(Character, on_delete=models.CASCADE, null=True, blank=True, related_name='npc')
    level = models.IntegerField(choices=BLOKE_LEVELS, default=0)
    description = models.TextField(default='', max_length=1024, blank=True, null=True)

    def __str__(self):
        try:
            src = self.character.rid
        except:
            src= 'blank'
        return f'{src} > ({self.level}) > {self.npc.rid}'


class BlokeInline(admin.TabularInline):
    model = Bloke
    fk_name = 'character'


class BlokeAdmin(admin.ModelAdmin):
    list_display = ['character', 'level', 'npc', 'description']
    ordering = ['character', '-level', 'npc']
    search_fields = ['character', 'npc']
    list_filter = ['character', 'npc', 'level']

