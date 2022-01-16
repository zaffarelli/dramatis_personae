from django.db.models.signals import pre_save
from django.dispatch import receiver
from cartograph.models.system import OrbitalItem


@receiver(pre_save, sender=OrbitalItem, dispatch_uid='prepare_orbital_data')
def prepare_orbital_data(sender, instance, **kwargs):
    instance.prepare()
