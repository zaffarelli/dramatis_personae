'''
 ╔╦╗┬─┐┌─┐┌┬┐┌─┐┌┬┐┬┌─┐  ╔═╗┌─┐┬─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
  ║║├┬┘├─┤│││├─┤ │ │└─┐  ╠═╝├┤ ├┬┘└─┐│ ││││├─┤├┤
 ═╩╝┴└─┴ ┴┴ ┴┴ ┴ ┴ ┴└─┘  ╩  └─┘┴└─└─┘└─┘┘└┘┴ ┴└─┘
'''
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'pdf_schedule': {
        'task': 'collector.tasks.pdf_check',
        'schedule': crontab(minute='*/3'),
        'args': (),
    },
    'fix_schedule': {
        'task': 'collector.tasks.fix_check',
        'schedule': 30,
        'args': (),
    },
    'todo_schedule': {
        'task': 'collector.tasks.todo',
        'schedule': 50,
        'args': (),
    },
    'skills_schedule': {
        'task': 'collector.tasks.skills_check',
        'schedule': crontab(minute='*/30'),
        'args': (),
    },
    'tod_schedule': {
        'task': 'collector.tasks.tod_check',
        'schedule': 5,
        'args': (),
    },
    'policies_schedule': {
        'task': 'collector.tasks.policies_check',
        'schedule': 15,
        'args': (),
    },

}