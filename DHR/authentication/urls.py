from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('', views.home, name='home'),
    path('create_superuser/', views.create_superuser_view, name='create_superuser'),
]
