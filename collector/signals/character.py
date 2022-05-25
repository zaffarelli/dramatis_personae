from django.db.models.signals import pre_save
from collector.models.character_custo import CharacterCusto
from collector.models.character import Character
from django.dispatch import receiver
from datetime import datetime
from django.utils.timezone import get_current_timezone


@receiver(pre_save, sender=CharacterCusto, dispatch_uid='update_character_custo')
def update_character_custo(sender, instance, conf=None, **kwargs):
    instance.recalculate()


@receiver(pre_save, sender=Character, dispatch_uid='update_character')
def update_character(sender, instance, conf=None, **kwargs):
    """ Before saving, fix() and  get_RID() for the character """
    instance.get_rid(instance.full_name)
    instance.pub_date = datetime.now(tz=get_current_timezone())
