#!/usr/bin/env bash
python manage.py migrate
python manage.py collectstatic --no-input --clear --verbosity 0
#exec gunicorn --bind 0.0.0.0:8000 dramatis_personae.wsgi
