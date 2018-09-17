from django.contrib import admin
from collector.models.skills import Skill

class SkillInline(admin.TabularInline):
  model = Skill
  extras = 10
  ordering = ('skill_ref',)
