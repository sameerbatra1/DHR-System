from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add_voter/', views.add_voter, name='add_voter'),
    path('view_all_voters/', views.view_all_voter, name='view_all_voters'),
    path('delete_voter/<int:user_id>/', views.delete_voter, name='delete_voter'),
    path('update_voter/<int:user_id>/', views.update_voter, name='update_voter'),
    path('add_mohalla/', views.add_mohalla_name, name='add_mohalla'),
    path('update_block_numbers/', views.update_block_numbers, name='update_block_numbers'),
    path('check_voter/<int:user_id>/', views.check_voter, name='check_voter'),
    path('check_voter/', views.check_voter_page, name='check_voter')
]