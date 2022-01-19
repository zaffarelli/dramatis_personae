from django.db.models.signals import pre_save
from django.dispatch import receiver
from cartograph.models.system import OrbitalItem, System


@receiver(pre_save, sender=OrbitalItem, dispatch_uid='fix_orbital_data')
def fix_orbital_data(sender, instance, **kwargs):
    instance.fix()


@receiver(pre_save, sender=System, dispatch_uid='fix_system')
def fix_system(sender, instance, **kwargs):
    instance.fix()
