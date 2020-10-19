#!/usr/bin/env bash
clear
export DJANGO_SETTINGS_MODULE=dramatis_personae.settings.local
echo "Cleansing Coverage"

coverage erase

echo "Rebuilding Coverage"

coverage run manage.py test
coverage report
coverage xml

echo "Launching Sonar scanner"

/opt/sonar-scanner/bin/sonar-scanner
