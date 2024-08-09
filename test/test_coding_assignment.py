import pytest
import requests
import json
from datetime import datetime, timezone
from fixtures import token

BASE_URL = "http://localhost:8000"

ASSIGNMENT_ID = "66a789366a6dc45d5c1ffffa"

def test_create_programming_question(token):
    path = BASE_URL + "/coding_assignment/create_programming_question"
    data = {
        "question": "Write a function to add two numbers.",
        "language": "python",
        "public_testcase": [{"input": "1\n2", "output": "3"}],
        "private_testcase": [{"input": "3\n4", "output": "7"}],
        "assgn_type": "PPA",
        "course_id": "CS01",
        "week": 1,
        "deadline": datetime.now(timezone.utc).isoformat()
    }
    
    response = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    assert response.status_code == 201
    payload = response.json()
    assert payload.get("msg") == "success"
    assert payload.get("db_entry_id") is not None

def test_get_coding_assignment(token):
    path = f"{BASE_URL}/coding_assignment/get/{ASSIGNMENT_ID}"
    response = requests.get(path, headers={"Authorization": token})
    
    assert response.status_code == 200

def test_run_code(token):
    path = f"{BASE_URL}/coding_assignment/run"
    data = {
        "assgn_id": ASSIGNMENT_ID,
        "code": "def add(a, b):\n    return a + b\n\nprint(add(*map(int, input().split())))"
    }
    
    response = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    assert response.status_code == 200
    payload = response.json()
    
    assert "public_testcases" in payload
    assert "private_testcases" in payload
    assert "passed_public_count" in payload
    assert "passed_private_count" in payload


def test_update_coding_assignment(token):
    path = f"{BASE_URL}/coding_assignment/update/{ASSIGNMENT_ID}"
    data = {
        "question": "Updated question",
        "language": "python",
        "public_testcase": [{"input": "5\n6", "output": "11"}],
        "private_testcase": [{"input": "7\n8", "output": "15"}],
        "assgn_type": "PPA",
        "week": 1,
        "deadline": datetime.now(timezone.utc).isoformat()
    }
    
    response = requests.put(path, data=json.dumps(data), headers={"Authorization": token})
    assert response.status_code == 202
    payload = response.json()
    assert payload.get("msg") == "Assigment Updated"
    
    # Verify update
    response_check = requests.get(f"{BASE_URL}/coding_assignment/get/{ASSIGNMENT_ID}", headers={"Authorization": token})
    updated_data = response_check.json()
    assert updated_data.get("question") == "Updated question"
    assert updated_data.get("public_testcase")[0]["output"] == "11"

def test_delete_coding_assignment(token):
    path = f"{BASE_URL}/coding_assignment/delete/{ASSIGNMENT_ID}"
    response = requests.delete(path, headers={"Authorization": token})
    
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("msg") == "Assignment Deleted"
    
    # Verify deletion
    response_check = requests.get(f"{BASE_URL}/coding_assignment/get/{ASSIGNMENT_ID}", headers={"Authorization": token})
    assert response_check.status_code == 404

def test_create_programming_question_invalid_data(token):
    path = BASE_URL + "/coding_assignment/create_programming_question"
    invalid_data = {
        "language": "python", # Missing question
        "public_testcase": [{"input": "1\n2", "output": "3"}],
        "private_testcase": [{"input": "3\n4", "output": "7"}],
        "assgn_type": "PPA",
        "course_id": "CS01",
        "week": 1,
        "deadline": datetime.now(timezone.utc).isoformat()
    }
    
    response = requests.post(path, data=json.dumps(invalid_data), headers={"Authorization": token})
    assert response.status_code == 422


def test_get_coding_assignment_invalid_id(token):
    invalid_id = "invalid_id"
    path = f"{BASE_URL}/coding_assignment/get/{invalid_id}"
    response = requests.get(path, headers={"Authorization": token})
    
    assert response.status_code == 422 

def test_delete_coding_assignment_invalid_id(token):
    path = f"{BASE_URL}/coding_assignment/delete/invalid_id"
    response = requests.delete(path, headers={"Authorization": token})
    
    assert response.status_code == 422

def test_run_code_invalid_id(token):
    path = f"{BASE_URL}/coding_assignment/run"
    invalid_data = {
        "assgn_id": "invalid_id",
        "code": "def add(a, b):\n    return a + b\n\nprint(add(*map(int, input().split())))"
    }
    
    response = requests.post(path, data=json.dumps(invalid_data), headers={"Authorization": token})
    assert response.status_code == 422

def test_create_programming_question_no_token():
    path = BASE_URL + "/coding_assignment/create_programming_question"
    data = {
        "question": "Write a function to add two numbers.",
        "language": "python",
        "public_testcase": [{"input": "1\n2", "output": "3"}],
        "private_testcase": [{"input": "3\n4", "output": "7"}],
        "assgn_type": "PPA",
        "course_id": "CS01",
        "week": 1,
        "deadline": datetime.now(timezone.utc).isoformat()
    }
    
    response = requests.post(path, data=json.dumps(data))  # Missing Authorization header
    assert response.status_code == 401
