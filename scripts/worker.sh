#!/bin/sh

celery worker -A dramatis_personae -l WARNING -B -E
