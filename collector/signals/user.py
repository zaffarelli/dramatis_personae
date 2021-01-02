from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from collector.models.profile import Profile


@receiver(pre_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, **kwargs):
    all_profiles = Profile.objects.get(user=instance)
    if len(all_profiles) == 0:
        p = Profile()
        p.user = instance
        p.save()
