"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
import json

class Specie(models.Model):
    class Meta:
        ordering = ['species', 'race']
        unique_together = (('species', 'race'),)
        verbose_name = "FICS: Specie"

    species = models.CharField(max_length=64, default=1)
    race = models.CharField(max_length=64, default='')
    # racial_attr_mod = models.CharField(max_length=128, default='{}')
    # racial_skills = models.CharField(max_length=512, default='{}')
    # racial_occult = models.CharField(max_length=128, default='{}')
    # attr_mod_balance = models.IntegerField(default=0)
    # skill_balance = models.IntegerField(default=0)
    description = models.TextField(max_length=512, default='', blank=True)
    ra_tod_name = models.CharField(max_length=64, default='', blank=True)
    br_tod_name = models.CharField(max_length=64, default='', blank=True)


    def __str__(self):
        return '%s %s' % (self.species, self.race)

    def set_racial_skills(self, data):
        self.racial_skills = json.dumps(data)

    def get_racial_skills(self):
        return json.loads(self.racial_skills)

    def set_racial_attr_mod(self, data):
        self.racial_attr_mod = json.dumps(data)

    def get_racial_attr_mod(self):
        return json.loads(self.racial_attr_mod)

    def update_balance(self):
        attr_mods = self.get_racial_attr_mod()
        b = 0
        for am in attr_mods:
            b += attr_mods[am]
        self.attr_mod_balance = b
        # print('PA --> %s:%d'%(self,b))
        skills_mods = self.get_racial_skills()
        b = 0
        for sm in skills_mods:
            b += skills_mods[sm]
        self.skill_balance = b
        # print('Skill --> %s:%d'%(self,b))
        self.save()


class SpecieAdmin(admin.ModelAdmin):
    ordering = ['species', 'race']
    list_display = [ 'species', 'race', 'ra_tod_name','br_tod_name','description']
    search_fields = ['species', 'race', 'ra_tod_name','br_tod_name']
    list_filter = ['species', 'ra_tod_name','br_tod_name']

