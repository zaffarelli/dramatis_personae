'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.contrib import admin
from collector.models.character_custo import CharacterCusto

class CharacterCustoAdmin(admin.ModelAdmin):
    from collector.models.skill import SkillCustoInline
    from collector.models.blessing_curse import BlessingCurseCustoInline
    from collector.models.benefice_affliction import BeneficeAfflictionCustoInline
    from collector.models.weapon import WeaponCustoInline
    from collector.models.armor import ArmorCustoInline
    from collector.models.shield import ShieldCustoInline
    from collector.models.ritual import RitualCustoInline
    list_display = ('character','value','AP','OP',)
    exclude = ('value','AP','OP')
    inlines = [
        SkillCustoInline,
        BlessingCurseCustoInline,
        BeneficeAfflictionCustoInline,
        WeaponCustoInline,
        ArmorCustoInline,
        ShieldCustoInline,
        RitualCustoInline,
    ]
    ordering = ['character__full_name',]
