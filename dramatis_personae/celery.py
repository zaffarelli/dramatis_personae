from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dramatis_personae.settings')

app = Celery('dramatis_personae')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()