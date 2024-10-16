from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if the access_time has passed
            if user.access_time and timezone.now() > user.access_time:
                user.is_active = False  # Set user as inactive if access_time has passed
                user.save()
                messages.error(request, 'Your access time has expired. Please contact the admin.')
                return redirect('login')  # Redirect to the login page
            elif user.is_active:
                login(request, user)
                return redirect('home')  # Redirect to home after successful login
            else:
                messages.error(request, 'Your account is deactivated. Please contact the admin.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'authentication/login.html')

def home(request):
    return render(request, 'authentication/home.html')