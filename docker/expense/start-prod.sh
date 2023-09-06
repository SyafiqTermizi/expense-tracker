#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

export DJANGO_SETTINGS_MODULE=expense.settings.prod
/usr/local/bin/python3 /app/manage.py collectstatic --noinput
/usr/local/bin/python3 /app/manage.py migrate --noinput
/usr/local/bin/gunicorn expense.wsgi -c ./gunicorn.conf.py
