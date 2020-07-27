'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db import models
from collector.models.character import Character
from django.dispatch import receiver
from django.contrib import admin
from django.db.models.signals import pre_save, post_save


class TalentRef(models.Model):
    class Meta:
        ordering = ['reference']
        verbose_name = "Talent Reference"

    reference = models.CharField(max_length=64, default='', blank=True)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    description = models.TextField(max_length=1024, default='', blank=True)

    def __str__(self):
        return '%s [%d]' % (self.reference, self.value)

    def fix(self):
        self.value = self.AP * 3 + self.OP


@receiver(pre_save, sender=TalentRef, dispatch_uid='update_talent_ref')
def update_talent_ref(sender, instance, **kwargs):
    instance.fix()


class Talent(models.Model):
    class Meta:
        ordering = ['name']

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, default='', blank=True)
    attributes_list = models.CharField(max_length=128, default='', blank=True)
    skills_list = models.CharField(max_length=128, default='', blank=True)
    description = models.TextField(max_length=1024, default='', blank=True)
    AP = models.IntegerField(default=0)
    OP = models.IntegerField(default=0)
    value = models.IntegerField(default=0)
    talent_ref = models.ForeignKey(TalentRef, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return '%s=%s' % (self.character.full_name, self.name)

    def fix(self):
        self.value = self.AP * 3 + self.OP + self.talent_ref.value


@receiver(pre_save, sender=Talent, dispatch_uid='update_talent')
def update_talent(sender, instance, **kwargs):
    instance.fix()


class TalentRefAdmin(admin.ModelAdmin):
    ordering = ['reference', 'value']
    list_display = ('reference', 'AP', 'OP', 'value', 'description')
