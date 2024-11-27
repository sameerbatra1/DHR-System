from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.custom_login_view, name='login'),
    path('', views.custom_login_view, name='home'),
    path('create_user/', views.create_user_view, name='create_superuser'),
    # path('check_superuser/', views.check_superuser, name='check_superuser'),
    path('view_all_users/', views.view_all_users, name='view_all_users'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('check_superuser/', views.check_superuser_status, name='check_superuser_status'),
    path('users/', views.users, name='users'),
]
