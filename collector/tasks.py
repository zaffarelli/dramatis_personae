from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.utils import timezone

from django.contrib import messages

# from celery import Celery
# from celery.schedules import crontab

from collector.utils.basic import make_audit_report

from optimizer.models.policy import Policy
import logging
from datetime import datetime, timedelta
from collector.utils.basic import get_current_config

logger = logging.getLogger(__name__)


@shared_task
def todo():
    from collector.models.character import Character
    from collector.models.tourofduty import TourOfDutyRef
    campaign = get_current_config()
    if campaign:
        to_be_fixed = campaign.dramatis_personae.filter(need_fix=True)
        to_be_pdfed = campaign.dramatis_personae.filter(need_pdf=True)
        balanced = campaign.dramatis_personae.filter(balanced=True)
        all = campaign.dramatis_personae.all()
        tod_to_be_fixed = TourOfDutyRef.objects.filter(need_fix=True)
        logger.info(f'Incoming TODO list... ({campaign.epic})')
        logger.info(f' - Characters to be fixed ..... {len(to_be_fixed)}')
        logger.info(f' - Characters ready for PDF ... {len(to_be_pdfed)}')
        logger.info(f' - Characters balanced ........ {len(balanced)}  / {len(all)}')
        logger.info(f' - ToDs to be fixed ........... {len(tod_to_be_fixed)}')
        oldest = Character.objects.filter(pub_date__lte=timezone.now() - timedelta(days=14))
        logger.info(f' - Oldest to be fixed ......... {len(oldest)}')
        answer = 'Todo'
    return answer


@shared_task
def pdf_check():
    answer = '/!\\ Pdf_check task is idle'
    from collector.models.character import Character
    campaign = get_current_config()
    all = campaign.dramatis_personae.filter(need_pdf=True)
    if len(all):
        c = all.first()
        answer = f'Task: Building PDF for {c.rid}'
        c.backup()
        c.save()
    logger.info(answer)
    return answer


@shared_task
def skills_check():
    answer = '/!\\ Skills_check task is idle.'
    logger.info(answer)
    return answer


@shared_task
def tod_check():
    answer = '/!\\ Tod_check task is idle.'
    from collector.models.tourofduty import TourOfDutyRef
    tbf = TourOfDutyRef.objects.filter(need_fix=True)
    if len(tbf):
        tod = tbf.first()
        tod.fix()
        tod.save()
        answer = f'Tod_check: Fixing [{tod.reference}] tod.'
    else:
        recent_ones = TourOfDutyRef.objects.filter(valid=False)
        if len(recent_ones):
            for t in recent_ones:
                t.need_fix = True
                t.save()
            answer = f'Tod_check: Putting older ToD on the fix list...'
    logger.info(answer)
    return answer


@shared_task
def fix_check():
    campaign = get_current_config()
    answer = '/!\\ Fix_check task is idle.'
    need_audit = False
    from collector.models.character import Character
    campaign = get_current_config()
    logger.info("FIX CHECK")
    all = Character.objects.filter(need_fix=True)
    if len(all):
        c = all.first()
        answer = f'Task: Fixing avatar {c.rid}. {len(all)} remaining.'
        c.fix()
        c.save()
        if len(all) == 1:
            need_audit = True
    else:
        oldest = Character.objects.filter(pub_date__lte=timezone.now() - timedelta(days=14))
        for c in oldest:
            c.need_fix = True
            logger.debug(f"To be fixed : [{c.full_name}]")
            c.save()
        if len(oldest):
            answer = f'Fix_check: Putting older avatars on the fix list...'
    logger.info(answer)
    if need_audit:
        make_audit_report(campaign)
    return answer

@shared_task
def policies_check():
    answer = f'/!\\ Policies_check task is idle.'
    all = Policy.objects.filter(is_applied=False)
    logger.debug(f'Found {len(all)} policies.')
    if len(all):
        p = all.first()
        logger.debug(f'Handling {p.name}.')
        x = p.perform()
        answer = f'-----------> Performing [{p.name}]: {x}'
        p.save()
    if len(all)<5:
        from collector.models.character import Character
        characters = Character.objects.order_by('pub_date')[:10]
        for c in characters:
            if not len(Policy.objects.filter(character=c)):
                p = Policy()
                p.character = c
                logger.info(f'Added policy for [{c.full_name}]')
            else:
                p = Policy.objects.filter(character=c)
                logger.info(f'Updated policy for [{c.full_name}]')
            p.is_applied = False
            p.fix()
            p.save()

        for p in Policy.objects.all():
            logger.debug(f'{p.name} --> {p.is_applied}')

    logger.info(answer)
    return answer


