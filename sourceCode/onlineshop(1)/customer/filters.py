import django_filters
from django_filters import DateFilter
from .models import *

class Orderfilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']

class Customerfilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    class Meta:
        model = Customer
        fields = ['name', 'phone']