from django.db.models.signals import pre_save
from django.dispatch import receiver
from collector.models.collection import Collection


@receiver(pre_save, sender=Collection, dispatch_uid='update_collection')
def update_collection(sender, instance, **kwargs):
    try:
        instance.fix()
    except:
        print("whoopsie")

