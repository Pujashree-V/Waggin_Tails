from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.db import models
from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OwnerForm(ModelForm):
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['user']


class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'

class DogUpdateForm(ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'
        exclude = ['owner']

class VolunteerForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = '__all__'
        exclude = ['user', 'dogs']


class CustomMMCF(forms.ModelMultipleChoiceField):

    def label_from_instance(self, member):
        return member.name


class VolunteerDogForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'dogs']

    city = models.CharField(max_length=30)
    dogs = CustomMMCF(
        queryset=Dog.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class DateLocationForm(ModelForm):
    class Meta:
        model = DateLocation
        fields = '__all__'


class PlayDateForm(ModelForm):
    class Meta:
        model = PlayDate
        fields = ['playDate','location','owner2','pet1','pet2']
        exclude = ['owner1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = DateLocation.objects.all()
        self.fields['owner2'].queryset = Owner.objects.none()
        self.fields['pet1'].queryset = Dog.objects.none()
        self.fields['pet2'].queryset = Dog.objects.none()