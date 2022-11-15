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
        'schedule': 5,
        'args': (),
    },
    'todo_schedule': {
        'task': 'collector.tasks.todo',
        'schedule': 50,
        'args': (),
    },
    'handle_messages': {
        'task': 'collector.tasks.handle_messages',
        'schedule': 10,
        'args': (),
    },
    'skills_schedule': {
        'task': 'collector.tasks.skills_check',
        'schedule': crontab(minute='*/30'),
        'args': (),
    },
    'tod_schedule': {
        'task': 'collector.tasks.tod_check',
        'schedule': crontab(hour='*/5'),
        'args': (),
    },
    'policies_schedule': {
        'task': 'collector.tasks.policies_check',
        'schedule': crontab(minute='*/20'),
        'args': (),
    },

}