#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata default_info.json
python manage.py loaddata default_info_and_root_user.json
# python manage.py cronloop &