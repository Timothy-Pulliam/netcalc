#!/bin/sh
gunicorn --bind 0.0.0.0:80 --workers 3 --access-logfile - --error-logfile - main:app