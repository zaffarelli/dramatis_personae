'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'pdf_schedule': {
        'task': 'cartograph.tasks.pdf_check',
        'schedule': 15,
        'args': (),
    },
    'fix_schedule': {
        'task': 'cartograph.tasks.fix_check',
        'schedule': 18,
        'args': (),
    },
    'todo_schedule': {
        'task': 'cartograph.tasks.todo',
        'schedule': 31,
        'args': (),
    },
    'skills_schedule': {
        'task': 'cartograph.tasks.skills_check',
        'schedule': 44,
        'args': (),
    },
    'tod_schedule': {
        'task': 'cartograph.tasks.tod_check',
        'schedule': 37,
        'args': (),
    },
}