#!/bin/bash

celery -A dramatis_personae worker  -l WARNING --beat -E
