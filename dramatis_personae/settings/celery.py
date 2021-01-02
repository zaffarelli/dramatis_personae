"""
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
"""
from celery.schedules import crontab

#CELERY_BROKER_URL = 'amqp://guest@phasma//'
CELERY_BROKER_URL = 'amqp://guest@galliard//'


CELERY_BEAT_SCHEDULE = {
    'pdf_schedule': {
        'task': 'collector.tasks.pdf_check',
        'schedule': 15,
        'args': (),
    },
    'fix_schedule': {
        'task': 'collector.tasks.fix_check',
        'schedule': 18,
        'args': (),
    },
    'todo_schedule': {
        'task': 'collector.tasks.todo',
        'schedule': 31,
        'args': (),
    },
    'skills_schedule': {
        'task': 'collector.tasks.skills_check',
        'schedule': 44,
        'args': (),
    },
    'tod_schedule': {
        'task': 'collector.tasks.tod_check',
        'schedule': 37,
        'args': (),
    },

}