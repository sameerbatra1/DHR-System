# from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from mongo_config import db
import bcrypt
import jwt
import datetime
from django.conf import settings
from .user_manager import UserManager
from .forms import SuperuserForm
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
import pytz

users_collection = db['users']

@csrf_exempt
def custom_login_view(request):
    print("Login View")
    if request.method == 'GET':
        print("Getting get method")
        return render(request, 'authentication/login.html')

    if request.method == 'POST':
        print("POST method confirmed")

        try:
            print(f"Trying to get json data")
            data = json.loads(request.body)
            print(f"Got JSON data Successfully: {data}")
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format or empty body.'}, status=400)
        
        username = data.get('username')
        password = data.get('password')
        print(f"Username: {username}")
        print(f"Password: {password}")

        user = users_collection.find_one({'username': username})
        print(f"User: {user}")

        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                if user.get('access_time') and timezone.now() > user['access_time']:
                    # Deactivate the user
                    users_collection.update_one({'_id': user['_id']}, {'$set': {'is_active': False}})
                    return JsonResponse({'error': 'Your access time has expired. Please contact the admin.'}, status=403)

                elif user.get('is_active'):
                    # Get current time in PKT
                    pkt_tz = pytz.timezone('Asia/Karachi')
                    last_login_time = timezone.now() + timedelta(hours=5)

                    # Update the last_login field in the database
                    users_collection.update_one({'_id': user['_id']}, {'$set': {'last_login': last_login_time}})

                    access_token = jwt.encode({
                        'user_id': str(user['_id']),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # 30 mins token validity
                    }, settings.JWT_SECRET_KEY, algorithm='HS256')

                    refresh_token = jwt.encode({
                        'user_id': str(user['_id']),
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)  # 7 days token validity
                    }, settings.JWT_SECRET_KEY, algorithm='HS256')

                    return JsonResponse({
                        'refresh': refresh_token,
                        'access': access_token,
                        'first_name': user['first_name'],
                        'last_name': user['last_name'],
                        'user_type': user['user_type'],
                        'message': 'Login successful'
                    }, status=200)
                else:
                    return JsonResponse({'error': 'Your account is deactivated. Please contact the admin.'}, status=403)
            else:
                return JsonResponse({'error': 'Invalid username or password.'}, status=401)
        else:
            return JsonResponse({'error': 'Invalid username or password.'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_next_sequence_value(sequence_name):
    counters_collection = db['counters']  # This is your counters collection
    sequence_document = counters_collection.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        return_document=True
    )
    if sequence_document is None:
        # If the sequence document doesn't exist, you can create it here
        db.counters.insert_one({"_id": sequence_name, "sequence_value": 1})
        return 1
    return sequence_document['sequence_value']

# @api_view(['POST'])
def create_superuser_view(request):
    if request.method == 'POST':
        form = SuperuserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']  # Extract password from the form

            # Hash the password
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            user_id = get_next_sequence_value('user_id')

            current_time = timezone.now()

            superuser_data = {
                'id': user_id,  
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': hashed,
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
                'user_type': 'superuser',
                'access_time': None,  
                'last_login': current_time
            }

            users_collection.insert_one(superuser_data)
            return redirect('home')  # Redirect to a success page

    else:
        form = SuperuserForm()

    return render(request, 'authentication\create_superuser.html', {'form': form})

def home(request):
    return render(request, 'authentication/home.html')