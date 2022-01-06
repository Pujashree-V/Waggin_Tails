from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.deletion import RESTRICT
from django_countries.fields import CountryField
import random

# Create your models here.

DAYS = (
    ('Sunday', 'Sunday'),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)

GENDER = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('OTHER', 'OTHER'),
)

STATES = (
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Bihar', 'Bihar'),
    ('Chandigarh', 'Chandigarh'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
    ('Daman and Diu', 'Daman and Diu'),
    ('Delhi', 'Delhi'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Lakshadweep', 'Lakshadweep'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),
    ('Orissa', 'Orissa'),
    ('Pondicherry', 'Pondicherry'),
    ('Punjab', 'Punjab'),
    ('Rajasthan', 'Rajasthan'),
    ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'),
    ('Tripura', 'Tripura'),
    ('Uttaranchal', 'Uttaranchal'),
    ('Uttar Pradesh', 'Uttar Pradesh'),
    ('West Bengal', 'West Bengal'),
)

TIME_PREFERENCE = (
    ('4a.m. - 5a.m.', '4a.m. - 5a.m.'),
    ('5a.m. - 6a.m.', '5a.m. - 6a.m.'),
    ('6a.m. - 7a.m.', '6a.m. - 7a.m.'),
    ('7p.m. - 8p.m.', '7p.m. - 8p.m.'),
    ('8p.m. - 9p.m.', '8p.m. - 9p.m.'),
    ('9p.m. - 10p.m.', '9p.m. - 10p.m.'),
)

STATUS = (
    ('At Home', 'At Home'),
    ('Sheltered', 'Sheltered'),
    ('ForWalk', 'ForWalk'),
)

BREED = (
    ('Labrador', 'Labrador'),
    ('Huskey', 'Huskey'),
    ('GrateDane', 'GrateDane'),
)

class Person(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, unique=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    aadhaar = models.PositiveIntegerField(validators=[MaxValueValidator(999999999999)], unique=True,default=random.randint(0,99999999999))
   
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True, choices=STATES)
    postal_code = models.PositiveIntegerField(validators=[MaxValueValidator(999999)],default=000000)

    def get_username(self):
        return self.city
    
    class Meta:
        abstract = True

    
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.product.name

       
class Owner(Person):
    # user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, null=True)
    # phone = models.CharField(max_length=200, null=True)
    # email = models.CharField(max_length=200, null=True, unique=True)
    # profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    # aadhaar = models.PositiveIntegerField(validators=[MaxValueValidator(999999999999)], unique=True,default=random.randint(0,99999999999))
    # # address = models.CharField(max_length=500, null=True)
    # city = models.CharField(max_length=100, null=True)
    # state = models.CharField(max_length=100, null=True, choices=STATES)
    # postal_code = models.PositiveIntegerField(validators=[MaxValueValidator(999999)],default=000000)
    is_owner = models.BooleanField(default=True)
    

    def __str__(self):
        return self.name



class Dog(models.Model):
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=False)
    breed = models.CharField(max_length=200, null=True, choices=BREED)
    year = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    city = models.CharField(max_length=100, null=True)
    note = models.CharField(max_length=1000, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    profile_pic = models.ImageField(default="logo.jpeg", null=True, blank=True)

    def __str__(self):
        return self.name


# class User(models.Model):
#    first_name = models.CharField(max_length=255)

#    def get_username(self):
#        return self.username

#    class Meta:
#        abstract = True

# class Employee(User):
#    title = models.CharField(max_length=255)


class Volunteer(Person):
    # user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # name = models.CharField(max_length=200, null=True)
    # gender = models.CharField(max_length=20, null=True, choices=GENDER)
    # age = models.PositiveIntegerField(validators=[MaxValueValidator(60)],default=18)
    # phone = models.CharField(max_length=200, null=True)
    # email = models.EmailField(max_length=200, null=True, unique=True)
    # aadhaar = models.PositiveIntegerField(validators=[MaxValueValidator(999999999999)], unique=True,default=random.randint(0,99999999999))
    # # address = models.CharField(max_length=500, null=True)
    # city = models.CharField(max_length=100, null=True)
    # state = models.CharField(max_length=100, null=True, choices=STATES)
    # postal_code = models.PositiveIntegerField(validators=[MaxValueValidator(999999)],default=000000)
    day_pref = models.CharField(max_length=10, null=True, choices=DAYS)
    time_pref = models.CharField(max_length=20, null=True, choices=TIME_PREFERENCE)
    #profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    is_volunteer = models.BooleanField(default=True)
    dogs = models.ManyToManyField(Dog)

    def __str__(self):
        return self.name



class DateLocation(models.Model):
    name = models.CharField(max_length=30)
    street1 = models.CharField(max_length=90)
    street2 = models.CharField(max_length=90)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = CountryField()
    postal_code = models.PositiveIntegerField(validators=[MaxValueValidator(999999)],default=000000)
    
    def __str__(self):
        return self.name


class PlayDate(models.Model):
    playDate = models.DateField()
    location = models.ForeignKey(DateLocation, on_delete=RESTRICT)
    owner1 = models.ForeignKey(Owner, related_name='%(class)s_owner1', on_delete=RESTRICT)
    owner2 = models.ForeignKey(Owner, related_name='%(class)s_owner2', on_delete=RESTRICT)
    pet1 = models.ForeignKey(Dog, related_name='%(class)s_pet1', on_delete=RESTRICT)
    pet2 = models.ForeignKey(Dog, related_name='%(class)s_pet2', on_delete=RESTRICT)
    
    def __str__(self):
        return self.owner1.name + self.owner2.name + self.pet1.name + self.pet2.name + self.playDate

   
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    # class Meta:
    #     ordering = ('timestamp',)
