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
    path('check_voter/', views.check_voter_page, name='check_voter'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('election_mode/', views.election_mode_view, name='election_mode'),   
    path('activate_election_mode/', views.activate_election_mode, name='activate_election_mode'),
    path('voter_analytics/', views.voter_analytics, name='voter_analytics'),
    path('voter_analytics_page/', views.voter_analytics_page, name='voter_analytics_page'),    
    path('voter_by_mohalla/', views.mohalla_voter_stats, name='voter_by_mohalla'),
    path('voter_by_gender/', views.voter_by_gender, name='voter_by_gender'),
 
]