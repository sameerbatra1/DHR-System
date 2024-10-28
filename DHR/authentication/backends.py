from pymongo import MongoClient
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.conf import settings
from .models import User

class MongoBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]
        user_data = db.users.find_one({"username": username})

        if user_data and check_password(password, user_data["password"]):
            return User(username=user_data["username"], password=user_data["password"])
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
