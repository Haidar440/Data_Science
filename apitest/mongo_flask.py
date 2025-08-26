from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

# Flask app
app = Flask(__name__)

# MongoDB Connection
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

@app.route("/data", methods=["GET"])
def get_data():
    collection = db["users"]   # change this to your collection
    data = list(collection.find({}, {"_id": 0}))  # fetch all docs, exclude _id
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
