from django.contrib import admin
from collector.models.weapons import Weapon

class WeaponInline(admin.TabularInline):
  model = Weapon
