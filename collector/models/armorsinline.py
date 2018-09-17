from django.contrib import admin
from collector.models.armors import Armor

class ArmorInline(admin.TabularInline):
  model = Armor
