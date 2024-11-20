from django.contrib import admin
from collector.utils.helper import refix, extract


class TourOfDutyRefAdmin(admin.ModelAdmin):
    from collector.models.skill import SkillModificatorInline
    from collector.models.degree import DegreeModificatorInline
    from collector.models.benefice_affliction import BeneficeAfflictionModificatorInline
    from collector.models.blessing_curse import BlessingCurseModificatorInline
    ordering = ['is_public','is_kit', '-valid','category', '-core', 'caste',  'topic', 'value', 'reference', ]
    list_display = ['reference', 'caste', 'category', 'is_public', 'is_kit', 'is_custom', 'core', 'valid', 'balance', 'topic',
                    'source', 'AP', 'SP', 'DP', 'BCP', 'BAP', 'WP', 'OP', 'value', 'description', 'rid']
    exclude = ['value']
    actions = [refix, extract]
    inlines = [
        SkillModificatorInline,
        DegreeModificatorInline,
        BeneficeAfflictionModificatorInline,
        BlessingCurseModificatorInline
    ]
    list_filter = ['is_public','core', 'category', 'valid', 'caste', 'topic', 'is_kit', 'is_custom']
    list_editable = ['is_public','is_kit']
    search_fields = ['reference', 'description']
