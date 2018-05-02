#!/bin/bash
clear
echo "Make migrations..."
python3 manage.py makemigrations
echo "Migrate..."
python3 manage.py migrate
echo "Updating CSS from SCSS..."
sass ./collector/static/collector/styles.scss ./collector/static/collector/styles.css
echo "Launching server..."
python3 manage.py runserver 0.0.0.0:8000
