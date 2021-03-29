from django.db.models.signals import pre_save
from django.dispatch import receiver
from collector.models.policy import Policy

@receiver(pre_save, sender=Policy, dispatch_uid='update_policy')
def update_policy(sender, instance, **kwargs):
    instance.fix()
