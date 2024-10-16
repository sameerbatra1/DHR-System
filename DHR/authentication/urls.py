from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.custom_login_view, name='login'),
    path('home/', views.home, name='home'),
]
