from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from collector.models.degree import Degree, DegreeModificator, DegreeRef

# SkillRef
@receiver(pre_save, sender=DegreeRef, dispatch_uid='update_degreeref')
def update_degreeref(sender, instance, **kwargs):
    instance.fix()

# Skill
@receiver(pre_save, sender=Degree, dispatch_uid='update_degree')
def update_degree(sender, instance, **kwargs):
    instance.fix()

@receiver(pre_save, sender=DegreeModificator, dispatch_uid='update_degree_modificator')
def update_degree_modificator(sender, instance, **kwargs):
    instance.fix()

