import os
from dotenv import load_dotenv
from pymongo import MongoClient

# 1) Load secrets
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "mydb")

# 2) Connect to Atlas
client = MongoClient(MONGODB_URI)

# 3) Quick ping (connectivity check)
client.admin.command("ping")
print("✅ Connected to MongoDB Atlas!")

# 4) Get DB & collection
db = client[DB_NAME]
users = db["users"]

# 5) Insert sample docs
users.insert_many([
    {"name": "Haidar", "email": "haidar@example.com"},
    {"name": "Ali", "email": "ali@example.com"}
])

# 6) Read (exclude _id)
for doc in users.find({}, {"_id": 0}):
    print(doc)
