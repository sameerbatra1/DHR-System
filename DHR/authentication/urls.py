from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('', views.home, name='home'),
    path('create_superuser/', views.create_superuser_view, name='create_superuser'),
    path('check_superuser/', views.check_superuser, name='check_superuser'),
    path('view_all_users/', views.view_all_users, name='view_all_users'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
]
