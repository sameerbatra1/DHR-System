from django import forms
from django.core.exceptions import ValidationError
import bcrypt
from mongo_config import db
from django.utils import timezone  # Import timezone

users_collection = db['users']

from datetime import datetime

class SuperuserForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    access_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],
        required=False,
        help_text="Set the access time in the format YYYY-MM-DD HH:MM"
    )

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_username(self):
        # Check for existing usernames using PyMongo
        username = self.cleaned_data['username']
        if users_collection.find_one({'username': username}):
            raise ValidationError("Username already exists.")
        return username

    def clean_access_time(self):
        access_time = self.cleaned_data.get('access_time')
        if access_time and access_time < timezone.now():
            raise ValidationError("Access time cannot be in the past.")
        return access_time
