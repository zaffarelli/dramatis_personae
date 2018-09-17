from django.contrib import admin
from collector.models.talents import Talent

class TalentInline(admin.TabularInline):
  model = Talent
