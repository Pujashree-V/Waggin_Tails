import re
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models.aggregates import Max
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from ..decorators import unauthenticated_user, allowed_users, admin_only
from ..filters import DogFilter, VolunteerDogFilter
from ..forms import CreateUserForm, OwnerForm, DogForm, PlayDateForm, VolunteerForm, DateLocationForm, DogUpdateForm, chatMessageForm
from ..models import *
# Django Build in User Model
from django.contrib.auth.models import User
from django.http.response import HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from app_wagntails.models import Message
from app_wagntails.serializers import MessageSerializer, UserSerializer
import json                                              # Our Message model
# Create your views here.



@unauthenticated_user
def baseLogin(request):
    return render(request, 'app_wagntails/baseLogin.html')


@unauthenticated_user
def registerVolunteerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='volunteer')
            user.groups.add(group)
            # Added username after video because of error returning customer name if not added
            Volunteer.objects.create(
                user=user,
                name=user.username,
                email=email,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('loginVolunteer')

    context = {'form': form}
    return render(request, 'app_wagntails/volunteer/register.html', context)


@unauthenticated_user
def loginVolunteerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homeVolunteer')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'app_wagntails/volunteer/loginVolunteer.html', context)


def logoutVolunteerUser(request):
    logout(request)
    return redirect('loginVolunteer')


@login_required(login_url='loginVolunteer')
@admin_only
def homeVolunteer(request):
    dogs = Dog.objects.all()
    volunteers = Volunteer.objects.all()

    total_volunteers = volunteers.count()

    total_dogs = dogs.count()
    sheltered = dogs.filter(status='Sheltered').count()
    forwalk = dogs.filter(status='ForWalk').count()

    context = {'volunteers': volunteers, 'dogs': dogs}

    return render(request, 'app_wagntails/volunteer/volunteer_dashboard.html', context)


@login_required(login_url='loginVolunteer')
@allowed_users(allowed_roles=['volunteer'])
def accountSettingsVolunteer(request):
    volunteer = request.user.volunteer
    form = VolunteerForm(instance=volunteer)

    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            form.save()

    context = {'form': form, 'volunteer': volunteer}
    return render(request, 'app_wagntails/volunteer/volunteer_account_settings.html', context)


@login_required(login_url='loginVolunteer')
@allowed_users(allowed_roles=['volunteer'])
def volunteerPage(request):
    volunteer = request.user.volunteer
    dogs = request.user.volunteer.dogs.all()

    total_dogs = dogs.count()
    sheltered = dogs.filter(status='Sheltered').count()
    forwalk = dogs.filter(status='ForWalk').count()

    print('DOGS:', dogs)

    context = {'dogs': dogs, 'volunteer': volunteer, 'total_dogs': total_dogs,
               'sheltered': sheltered, 'forwalk': forwalk}
    return render(request, 'app_wagntails/volunteer/volunteer_landingPage.html', context)


@login_required(login_url='loginVolunteer')
@allowed_users(allowed_roles=['volunteer'])
def volunteer(request, pk_test):
    volunteer = Volunteer.objects.get(id=pk_test)

    dogs = volunteer.dogs.all()
    dog_count = dogs.count()

    myFilter = DogFilter(request.GET, queryset=dogs)
    dogs = myFilter.qs

    context = {'volunteer': volunteer, 'dogs': dogs, 'dog_count': dog_count,
               'myFilter': myFilter}
    return render(request, 'app_wagntails/volunteer/volunteer.html', context)


@login_required(login_url='loginVolunteer')
@allowed_users(allowed_roles=['volunteer'])
def associateVolunteer(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    dogs = Dog.objects.filter(city=volunteer.city)
    print('DOGS:', dogs, Volunteer.objects.get(id=pk))
    context = {'dogs': dogs, 'volunteer': volunteer}
    return render(request, 'app_wagntails/volunteer/volunteer_dog_form.html', context)


@login_required(login_url='volunteerLogin')
@allowed_users(allowed_roles=['volunteer'])
def volunteerDashboard(request):
    volunteer = request.user.volunteer
    form = VolunteerForm(instance=volunteer)

    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            form.save()

    context = {'form': form, 'volunteer': volunteer}
    return render(request, 'app_wagntails/volunteer/volunteer_landingPage.html', context)

