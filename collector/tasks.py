from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.contrib import messages


@shared_task
def add(x, y):
    return x + y


@shared_task
def build_pdf(rid):
    from collector.models.character import Character
    c = Character.objects.get(rid=rid)
    c.need_pdf = True
    if c.need_pdf:
        #messages.warning(f'Task: Building PDF for {c.rid}')
        c.backup()



@shared_task
def recalc_avatar(rid, page):
    from collector.models.character import Character
    c = Character.objects.get(rid=rid)
    c.page_num = page
    c.need_pdf = False
    #messages.warning(f'Task: Recalculating {c.rid}')
    c.save()



