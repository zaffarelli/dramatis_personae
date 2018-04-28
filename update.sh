#!/bin/bash
clear
echo "Make migrations..."
python3 manage.py makemigrations
echo "Migrate..."
python3 manage.py migrate
echo "Updating CSS from SCSS..."
sass /home/zaffarelli/Projects/github/fics7/collector/static/collector/styles.scss /home/zaffarelli/Projects/github/fics7/collector/static/collector/styles.css
echo "Launching server..."
python3 manage.py runserver
