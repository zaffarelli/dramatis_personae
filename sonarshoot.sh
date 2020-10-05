#!/usr/bin/env bash
clear

echo "Cleansing Coverage"

coverage erase

echo "Rebuilding Coverage"

coverage run -m pytest
coverage report
coverage xml

echo "Launching Sonar scanner"

/opt/sonar-scanner/bin/sonar-scanner
