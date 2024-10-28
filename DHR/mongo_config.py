from django.conf import settings
from pymongo import MongoClient

MONGO_URI = settings.MONGO_URI

client = MongoClient(MONGO_URI)

db = client['DHR'] 
