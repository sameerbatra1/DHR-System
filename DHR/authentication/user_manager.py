# user_manager.py
from mongo_config import db
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class UserManager:
    collection = db['users']  # Replace with your users collection name

    @classmethod
    def create_user(cls, username, first_name, last_name, password, user_type):
        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'password': hashed_password,
            'user_type': user_type,
            'is_active': True,
            'is_staff': False,
        }
        result = cls.collection.insert_one(user_data)
        return str(result.inserted_id)

    @classmethod
    def create_superuser(cls, username, first_name, last_name, password):
        return cls.create_user(username, first_name, last_name, password, 'superuser')
