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
from django.contrib.auth.decorators import login_required
from bson import ObjectId

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

def get_user_from_jwt(request):
    # print("In get_user_from_jwt token")
    token = request.headers.get('Authorization')  # Get token from Authorization header
    print(f"Token: {token}")
    if token:
        try:
            # Remove the 'Bearer ' prefix
            token = token.split()[1]
            print(f"Token from line 118: {token}")
            # print(f"Getting secret key: {settings.SECRET_KEY}")
            decoded_data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            # print(f"decoded data {decoded_data}")
            user_id = decoded_data.get('user_id')  # Assuming 'user_id' is stored in the JWT
            # print(f"User_id: {user_id}")
            # Use PyMongo to query the MongoDB collection by user_id
            user = users_collection.find_one({'_id': ObjectId(user_id)})
            if user:
                # print(f"user from line 127: {user}")
                return user
            else:
                return None  # User not found in MongoDB

        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token
    return None  # No token found

@csrf_exempt
def check_superuser(request):
    user = get_user_from_jwt(request)
    if user:
        return render(request, 'authentication/create_superuser.html')
    else:
        return JsonResponse({'error': 'You are not authorized to access this page.'}, status=401)

# @api_view(['POST'])
# @login_required@csrf_exempt
@csrf_exempt
def create_superuser_view(request):
    print("Calling create_superuser_view function")

    # Handling GET request
    if request.method == 'GET':
        form = SuperuserForm()
        return render(request, 'authentication/create_superuser.html', {'form': form})

    # Handling POST request
    elif request.method == 'POST':
        # Retrieve form data
        form = SuperuserForm(request.POST)
        
        print(f"Form data received: {request.POST}")
        
        # Authenticate the user based on JWT
        user = get_user_from_jwt(request)
        print(f"Getting User: {user}")
        
        if not user:
            return JsonResponse({'message': 'Authentication failed: Invalid token'}, status=401)

        print(f"Is Superuser: {user.get('is_superuser')}")  # Check if the user is a superuser
        if not user.get('is_superuser'):
            return JsonResponse({'message': 'Access denied: Only superusers can create users'}, status=403)
        # print(f"Form cleaned data: {form.cleaned_data}")
        # Check if form is valid
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']  # Extract password from the form
            access_time = form.cleaned_data['access_time']
            # Hash the password using bcrypt
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Generate a unique user_id and store the time
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
                'user_type': 'voter_manager',
                'access_time': access_time,
                'last_login': current_time
            }
            
            # Insert the new user into MongoDB
            users_collection.insert_one(superuser_data)
            print(f"Superuser created with ID: {user_id}")

            return JsonResponse({'success': True, 'message': 'Superuser created successfully'})

        else:
            print("Form is invalid")
            return JsonResponse({'success': False, 'message': 'Form validation failed'}, status=400)

    else:
        # This should return if request method is not GET or POST
        print(f"Invalid request method: {request.method}")
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def home(request):
    return render(request, 'authentication/home.html')

