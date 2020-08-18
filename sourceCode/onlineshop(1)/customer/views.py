from django.shortcuts import render, redirect
from .models import Product, Tag, Order, Customer
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import Orderfilter, Customerfilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
#from django.http import HttpResponse

# Create your views here.
#@login_required(login_url="login")

def home(request):
    return render(request, 'customer/home.html')

@login_required
@admin_only
def dashboard(request):
    total = Order.objects.count()
    pending = Order.objects.filter(status='Pending').count()
    delivered = Order.objects.filter(status='Delivered').count()
    orders = Order.objects.all()
    customers = Customer.objects.all()
    myFilter = Customerfilter(request.GET, queryset=customers)
    customers = myFilter.qs
    context = {'customers': customers, 'orders': orders, 'total': total, 'delivered': delivered, 'pending': pending, 'myFilter': myFilter}
    return render(request, 'customer/dashboard.html', context)

@login_required
@allowed_users(allowed_rule=['admin'])
def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'customer/product.html', context)

@login_required
@allowed_users(allowed_rule=['admin'])
def customer(request, pk):
    cust = Customer.objects.get(pk=pk)
    order = cust.order_set.all()
    total = order.count()
    myFilter = Orderfilter(request.GET, queryset=order)
    order = myFilter.qs
    context = {'customer': cust, 'total': total, 'orders': order, 'myFilter': myFilter}
    return render(request, 'customer/customer.html', context)

@login_required
@allowed_users(allowed_rule=['admin'])
def create_customer(request):
    context = {}
    return render(request, 'customer/create_customer.html', context)

@login_required
@allowed_users(allowed_rule=['admin', 'customer'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    order = Customer.objects.get(pk=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=order)
    #form = OrderForm(initial={'customer': order})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/customer/'+str(order.id))
    context = {'formset': formset}
    return render(request, 'customer/create_order.html', context)

@login_required
@allowed_users(allowed_rule=['admin'])
def update_order(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = {'form': form}
    return render(request, 'customer/order.html', context)

@login_required
@allowed_users(allowed_rule=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/dashboard')
    context = {'order': order}
    return render(request, 'customer/delete.html', context)

@unauthenticated_user
def register_customer(request):
    form = CreateUserForm()
    if request.method == 'POST':
        if request.POST['password'] == request.POST['c_password']:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.set_password(user.password)
                user.save()
                name = request.POST['username']
                messages.success(request, name+' is successfully created')
                return redirect('/login_customer/')
            else:
                messages.error(request, form)
        else:
            messages.error(request, 'password and confirm password does not match')
    context = {'form': form}
    return render(request, 'customer/register_customer.html', context)

@unauthenticated_user
def login_customer(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')
            
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'customer/login_customer.html')

def logout_customer(request):
    logout(request)
    return redirect('login_customer')

@login_required
@allowed_users(allowed_rule=['customer'])
def user(request):
    orders = request.user.customer.order_set.all()
    #cus_id = request.user.customer.id
    total = orders.count()
    pending = orders.filter(status="Pending").count()
    delivered = orders.filter(status="Delivered").count()
    context = {'orders': orders, 'total': total, 'pending': pending, 'delivered': delivered}
    return render(request, 'customer/user.html', context)

@login_required
@allowed_users(allowed_rule=['customer'])
def profile(request):
    user = request.user.customer
    form = CustomerForm(instance=user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    context = {'form': form, 'user': user}
    return render(request, 'customer/profile.html', context)
