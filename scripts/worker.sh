#!/bin/sh

celery -A dramatis_personae worker -l WARNING -B -E
