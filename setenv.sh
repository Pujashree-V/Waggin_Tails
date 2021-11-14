cd prj_wagntails
rm -rf prj_wagntails/app_wagntails/migrations
rm db.sqlite3
cd ..
python -m venv env 
source ./env/bin/activate
python -m pip install --upgrade pip
pip install django django-countries django-filter Pillow djangorestframework django-widget-tweaks whitenoise
cd prj_wagntails
python manage.py makemigrations app_wagntails
python manage.py migrate app_wagntails
python manage.py migrate
python manage.py create_groups
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'sreeku.ralla@gmail.com', 'Gibb@#123')" | python manage.py shell
