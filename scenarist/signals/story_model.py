from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from scenarist.models.cards import Card
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Card, dispatch_uid='fix_card')
def fix_card(sender, instance, **kwargs):
    if instance.saved:
        for c in instance.children.all():
            c.save()
    instance.fix()


@receiver(post_save, sender=Card, dispatch_uid='post_fix_card')
def post_fix_card(sender, instance, **kwargs):
    instance.post_fix()


