from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default="default.png")
    phone = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=50, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=50, null=True, choices=CATEGORY)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    