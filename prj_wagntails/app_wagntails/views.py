from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import DogFilter, VolunteerDogFilter
from .forms import CreateUserForm, OwnerForm, DogForm, VolunteerForm, DateLocationForm
# Create your views here.
from .models import *


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
    return render(request, 'app_wagntails/register.html', context)


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
    return render(request, 'app_wagntails/login.html', context)


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
    return render(request, 'app_wagntails/owner.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def accountSettings(request):
    owner = request.user.owner
    form = OwnerForm(instance=owner)

    if request.method == 'POST':
        form = OwnerForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'app_wagntails/owner_account_settings.html', context)


@login_required(login_url='login')
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

    return render(request, 'app_wagntails/owner_dashboard.html', context)


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
    return render(request, 'app_wagntails/owner.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def dogs(request):
    dogs = Dog.objects.all()
    owner = Dog.objects.first().owner.name
    return render(request, 'app_wagntails/dogs.html', {'dogs': dogs, 'owner': owner})


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def volunteers(request, pk):
    owner = Owner.objects.get(id=pk)
    volunteers = Volunteer.objects.filter(city=owner.city)
    return render(request, 'app_wagntails/volunteers.html', {'volunteers': volunteers, 'owner': owner})


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def createDog(request, pk):
    DogFormSet = inlineformset_factory(Owner, Dog, fields=('name', 'breed', 'status', 'city', 'note'), extra=1)
    owner = Owner.objects.get(id=pk)
    formset = DogFormSet(queryset=Dog.objects.none(), instance=owner)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = DogForm(request.POST)
        formset = DogFormSet(request.POST, instance=owner)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset, 'owner': owner}
    return render(request, 'app_wagntails/dog_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def updateDog(request, pk):
    dog = Dog.objects.get(id=pk)
    form = DogForm(request.POST or None, instance=dog)
    print('DOG:', dog)
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            dog.owner = request.owner
            dog.save()
            return redirect('/')

    context = {'form': form, 'dog': dog}
    return render(request, 'app_wagntails/dog_update_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def deleteDog(request, pk):
    dog = Dog.objects.get(id=pk)
    if request.method == "POST":
        dog.delete()
        return redirect('/')

    context = {'item': dog}
    return render(request, 'app_wagntails/dog_delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def addDateLocation(request, pk):
    owner = Owner.objects.get(id=pk)
    form = DateLocationForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'owner': owner}
    return render(request, 'app_wagntails/date_location.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def updateDateLocation(request, pk):
    dateLocation = DateLocation.objects.get(id=pk)
    form = DateLocationForm(request.POST or None, instance=dateLocation)
    if request.method == 'POST':

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'location': dateLocation}
    return render(request, 'app_wagntails/update_location.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['owner'])
def deleteDateLocation(request, pk):
    dateLocation = DateLocation.objects.get(id=pk)
    if request.method == "POST":
        dateLocation.delete()
        return redirect('/')

    context = {'datelocation': dateLocation}
    return render(request, 'app_wagntails/date_location_delete.html', context)


################### Volunteer Related Methods ########################

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

            return redirect('login')

    context = {'form': form}
    return render(request, 'app_wagntails/register.html', context)


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
    return render(request, 'app_wagntails/loginVolunteer.html', context)


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

    return render(request, 'app_wagntails/volunteer_dashboard.html', context)


@login_required(login_url='loginVolunteer')
@allowed_users(allowed_roles=['volunteer'])
def accountSettingsVolunteer(request):
    volunteer = request.user.volunteer
    form = VolunteerForm(instance=volunteer)

    if request.method == 'POST':
        form = VolunteerForm(request.POST, request.FILES, instance=volunteer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'app_wagntails/volunteer_account_settings.html', context)


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
    return render(request, 'app_wagntails/volunteer.html', context)


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
    return render(request, 'app_wagntails/volunteer.html', context)


@login_required(login_url='loginVolunteer')
@allowed_users(allowed_roles=['volunteer'])
def associateVolunteer(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    dogs = Dog.objects.filter(city=volunteer.city)
    print('DOGS:', dogs)
    for dog in dogs:
        print('Dog City:', dog.city)
    context = {'volunteer': volunteer, 'dogs': dogs}
    return render(request, 'app_wagntails/volunteer_dog_form.html', context)
