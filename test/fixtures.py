import pytest
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timezone

load_dotenv()  # Load environment variables from .env file

USERNAME = os.getenv("DATABASE_USERNAME")
PASSWORD = os.getenv("DATABASE_PASSWORD")
uri = f"mongodb+srv://{USERNAME}:{PASSWORD}@se_project.ox1e0tt.mongodb.net/?retryWrites=true&w=majority&appName=se_project"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client[os.getenv("DATABASE")]


@pytest.fixture
def token():
    return "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMmYzMDAwNjA3QGRzLnN0dWR5LmlpdG0uYWMuaW4iLCJzY29wZXMiOlsidXNlciJdLCJleHAiOjE3MjMzODk0NDJ9.tK3Htj_yvf_0Ib-ozr63ZHLyQpoHDSvaGWKRXxfmH4s"


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

@pytest.fixture
def course_id():
    return "CS01"

@pytest.fixture
def ensure_course(token, url, course_id):
    # Create success
    path = url + "course/create"

    data = {"course_id": course_id, "course_name": "Python Data Structures and Algorithms"}
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})


# @pytest.fixture
# def user_id():
#     return "your_user_id_here"

@pytest.fixture
def week_id():
    return 1  

@pytest.fixture
def assignment_id():
    return "66b3903725cfaedcce34af1d"

@pytest.fixture
def assignment():
    return {
        "question": "What is the capital of France?",
        "q_type": "MCQ",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answers": ["Paris"],
        "assgn_type": "AQ",
        "course_id": "CS01",
        "week": 1,
        "evaluated": False,
        "deadline": datetime.now(timezone.utc).isoformat()
    }

@pytest.fixture
def assignments():
    return [
        {
            "question": "What is 2 + 2?",
            "q_type": "MCQ",
            "options": [3, 4, 5],
            "answers": [4],
            "assgn_type": "AQ",
            "course_id": "CS01",
            "week": 1,
            "evaluated": False,
            "deadline": datetime.now(timezone.utc).isoformat()
        },
        {
            "question": "What is the boiling point of water?",
            "q_type": "MCQ",
            "options": [90, 100, 110],
            "answers": [100],
            "assgn_type": "AQ",
            "course_id": "CS01",
            "week": 2,
            "evaluated": False,
            "deadline": datetime.now(timezone.utc).isoformat()
        }
    ]