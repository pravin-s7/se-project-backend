import pytest
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

USERNAME = os.getenv("DATABASE_USERNAME")
PASSWORD = os.getenv("DATABASE_PASSWORD")
uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@se_project.ox1e0tt.mongodb.net/?retryWrites=true&w=majority&appName=se_project"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client[os.getenv("DATABASE")]


@pytest.fixture
def token():
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMmYzMDAwNjA3QGRzLnN0dWR5LmlpdG0uYWMuaW4iLCJzY29wZXMiOlsidXNlciJdLCJleHAiOjE3MjMxMTY5NTN9.C6vwX52ZjgD57ag4FKHzsNUY15m9t8wWoHsuaxpLuIg"


@pytest.fixture
def url():
    return "http://localhost:8000/"


@pytest.fixture
def course_id():
    return "CS0001"


@pytest.fixture
def delete_course(course_id):
    find = db.course.find_one(filter={"course_id": course_id})
    if find:
        db.course.delete_one(filter={"course_id": course_id})