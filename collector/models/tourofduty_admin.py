"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.contrib import admin


def refix(modeladmin, request, queryset):
    for tour_of_duty_ref in queryset:
        tour_of_duty_ref.fix()
        tour_of_duty_ref.save()
    short_description = "Do fix"


def unset_core(modeladmin, request, queryset):
    for tour_of_duty_ref in queryset:
        tour_of_duty_ref.core = False
        tour_of_duty_ref.save()
    short_description = "Unset core"


def set_core(modeladmin, request, queryset):
    for tour_of_duty_ref in queryset:
        tour_of_duty_ref.core = True
        tour_of_duty_ref.save()
    short_description = "Set core"


class TourOfDutyRefAdmin(admin.ModelAdmin):
    from collector.models.skill import SkillModificatorInline
    from collector.models.benefice_affliction import BeneficeAfflictionModificatorInline
    from collector.models.blessing_curse import BlessingCurseModificatorInline
    ordering = ['-core', 'category', 'topic', 'reference', 'caste', 'value']
    list_display = ['reference', 'category', 'caste', 'valid', 'core', 'balance', 'topic', 'is_custom', 'source', 'AP',
                    'OP', 'balance_AP', 'balance_OP',
                    'value',
                    'description']
    exclude = ['value']
    actions = [refix, unset_core, set_core]
    inlines = [
        SkillModificatorInline,
        BeneficeAfflictionModificatorInline,
        BlessingCurseModificatorInline
    ]
    list_filter = ['core', 'category', 'valid', 'caste', 'topic']
    search_fields = ['reference']
