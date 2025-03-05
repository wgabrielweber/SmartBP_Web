from pymongo import MongoClient
from configs_st import MONGO_URI, DB_NAME

# Initialize the MongoDB client and database
client = MongoClient(MONGO_URI)
db = client[DB_NAME]  # This is the database instance