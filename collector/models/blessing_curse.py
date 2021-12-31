'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from collector.models.character import Character
from collector.models.character_custo import CharacterCusto


class BlessingCurseRef(models.Model):
    class Meta:
        ordering = ['reference']
        verbose_name = "FICS: Blessing/Curse"

    reference = models.CharField(max_length=64, default='', blank=True)
    value = models.IntegerField(default=0)
    description = models.TextField(max_length=256, default='')
    source = models.CharField(max_length=32, default='FS2CRB')

    def __str__(self):
        return '%s (%+d)' % (self.reference, self.value)

    def to_json(self):
        from collector.utils.basic import json_default
        import json
        jstr = json.loads(json.dumps(self, default=json_default, sort_keys=True, indent=4))
        return jstr


class BlessingCurse(models.Model):
    class Meta:
        ordering = ['character', 'blessing_curse_ref']

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    blessing_curse_ref = models.ForeignKey(BlessingCurseRef, on_delete=models.CASCADE)

    def __str__(self):
        return '%s (%s)' % (self.character.full_name, self.blessing_curse_ref.reference)


class BlessingCurseCusto(models.Model):
    class Meta:
        ordering = ['character_custo', 'blessing_curse_ref']

    character_custo = models.ForeignKey(CharacterCusto, on_delete=models.CASCADE)
    blessing_curse_ref = models.ForeignKey(BlessingCurseRef, on_delete=models.CASCADE)


class BlessingCurseModificator(models.Model):
    class Meta:
        ordering = ['tour_of_duty_ref', 'blessing_curse_ref']

    from collector.models.tourofduty import TourOfDutyRef
    tour_of_duty_ref = models.ForeignKey(TourOfDutyRef, on_delete=models.CASCADE)
    blessing_curse_ref = models.ForeignKey(BlessingCurseRef, on_delete=models.CASCADE)

    def __str__(self):
        return '%s (%s)' % (self.tour_of_duty_ref.reference, self.blessing_curse_ref.reference)


# Inlines
class BlessingCurseModificatorInline(admin.TabularInline):
    model = BlessingCurseModificator


class BlessingCurseInline(admin.TabularInline):
    model = BlessingCurse


class BlessingCurseCustoInline(admin.TabularInline):
    model = BlessingCurseCusto


# Admin
class BlessingCurseRefAdmin(admin.ModelAdmin):
    ordering = ('reference',)
    search_fields = ('reference', 'description')


class BlessingCurseModificatorAdmin(admin.ModelAdmin):
    ordering = ('blessing_curse_ref',)
