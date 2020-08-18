from django.forms import ModelForm
from .models import Order, Customer
from django.contrib.auth.models import User
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']