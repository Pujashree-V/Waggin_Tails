import django_filters
from django_filters import DateFilter, CharFilter

from .forms import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']


class DogFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="year", lookup_expr='gte')
    end_date = DateFilter(field_name="year", lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Dog
        form = DogForm
        fields = '__all__'
        exclude = ['owner', 'profile_pic']


class VolunteerDogFilter(django_filters.FilterSet):
    city = CharFilter(field_name='city', lookup_expr='exact')

    class Meta:
        model = Dog
        form = VolunteerDogForm
        fields = '__all__'
        exclude = ['owner', 'profile_pic']
