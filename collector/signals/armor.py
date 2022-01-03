from django.db.models.signals import pre_save
from collector.models.armor import ArmorRef
from django.dispatch import receiver


@receiver(pre_save, sender=ArmorRef, dispatch_uid='update_armor_ref')
def update_armor_ref(sender, instance, conf=None, **kwargs):
    instance.fix()
