from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

USERNAME = os.environ.get("DATABASE_USERNAME")
PASSWORD = os.getenv("DATABASE_PASSWORD")

# uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.mufz8bn.mongodb.net/?appName=Cluster0"
uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@se_project.ox1e0tt.mongodb.net/?retryWrites=true&w=majority&appName=se_project"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# db = client[os.environ.get("DATABASE")]
db = client[os.getenv("DATABASE")]