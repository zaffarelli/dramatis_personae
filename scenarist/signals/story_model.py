from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scenarist.models.acts import Act
from scenarist.models.dramas import Drama
from scenarist.models.events import Event
from scenarist.models.epics import Epic
from scenarist.models.cards import Card, Challenge
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Act, dispatch_uid='fix_act')
def fix_act(sender, instance, **kwargs):
    instance.full_id = instance.get_full_id
    # print(f"Saving!!! {instance.title}")


@receiver(pre_save, sender=Drama, dispatch_uid='fix_drama')
def fix_drama(sender, instance, **kwargs):
    instance.full_id = instance.get_full_id
    # print(f"Saving!!! {instance.title}")


@receiver(pre_save, sender=Event, dispatch_uid='fix_event')
def fix_event(sender, instance, **kwargs):
    instance.full_id = instance.get_full_id
    # print(f"Saving!!! {instance.title}")


@receiver(pre_save, sender=Epic, dispatch_uid='fix_epic')
def fix_epic(sender, instance, **kwargs):
    instance.full_id = instance.get_full_id
    # print(f"Saving!!! {instance.title}")


@receiver(pre_save, sender=Card, dispatch_uid='fix_card')
def fix_card(sender, instance, **kwargs):
    if instance.saved:
        for c in instance.children.all():
            c.save()
    instance.fix()


@receiver(post_save, sender=Card, dispatch_uid='post_fix_card')
def post_fix_card(sender, instance, **kwargs):
    instance.post_fix()


@receiver(pre_save, sender=Challenge, dispatch_uid='fix_challenge')
def fix_challenge(sender, instance, **kwargs):
    instance.fix()
