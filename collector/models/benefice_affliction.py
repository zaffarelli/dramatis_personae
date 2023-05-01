"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from django.db import models
from collector.models.character import Character
from collector.models.tourofduty import TourOfDutyRef
from django.contrib import admin
from collector.mixins.uuid_class import UUIDClass


class BeneficeAfflictionRef(UUIDClass):
    class Meta:
        verbose_name = "FICS: Benefice/Affliction"
        ordering = ['reference', 'value', ]

    reference = models.CharField(max_length=64)
    value = models.IntegerField(default=0)
    category = models.CharField(max_length=2, default='ot', choices=(
        ('ba', 'Background'),
        ('co', 'Community'),
        ('po', 'Possessions'),
        ('ri', 'Riches'),
        ('st', 'Status'),
        ('cm', 'Combat'),
        ('oc', 'Occult'),
        ('ta', 'Talent'),
        ('ot', 'Other')))
    description = models.TextField(max_length=256, default='', blank=True)
    source = models.CharField(max_length=32, default='FS2CRB')
    emphasis = models.CharField(max_length=64, default='', blank=True)
    ranking = models.BooleanField(default=False)
    cash_value = models.BooleanField(default=False)
    watermark = models.CharField(max_length=64, default='', blank=True)

    def __str__(self):
        return '%s %s(%d)' % (self.reference, self.emphasis, self.value)

    def fix(self):
        super().fix()

    def to_json(self):
        from collector.utils.basic import json_default
        import json
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class BeneficeAffliction(models.Model):
    class Meta:
        ordering = ['benefice_affliction_ref']

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    benefice_affliction_ref = models.ForeignKey(BeneficeAfflictionRef, on_delete=models.CASCADE)
    # value = models.IntegerField(default=0)
    description = models.TextField(max_length=256, default='', blank=True)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.benefice_affliction_ref.reference)

    def to_json(self):
        jstr = {}
        from collector.utils.basic import json_default_simple
        import json
        jstr = {"id": self.pk, "description": self.description }
        jstr['benefice_affliction_ref'] = self.benefice_affliction_ref.to_json()
        return jstr


def make_occult(modeladmin, request, queryset):
    queryset.update(category="oc")
    short_description = "Make Occult"


def make_combat(modeladmin, request, queryset):
    queryset.update(category="cm")
    short_description = "Make Combat"


def make_talent(modeladmin, request, queryset):
    queryset.update(category="ta")
    short_description = "Make Talent"


def make_possession(modeladmin, request, queryset):
    queryset.update(category="po")
    short_description = "Make possession"


def make_riches(modeladmin, request, queryset):
    queryset.update(category="ri")
    short_description = "Make riches"


def refix(modeladmin, request, queryset):
    for benefixe_affliction_ref in queryset:
        benefixe_affliction_ref.save()
    short_description = "Do fix"


class BeneficeAfflictionRefAdmin(admin.ModelAdmin):
    ordering = ('category', 'reference', 'watermark', '-value', 'ranking')
    list_display = (
        'reference', 'emphasis', 'value', 'watermark', 'category', 'ranking', 'cash_value', 'description',
        'source')
    search_fields = ('reference', 'description', 'emphasis', 'watermark')
    list_filter = ('ranking', 'source', 'watermark', 'category', 'emphasis')
    actions = [refix, make_occult, make_combat, make_talent, make_riches, make_possession]


class BeneficeAfflictionModificator(models.Model):
    class Meta:
        ordering = ['benefice_affliction_ref']

    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    benefice_affliction_ref = models.ForeignKey(BeneficeAfflictionRef, on_delete=models.CASCADE)
    description = models.TextField(max_length=256, default='', blank=True)

    def __str__(self):
        return '%s=%s' % (self.tour_of_duty_ref.reference, self.benefice_affliction_ref.reference)


class BeneficeAfflictionCusto(models.Model):
    class Meta:
        ordering = ['character_custo', 'benefice_affliction_ref']

    from collector.models.character_custo import CharacterCusto
    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    benefice_affliction_ref = models.ForeignKey(BeneficeAfflictionRef, on_delete=models.CASCADE)
    description = models.TextField(max_length=256, default='', blank=True)


# Inlines
class BeneficeAfflictionCustoInline(admin.TabularInline):
    model = BeneficeAfflictionCusto


class BeneficeAfflictionInline(admin.TabularInline):
    model = BeneficeAffliction


class BeneficeAfflictionModificatorInline(admin.TabularInline):
    model = BeneficeAfflictionModificator


class BeneficeAfflictionRefInline(admin.TabularInline):
    model = BeneficeAfflictionRef
