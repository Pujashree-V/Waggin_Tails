#!/bin/bash
# Set up script for wagntails

echo "setting up wagntails"

if ! hash python; then
    echo "python is not installed"
    exit 1
fi

ver=$(python -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "35" ] || [ "$ver" -gt "38" ]; then
    echo "This python version $(python -V 2>&1) is not supported"
    echo "This script requires python 3.5 and less than 38"
    exit 1
fi

python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip install django
pip install django-countries
pip install django-filter
pip install Pillow
pip install djangorestframework
pip install django-widget-tweaks
pip install whitenoise

cd prj_wagntails
python manage.py makemigrations app_wagntails
python manage.py migrate app_wagntails
python manage.py migrate
python manage.py create_groups
python manage.py createsuperuser
#python manage.py runserver
