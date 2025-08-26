from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Replace with your actual password
uri = "mongodb+srv://Nishan_Roy:Nishan_R@cluster0.7orh0.mongodb.net/?retryWrites=true&w=majority&appName=CLUSTER0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Database & collection
db = client["careerforge"]
jobs_collection = db["jobs"]

# Test connection
try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB Atlas!")
except Exception as e:
    print("❌ Connection failed:", e)
