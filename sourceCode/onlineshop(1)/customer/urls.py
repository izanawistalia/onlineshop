from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('product/', views.product, name="product"),
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('create_customer/', views.create_customer, name="create_customer"),
    path('create_order/<str:pk>/', views.create_order, name="create_order"),
    path('update_order/<str:pk>/', views.update_order, name="update_order"),
    path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),
    path('register_customer/', views.register_customer, name="register_customer"),
    path('login_customer/', views.login_customer, name="login_customer"),
    path('logout_customer/', views.logout_customer, name="logout_customer"),
    path('user/', views.user, name="user"),
    path('profile/', views.profile, name="profile")
]
