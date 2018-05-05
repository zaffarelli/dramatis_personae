from django.contrib import admin

# Register your models here.
from .models import Character, SkillRef, Skill, CharacterAdmin, SkillInline, SkillAdmin, SkillRefAdmin


admin.site.register(SkillRef, SkillRefAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Skill, SkillAdmin)



