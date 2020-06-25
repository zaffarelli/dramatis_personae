'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from collector.models.character import Character

BLOKE_LEVELS=(
    (-2,"Minimal"),     # Work colleagues
    (-1,"Light"),       # Usual coworker
    (0,"Mild"),         # Typical friend
    (1,"Strong"),       # Good friend
    (2,"Maximal"),      # Family / Lover
)

class Bloke(models.Model):
    class Meta:
        ordering = ('player','level','reference')
    player = models.ForeignKey(Character,on_delete=models.CASCADE, related_name='pc')
    reference = models.ForeignKey(Character,on_delete=models.CASCADE, null=True, blank=True, related_name='npc')
    level = models.IntegerField(choices=BLOKE_LEVELS,default=0)

    def __str__(self):
        return "%d > %s"%(self.level, self.reference.rid)

class BlokeInline(admin.TabularInline):
    model = Bloke
    fk_name = 'player'
