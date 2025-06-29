from django.contrib import admin
from collector.utils.helper import refix, extract


class TourOfDutyRefAdmin(admin.ModelAdmin):
    from collector.models.skill import SkillModificatorInline
    from collector.models.degree import DegreeModificatorInline
    from collector.models.benefice_affliction import BeneficeAfflictionModificatorInline
    from collector.models.blessing_curse import BlessingCurseModificatorInline
    ordering = ['-is_public', '-valid', 'category', 'is_kit', '-core', 'caste', 'topic', 'value', 'reference', ]
    list_display = ['reference', 'caste', 'category', 'is_custom', 'valid',
                    'AP', "AWP", 'SK', 'SWP', 'DE', "DWP", 'BC', 'BCW', 'BA', 'BAW', 'value', 'topic', 'subtopic']
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
