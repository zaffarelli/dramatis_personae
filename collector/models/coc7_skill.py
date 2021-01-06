"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from django.contrib import admin
from collector.models.investigator import Investigator
from collector.models.coc7_occupation import Coc7Occupation


C7S_CATEGORIES = (
    ('N/A','Aucune'),
    ('CAD','Combat à distance'),
    ('CRA','Combat rapproché'),
    ('SCI','Sciences'),
    ('A&M','Arts & Métiers'),
    ('SOC', 'Social'),
)

C7S_SPECIAL_BASES = (
    ('N/A','NORMAL'),
    ('DEX based','DEX/2'),
    ('EDU based','EDU'),
)
class Coc7SkillRef(models.Model):
    class Meta:
        ordering = ['reference','is_root','is_speciality', 'is_wildcard', ]
        verbose_name = "COC7: Skill Reference"

    reference = models.CharField(max_length=200, unique=True)
    smart_code = models.CharField(max_length=200, default='TBD')
    base = models.PositiveIntegerField(default=0)
    special_base = models.CharField(default='N/A',max_length=16,choices=C7S_SPECIAL_BASES)
    era = models.CharField(max_length=4, default=1920)
    is_root = models.BooleanField(default=False)
    is_speciality = models.BooleanField(default=False)
    is_common = models.BooleanField(default=True)
    is_wildcard = models.BooleanField(default=False)
    category = models.CharField(max_length=3, default='N/A',choices=C7S_CATEGORIES)
    linked_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def fix(self):
        from collector.utils.rpg import smart_code
        self.smart_code = smart_code(self.reference)

    def __str__(self):
        return f'{self.reference}'


class Coc7Skill(models.Model):
    class Meta:
        ordering = ['skill_ref', ]
        verbose_name = "Investigators Skill"
    investigator = models.ForeignKey(Investigator, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(Coc7SkillRef, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.investigator.rid} {self.skill_ref.smart_code}'


class Coc7SkillModificator(models.Model):
    class Meta:
        ordering = ['skill_ref']
    occupation = models.ForeignKey(Coc7Occupation, on_delete=models.CASCADE)
    skill_ref = models.ForeignKey(Coc7SkillRef, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.occupation.smart_code, self.skill_ref.smart_code)


# Inlines
class Coc7SkillModificatorInline(admin.TabularInline):
    model = Coc7SkillModificator
    extras = 3
    ordering = ['occupation', 'skill_ref']

# Admins
def refix(modeladmin, request, queryset):
    for item in queryset:
        item.save()
    short_description = "Refix by forced save'()"

class Coc7SkillRefAdmin(admin.ModelAdmin):
    ordering = ['smart_code','category','is_root','is_speciality', 'is_wildcard']
    list_display = ['reference', 'base', 'special_base','category','smart_code', 'is_root', 'is_speciality', 'is_wildcard', 'is_common', 'linked_to']
    actions = [refix]
    list_filter = ['category','linked_to']