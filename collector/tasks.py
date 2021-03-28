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
    from collector.models.tourofduty import TourOfDutyRef
    to_be_fixed = Character.objects.filter(need_fix=True)
    to_be_pdfed = Character.objects.filter(need_pdf=True)
    balanced = Character.objects.filter(balanced=True)
    all = Character.objects.all()
    tod_to_be_fixed = TourOfDutyRef.objects.filter(need_fix=True)
    logger.info(f'Incoming TODO list...')
    logger.info(f' - Characters to be fixed ..... {len(to_be_fixed)}')
    logger.info(f' - Characters ready for PDF ... {len(to_be_pdfed)}')
    logger.info(f' - Characters balanced ........ {len(balanced)}  / {len(all)}')
    logger.info(f' - ToDs to be fixed ........... {len(tod_to_be_fixed)}')
    answer = 'Todo'
    return answer


@shared_task
def pdf_check():
    answer = 'Pdf_check task is idle'
    from collector.models.character import Character
    all = Character.objects.filter(need_pdf=True).order_by('-pub_date')
    if len(all):
        c = all.first()
        answer = f'Task: Building PDF for {c.rid}'
        c.backup()
        c.save()
    logger.info(answer)
    return answer


@shared_task
def skills_check():
    answer = 'Skills_check task is idle'
    logger.info(answer)
    return answer


@shared_task
def tod_check():
    answer = 'Tod_check task is idle.'
    from collector.models.tourofduty import TourOfDutyRef
    tbf = TourOfDutyRef.objects.filter(need_fix=True)
    if len(tbf):
        tod = tbf.first()
        tod.fix()
        tod.save()
    else:
        fives = TourOfDutyRef.objects.order_by('pub_date').first(5)
        for t in fives:
            t.need_fix = True
            t.save()
        answer = f'Task: Putting older ToD on the fix list...'
    logger.info(answer)
    return answer


@shared_task
def fix_check():
    answer = 'Fix_check task is idle.'
    from collector.models.character import Character
    all = Character.objects.filter(need_fix=True).order_by('-pub_date')
    if len(all):
        c = all.first()
        answer = f'Task: Fixing avatar {c.rid}. {len(all)} remaining.'
        c.fix()
        c.save()
    else:
        fives = Character.objects.order_by('pub_date').first(5)
        for c in fives:
            c.need_fix = True
            c.save()
        answer = f'Task: Putting older avatars on the fix list...'

    logger.info(answer)
    return answer



