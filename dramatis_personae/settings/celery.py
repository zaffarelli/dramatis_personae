"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from celery.schedules import crontab

CELERY_BROKER_URL = 'amqp://guest@phasma//'


CELERY_BEAT_SCHEDULE = {
    'pdf_schedule': {
        'task': 'collector.tasks.pdf_check',
        'schedule': 10,
        'args': (),
    },
    'fix_schedule': {
        'task': 'collector.tasks.fix_check',
        'schedule': 10,
        'args': (),
    },
    'todo_schedule': {
        'task': 'collector.tasks.todo',
        'schedule': 60,
        'args': (),
    },

}