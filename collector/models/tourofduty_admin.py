from django.contrib import admin
from collector.utils.helper import refix, extract


class TourOfDutyRefAdmin(admin.ModelAdmin):
    from collector.models.skill import SkillModificatorInline
    from collector.models.degree import DegreeModificatorInline
    from collector.models.benefice_affliction import BeneficeAfflictionModificatorInline
    from collector.models.blessing_curse import BlessingCurseModificatorInline
    ordering = ['is_public', '-valid', 'is_kit', 'category', '-core', 'caste', 'topic', 'value', 'reference', ]
    list_display = ['reference', 'caste', 'degrees_wp_choices','category', 'is_custom', 'valid', 'balance', 'topic','subtopic',
                    'source', 'AP', 'SP', 'DP', 'BCP', 'BAP', 'WP', 'OP', 'value']
    exclude = ['value']
    actions = [refix, extract]
    inlines = [
        SkillModificatorInline,
        DegreeModificatorInline,
        BeneficeAfflictionModificatorInline,
        BlessingCurseModificatorInline
    ]
    list_filter = ['is_public', 'core', 'category', 'valid', 'caste', 'topic', 'subtopic', 'is_kit', 'is_custom']
    list_editable = ['topic', 'subtopic']
    search_fields = ['reference', 'description']
