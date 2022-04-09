#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py migrate
python manage.py collectstatic --noinput


uwsgi --socket :9000 --workers 4 --master --enable-threads --module motochas.wsgi