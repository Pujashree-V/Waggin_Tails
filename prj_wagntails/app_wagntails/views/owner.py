import re
from django import forms
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
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            group = Group.objects.get(name='owner')
            user.groups.add(group)
            # Added username after video because of error returning customer name if not added
            Owner.objects.create(
                user=user,
                name=user.username,
                email=email,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'app_wagntails/owner/register_owner.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'app_wagntails/owner/loginOwner.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def ownerPage(request):
    owner = request.user.owner
    dogs = request.user.owner.dog_set.all()

    total_dogs = dogs.count()
    sheltered = dogs.filter(status='Sheltered').count()
    forwalk = dogs.filter(status='ForWalk').count()

    print('DOGS:', dogs)

    context = {'dogs': dogs, 'owner': owner, 'total_dogs': total_dogs,
               'sheltered': sheltered, 'forwalk': forwalk}
    return render(request, 'app_wagntails/owner/owner_landingPage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def accountSettings(request):
    owner = request.user.owner
    form = OwnerForm(instance=owner)

    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            form.save()

    context = {'form': form, 'owner': owner}
    return render(request, 'app_wagntails/owner/owner_account_settings.html', context)


@login_required(login_url='baseLogin')
@admin_only
def home(request):
    dogs = Dog.objects.all()
    owners = Owner.objects.all()

    total_owners = owners.count()

    total_dogs = dogs.count()
    sheltered = dogs.filter(status='Sheltered').count()
    forwalk = dogs.filter(status='ForWalk').count()

    context = {'dogs': dogs, 'owners': owners,
               'total_orders': total_dogs, 'sheltered': sheltered,
               'forwalk': forwalk}

    return render(request, 'app_wagntails/owner/owner_dashboard.html', context)


@unauthenticated_user
def baseLogin(request):
    return render(request, 'app_wagntails/baseLogin.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def owner(request, pk_test):
    owner = Owner.objects.get(id=pk_test)

    dogs = owner.dog_set.all()
    dog_count = dogs.count()

    myFilter = DogFilter(request.GET, queryset=dogs)
    dogs = myFilter.qs

    context = {'owner': owner, 'dogs': dogs, 'dog_count': dog_count,
               'myFilter': myFilter}
    return render(request, 'app_wagntails/owner/sidebar.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def dogs(request, pk):
    owner = Owner.objects.get(id=pk)
    dogs = Dog.objects.filter(city=owner.city)
    return render(request, 'app_wagntails/owner/dogs.html', {'dogs': dogs, 'owner': owner})


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def volunteers(request, pk):
    owner = Owner.objects.get(id=pk)
    volunteers = Volunteer.objects.filter(city=owner.city)
    context = {'volunteers': volunteers, 'owner': owner}
    return render(request, 'app_wagntails/owner/volunteers.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def createDog(request, pk):
    DogFormSet = inlineformset_factory(Owner, Dog, fields=(
        'profile_pic', 'name', 'breed', 'gender', 'status', 'city', 'note'), extra=1)
    owner = Owner.objects.get(id=pk)
    formset = DogFormSet(queryset=Dog.objects.none(), instance=owner)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = DogForm(request.POST)
        formset = DogFormSet(request.POST, request.FILES, instance=owner)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset, 'owner': owner, 'dogs': owner.dog_set.all()}
    return render(request, 'app_wagntails/owner/dog_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def updateDog(request, pk):
    dog = Dog.objects.get(id=pk)
    owner = dog.owner
    form = DogUpdateForm(request.POST or None,request.FILES, instance=dog)
    context = {'form': form, 'dog': dog, 'owner': owner}
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            dog.owner = owner
            dog.save()
            return redirect('/')
        else:
            return render(request, 'app_wagntails/error.html', context)

    return render(request, 'app_wagntails/owner/dog_update_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def deleteDog(request, pk):
    dog = Dog.objects.get(id=pk)
    owner = dog.owner
    if request.method == "POST":
        dog.delete()
        return redirect('/')

    context = {'item': dog, 'owner': owner}
    return render(request, 'app_wagntails/owner/dog_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def addDateLocation(request, pk):
    owner = Owner.objects.get(id=pk)
    locations = DateLocation.objects.filter(city=owner.city)
    print(Owner.objects.get(id=pk))
    form = DateLocationForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'owner': owner, 'locations': locations}
    return render(request, 'app_wagntails/owner/date_location.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def updateDateLocation(request, pk, pk_test):
    print(request,pk,pk_test)
    dateLocation = DateLocation.objects.get(id=pk)
    owner = Owner.objects.get(id=pk_test)
    locations = DateLocation.objects.filter(city=owner.city)
    form = DateLocationForm(request.POST or None, instance=dateLocation)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'location': dateLocation,
               'owner': owner, 'locations': locations}
    return render(request, 'app_wagntails/owner/date_location_update.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def deleteDateLocation(request, pk, pk_test):
    dateLocation = DateLocation.objects.get(id=pk)
    owner = Owner.objects.get(id=pk_test)
    if request.method == "POST":
        dateLocation.delete()
        return redirect('/')

    context = {'datelocation': dateLocation, 'owner': owner}
    return render(request, 'app_wagntails/owner/date_location_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def addPlayDate(request, pk):
    owner = Owner.objects.get(id=pk)
    form = PlayDateForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'owner': owner}
    return render(request, 'app_wagntails/owner/playdate.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def error(request, pk):
    dog = Dog.objects.get(id=pk)
    owner = dog.owner
    print('DOG:', dog)
    context = {'form': forms, 'dog': dog, 'owner': owner}
    render(request, 'app_wagntails/error.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def ownerDashboard(request):
    owner = request.user.owner
    dogs = owner.dog_set.all()
    locations = DateLocation.objects.filter(city=owner.city)
    form = OwnerForm(instance=owner)

    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            form.save()

    context = {'form': form, 'owner': owner,
               'dogs': dogs, 'locations': locations}
    return render(request, 'app_wagntails/owner/owner_landingPage.html', context)



