from django.db.models.signals import pre_save,post_init
from collector.models.character_custo import CharacterCusto
from collector.models.character import Character
from django.dispatch import receiver
from datetime import datetime
from django.utils.timezone import get_current_timezone


@receiver(pre_save, sender=CharacterCusto, dispatch_uid='update_character_custo')
def update_character_custo(sender, instance, conf=None, **kwargs):
    instance.fix()


@receiver(pre_save, sender=Character, dispatch_uid='update_character')
def update_character(sender, instance, conf=None, **kwargs):
    """ Before saving, fix() and  get_RID() for the character """
    if instance.need_fix:
        instance.fix()
    instance.pub_date = datetime.now(tz=get_current_timezone())


# @receiver(post_init, sender=Character, dispatch_uid='post_init_character')
# def post_init_character(sender, instance, conf=None, **kwargs):
#     instance.check_cc()