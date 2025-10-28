from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url = os.getenv("Mongo_URL")

client = MongoClient(mongo_url)
db = client['civipulsedb']
complaints_collection = db['complaints']
print(complaints_collection)