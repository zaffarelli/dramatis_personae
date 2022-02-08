from django.db import models
from django.contrib import admin
import json


class Sequence(models.Model):
    class Meta:
        ordering = ['reference']
        verbose_name = "FICS: Sequence"

    reference = models.CharField(max_length=64, default='', unique=True)
    order = models.PositiveIntegerField(default=0, blank=True)
    data = models.TextField(max_length=4096, default='', blank=True)

    @property
    def hr_data(self):
        value = json.loads(self.data)
        return value


class SequenceAdmin(admin.ModelAdmin):
    ordering = ['reference', 'order']
    list_display = ['reference', 'data']
    list_filter = ['reference']
    search_fields = ['reference']
