from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add_voter/', views.add_voter, name='add_voter'),
    path('view_all_voters/', views.view_all_voter, name='view_all_voters'),
    path('delete_voter/<int:user_id>/', views.delete_voter, name='delete_voter'),
    path('update_voter/<int:user_id>/', views.update_voter, name='update_voter'),
]