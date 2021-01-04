from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from collector.models.coc7_skill import Coc7SkillRef
from collector.models.coc7_occupation import Coc7Occupation


@receiver(pre_save, sender=Coc7SkillRef, dispatch_uid='update_coc7skillref')
def update_coc7skillref(sender, instance, **kwargs):
    instance.fix()

@receiver(pre_save, sender=Coc7Occupation, dispatch_uid='update_coc7occupation')
def update_coc7occupation(sender, instance, **kwargs):
    instance.fix()