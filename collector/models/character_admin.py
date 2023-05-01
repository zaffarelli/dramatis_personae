"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.contrib import admin
from collector.models.skill import SkillInline
from collector.models.cyberware import CyberwareInline
from collector.models.tourofduty import TourOfDutyInline
from collector.models.blessing_curse import BlessingCurseInline
from collector.models.benefice_affliction import BeneficeAfflictionInline
# from cartograph.models.talent_inline import TalentInline
from collector.models.weapon import WeaponInline
from collector.models.armor import ArmorInline
from collector.models.shield import ShieldInline
from collector.models.bloke import BlokeInline
from collector.models.ritual import RitualInline



# def cast_to_dem(modeladmin, request, queryset):
#     e = Epic.objects.filter(shortcut="DEM").first()
#     queryset.update(epic=e)
#     short_description = "Cast to the Deus Ex Machina epic."
#
#
# def cast_to_blank(modeladmin, request, queryset):
#     e = Epic.objects.filter(shortcut="BLK").first()
#     queryset.update(epic=e)
#     short_description = "Cast to no epic."
#

def no_importance(modeladmin, request, queryset):
    queryset.update(importance=0)
    short_description = "Importance to 0 (no gs export)"


def importance_up(modeladmin, request, queryset):
    for character in queryset:
        character.importance = character.importance + 1
        character.save()
    short_description = "Importance ++"


def importance_down(modeladmin, request, queryset):
    for character in queryset:
        character.importance = character.importance - 1
        character.save()
        short_description = "Importance --"


# def cast_to_antu(modeladmin, request, queryset):
#     e = Epic.objects.filter(shortcut="ANTU").first()
#     queryset.update(epic=e)
#     short_description = "Cast to Abusus Non Tollit Usum"
#

def recalc_height(modeladmin, request, queryset):
    for c in queryset:
        if "urthish" in c.specie.species.lower():
            c.height = 0
            c.need_fix = True
            c.fix()
            c.save()
    short_description = "Recalculate urthish height/weight"


def make_invisible(modeladmin, request, queryset):
    queryset.update(is_visible=False)
    short_description = "Make invisible"


def make_visible(modeladmin, request, queryset):
    queryset.update(is_visible=True)
    short_description = "Make visible"


def make_public(modeladmin, request, queryset):
    queryset.update(is_public=True)
    short_description = "Make public"


def make_private(modeladmin, request, queryset):
    queryset.update(is_public=False)
    short_description = "Make private"


def make_partial(modeladmin, request, queryset):
    queryset.update(is_partial=True)
    short_description = "Make partial"


def make_complete(modeladmin, request, queryset):
    queryset.update(is_partial=False)
    short_description = "Make complete"


def make_teutonic(modeladmin, request, queryset):
    queryset.update(specie=1)
    short_description = "Make teutonic"


def make_kaanic(modeladmin, request, queryset):
    queryset.update(specie=25)
    short_description = "Make kaanic"


def make_castillan(modeladmin, request, queryset):
    queryset.update(specie=22)
    short_description = "Make castillan"


def make_enquist(modeladmin, request, queryset):
    queryset.update(specie=23)
    short_description = "Make enquist"


def enter_fencing_league(modeladmin, request, queryset):
    queryset.update(fencing_league=True)
    short_description = "Enter fencing league"


def exit_fencing_league(modeladmin, request, queryset):
    queryset.update(fencing_league=False)
    short_description = "Exit fencing league"


def needs_fix(modeladmin, request, queryset):
    queryset.update(need_fix=True)
    short_description = "Need fix"


def needs_pdf(modeladmin, request, queryset):
    queryset.update(need_pdf=True)
    short_description = "Need PDF"


class CharacterAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'need_fix','player', "ranking", "id", 'importance', 'entrance', 'specie', 'alliance_ref',
                    'is_dead', 'life_path_total', 'OP',
                    'audit', 'is_visible']
    inlines = [
        SkillInline,
        BlessingCurseInline,
        BeneficeAfflictionInline,
        # TalentInline,
        WeaponInline,
        ArmorInline,
        ShieldInline,
        TourOfDutyInline,
        BlokeInline,
        RitualInline,
        CyberwareInline,
    ]
    ordering = ['full_name', ]
    actions = [needs_fix, needs_pdf, no_importance, importance_up, importance_down, make_invisible,
               make_visible, make_teutonic, make_kaanic, make_castillan, make_enquist, make_public, make_private,
               make_partial, make_complete, enter_fencing_league, exit_fencing_league, recalc_height]
    exclude = ['SA_REC', 'SA_STA', 'SA_END', 'SA_STU', 'SA_RES', 'SA_DMG', 'SA_TOL', 'SA_HUM', 'SA_PAS', 'SA_WYR',
               'SA_SPD', 'SA_RUN', 'PA_TOTAL', 'SK_TOTAL', 'TA_TOTAL', 'BC_TOTAL', 'BA_TOTAL']
    list_filter = ['fencing_league', 'nameless', 'team', 'occult', 'alliance_ref', 'keyword', 'specie']
    search_fields = ['full_name', 'alias', 'keyword', 'rid', 'player']
    list_editable = ['need_fix']
