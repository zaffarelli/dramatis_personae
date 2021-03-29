from django.db.models.signals import pre_save
from django.dispatch import receiver
from collector.models.tourofduty import TourOfDutyRef
from datetime import datetime


@receiver(pre_save, sender=TourOfDutyRef, dispatch_uid='update_tour_of_duty_ref')
def update_tour_of_duty_ref(sender, instance, **kwargs):
    from django.utils.timezone import get_current_timezone
    instance.pub_date = datetime.now(tz=get_current_timezone())
