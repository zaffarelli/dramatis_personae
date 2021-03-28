'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'pdf_schedule': {
        'task': 'collector.tasks.pdf_check',
        'schedule': 120,
        'args': (),
    },
    'fix_schedule': {
        'task': 'collector.tasks.fix_check',
        'schedule': 15,
        'args': (),
    },
    'todo_schedule': {
        'task': 'collector.tasks.todo',
        'schedule': 25,
        'args': (),
    },
    'skills_schedule': {
        'task': 'collector.tasks.skills_check',
        'schedule': 45,
        'args': (),
    },
    'tod_schedule': {
        'task': 'collector.tasks.tod_check',
        'schedule': 30,
        'args': (),
    },
}