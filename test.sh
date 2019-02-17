#!/bin/bash
clear
#echo "Updating CSS from SCSS..."
#sass ./collector/static/collector/styles.scss ./collector/static/collector/styles.css
#echo "Collecting statics"
#python3 manage.py collectstatic --noinput --clear --link -v 0
echo "Launching tests..."
python3 manage.py test
