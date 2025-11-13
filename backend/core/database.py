# core/database.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# --- Synchronous client (for normal routes like expenses/income) ---
sync_client = MongoClient(MONGO_URI)
db = sync_client[DB_NAME]
expense_collection = db["expense"]
income_collection = db["income"]

# --- Async client (for auth routes) ---
async_client = AsyncIOMotorClient(MONGO_URI)
async_db = async_client[DB_NAME]
users_collection = async_db["users"]  # MongoDB will create this automatically
