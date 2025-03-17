"""
╔╦╗╔═╗  ╔═╗┌─┐┌┬┐┬┌┬┐┬┌─┐┌─┐┬─┐
 ║║╠═╝  ║ ║├─┘ │ │││││┌─┘├┤ ├┬┘
═╩╝╩    ╚═╝┴   ┴ ┴┴ ┴┴└─┘└─┘┴└─
"""
from django.db import models
from django.contrib import admin


class CelestialShipCard(models.Model):

    class CategoryChoices(models.TextChoices):
        PILOT = ("PIL","Pilot")
        ENGINEER = ("ENG", "Engineer")
        BOTH = ("BOTH","Both")

    class Meta:
        ordering = ['level','name']

    name = models.CharField(max_length=256)
    complement = models.CharField(max_length=256, default="", blank=True)
    category = models.CharField(max_length=128, choices=CategoryChoices.choices, default=CategoryChoices.BOTH, blank=True)
    description = models.TextField(max_length=1024, default="", blank=True)
    level = models.IntegerField(default=1, blank=True)
    power = models.IntegerField(default=1, blank=True)
    time_units = models.IntegerField(default=1, blank=True)

    def __str__(self):
        return f"{self.name}"


class CelestialShipCardAdmin(admin.ModelAdmin):
    model = CelestialShipCard
    list_display = ['name', 'complement', 'category', 'description', 'power', 'time_units', 'level']
    list_filter = ['complement','category', 'level', 'power', 'time_units']
    list_editable = ['complement', 'category', 'level', 'power', 'time_units', 'description']
