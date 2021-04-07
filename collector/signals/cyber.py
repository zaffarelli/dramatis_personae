from django.db.models.signals import pre_save
from django.dispatch import receiver
from collector.models.cyberware import CyberwareRef
from collector.models.weapon import WeaponRef


@receiver(pre_save, sender=CyberwareRef, dispatch_uid='update_cyberware_ref')
def update_cyberware_ref(sender, instance, **kwargs):
    instance.fix()

@receiver(pre_save, sender=WeaponRef, dispatch_uid='update_weapon_ref')
def update_weapon_ref(sender, instance, **kwargs):
    instance.fix()
