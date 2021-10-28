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
