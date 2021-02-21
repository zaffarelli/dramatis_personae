'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from collector.models.benefice_affliction import BeneficeAfflictionRef

# BeneficeAfflictionRef
@receiver(pre_save, sender=BeneficeAfflictionRef, dispatch_uid='update_benefice_affliction_ref')
def update_benefice_affliction_ref(sender, instance, **kwargs):
    instance.fix()

