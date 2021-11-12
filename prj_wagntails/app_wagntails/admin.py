from django.contrib import admin

from .models import *
from django.contrib import admin
from app_wagntails.models import Message
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Owner)
admin.site.register(Dog)
admin.site.register(Volunteer)
admin.site.register(DateLocation)
admin.site.register(PlayDate)
admin.site.register(Message)
