'''
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
'''
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from collector.models.skill import SkillRef, Skill, SkillModificator

# SkillRef
@receiver(pre_save, sender=SkillRef, dispatch_uid='update_skillref')
def update_skillref(sender, instance, **kwargs):
    instance.fix()

# Skill
@receiver(pre_save, sender=Skill, dispatch_uid='update_skill')
def update_skill(sender, instance, **kwargs):
    instance.fix()

# SkillModificator
@receiver(pre_save, sender=SkillModificator, dispatch_uid='update_skill_modificator')
def update_skill_modificator(sender, instance, **kwargs):
    instance.fix()