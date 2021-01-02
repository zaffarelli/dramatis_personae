"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.models.avatar import Avatar
from django.contrib import admin
from collector.utils.rpg import *


class Investigator(Avatar):
    class Meta:
        verbose_name = "EDGE_7E: Investigator"
    nationality = models.CharField(max_length=64, default="American")

    C_FOR = models.IntegerField(default=0)
    C_CON = models.IntegerField(default=0)
    C_TAI = models.IntegerField(default=0)
    C_DEX = models.IntegerField(default=0)
    C_APP = models.IntegerField(default=0)
    C_INT = models.IntegerField(default=0)
    C_POU = models.IntegerField(default=0)
    C_EDU = models.IntegerField(default=0)

    C_CHANCE = models.IntegerField(default=0)
    C_SANTE_MENTALE = models.IntegerField(default=0)

    C_TOTAL = models.IntegerField(default=0)

    def fix(self, conf=None):
        super().fix(conf)

    def roll_attributes(self):
        super().roll_attributes()
        self.C_FOR = d(3, 6)*5
        self.C_CON = d(3, 6) * 5
        self.C_DEX = d(3, 6) * 5
        self.C_APP = d(3, 6) * 5
        self.C_POU = d(3, 6) * 5

        self.C_CHANCE = d(3, 6) * 5

        self.C_TAI = (d(2, 6)+6) * 5
        self.C_INT = (d(2, 6)+6) * 5
        self.C_EDU = (d(2, 6)+6) * 5

        self.age = roll(89-15) +15

    def check_experience(self, c):
        x = getattr(self,c)
        if d(1, 100) > x:
            setattr(self,c, x+d(1, 10))

    def roll_age(self):
        if self.age > 79:
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.C_FOR -= 80
            self.C_CON -= 80
            self.C_DEX -= 80
            self.C_APP -= 25
        elif self.age > 69:
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.C_FOR -= 40
            self.C_CON -= 40
            self.C_DEX -= 40
            self.C_APP -= 20

        elif self.age > 69:
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.C_FOR -= 20
            self.C_CON -= 20
            self.C_DEX -= 20
            self.C_APP -= 15
        elif self.age > 49:
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.C_FOR -= 10
            self.C_CON -= 10
            self.C_DEX -= 10
            self.C_APP -= 10
        elif self.age > 39:
            self.check_experience('C_EDU')
            self.check_experience('C_EDU')
            self.C_FOR -= 5
            self.C_CON -= 5
            self.C_DEX -= 5
            self.C_APP -= 5
        elif self.age > 19:
            self.check_experience('C_EDU')
        elif self.age < 19:
            self.C_FOR -= 5
            self.C_TAI -= 5
            self.C_EDU -= 5
            new_chance = d(3, 6) * 5
            if new_chance > self.C_CHANCE:
                self.C_CHANCE = new_chance
        self.birthdate = 1920 - self.age

    def check_bounds(self, c):
        x = getattr(self, c)
        do = False
        if x < 1:
            x = 1
            do = True
        elif x > 99:
            x = 99
            do = True
        if do:
            setattr(self, c, x)

    def bound(self):
        l = ['C_INT', 'C_EDU', 'C_APP', 'C_FOR', 'C_DEX', 'C_POU', 'C_TAI', 'C_CON']
        self.C_TOTAL = 0
        for x in l:
            self.check_bounds(x)
            self.C_TOTAL += getattr(self, x)


    def roll(self):
        self.get_rid(self.full_name)
        self.roll_attributes()
        self.roll_age()
        self.bound()

    def recalc(self):
        self.get_rid(self.full_name)
        self.roll_age()
        self.bound()


def roll_investigator(modeladmin, request, queryset):
    for investigator in queryset:
        investigator.roll()
        investigator.save()
    short_description = "Roll investigator"


def recalc_investigator(modeladmin, request, queryset):
    for investigator in queryset:
        investigator.recalc()
        investigator.save()
    short_description = "Recalc investigator"


class InvestigatorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'rid', 'C_TOTAL', 'age', 'C_FOR', 'C_DEX', 'C_CON', 'C_TAI', 'C_APP', 'C_INT', 'C_EDU', 'C_POU']
    actions = [roll_investigator, recalc_investigator]