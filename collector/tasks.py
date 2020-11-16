from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.contrib import messages

# from celery import Celery
# from celery.schedules import crontab
import logging

logger = logging.getLogger(__name__)


@shared_task
def todo():
    from collector.models.character import Character
    to_be_fixed = Character.objects.filter(need_fix=True)
    to_be_pdfed = Character.objects.filter(need_pdf=True)
    answer = f'Incoming list... To be fixed:{len(to_be_fixed)} Ready for PDF:{len(to_be_pdfed)}'
    logger.warning(answer)
    return answer


@shared_task
def pdf_check():
    answer = 'pdf_check task is idle'
    from collector.models.character import Character
    all = Character.objects.filter(need_pdf=True).order_by('-pub_date')
    if len(all):
        c = all.first()
        answer = f'Task: Building PDF for {c.rid}'
        c.backup()
        c.save()
    return answer


@shared_task
def fix_check():
    answer = 'fix_check task is idle'
    from collector.models.character import Character
    all = Character.objects.filter(need_fix=True).order_by('-pub_date')
    if len(all):
        c = all.first()
        answer = f'Task: Fixing avatar {c.rid}. {len(all)} remaining.'
        c.fix()
        c.save()
    logger.warning(answer)
    return answer



