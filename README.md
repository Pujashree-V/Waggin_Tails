# waggintails

To run the application you need to follow the following steps

from the folder waggintails

1. Create python3 virtual environment -- python3 -m venv env
2. Activate the environment with -- source env/bin/activate
3. Upgrate pip with -- python -m pip install --upgrade pip
4. Install Django framework wiht -- pip install django
5. Install Django support for countries -- pip install django-countries
6. Install Django support for filters -- pip install django-filter
7. Install Django support for Pillow -- pip install Pillow
8. Install Django support for REST -- pip install djangorestframework 
9. Install Django suppprt for widgets -- pip install django-widget-tweaks
10. Install Django support for whitenoise -- pip install whitenoise

Once you finish the environment to setup the application

1. Move into the Project folder -- cd prj_wagntails
2. You need to run the migrations for the Model
3. python manage.py makemigrations app_wagntails
4. python manage.py migrate app_wagntails
5. python manage.py migrate
6. python manage.py create_groups -- this creates groups for pet owners and volunteers apart from the customers for the pet products that are sold (yet to implement)
7. python manage.py createsuperuser -- this creates super user for the Django environment
8. python manage.py runserver

Currently you can do the following activities:

1. You can signup as a owner with localhost:8000/register
2. You can login as owner with localhost:8000/login
3. You can update the owner profile
4. You can view the listed volunteers with localhost:8000/viewVolunteers
5. You can add your pets / delete pets
6. You can signup as a volunteer with localhost:8000/registerVolunteer
7. You can login as a volunteer with localhost:8000/loginVolunteer
