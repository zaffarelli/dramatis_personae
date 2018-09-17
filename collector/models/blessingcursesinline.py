from django.contrib import admin
from collector.models.blessings_curses import BlessingCurse

class BlessingCurseInline(admin.TabularInline):
  model = BlessingCurse
