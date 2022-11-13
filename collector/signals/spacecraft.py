from django.db.models.signals import pre_save
from django.dispatch import receiver
from collector.models.spacecraft import ShipRef
from collector.models.spacecraft import ShipSystem


@receiver(pre_save, sender=ShipRef, dispatch_uid='update_ship_ref')
def update_ship_ref(sender, instance, **kwargs):
    instance.fix()


@receiver(pre_save, sender=ShipSystem, dispatch_uid='update_ship_system')
def update_ship_system(sender, instance, **kwargs):
    instance.fix()
