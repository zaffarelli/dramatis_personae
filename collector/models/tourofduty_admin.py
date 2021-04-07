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


class TourOfDutyRefAdmin(admin.ModelAdmin):
    from collector.models.skill import SkillModificatorInline
    from collector.models.benefice_affliction import BeneficeAfflictionModificatorInline
    from collector.models.blessing_curse import BlessingCurseModificatorInline
    ordering = ['category', 'topic', 'reference', 'caste', 'value']
    list_display = ['reference', 'category', 'caste', 'valid', 'balance', 'topic', 'is_custom', 'source', 'AP', 'OP','balance_AP', 'balance_OP',
                    'value',
                    'description']
    exclude = ['value']
    actions = [refix]
    inlines = [
        SkillModificatorInline,
        BeneficeAfflictionModificatorInline,
        BlessingCurseModificatorInline
    ]
    list_filter = ['category', 'valid', 'caste', 'topic']
    search_fields = ['reference']
