from django.contrib import admin

# Register your models here.
from .models import Character, SkillRef, Skill

admin.site.register(Character)
admin.site.register(SkillRef)
admin.site.register(Skill)
