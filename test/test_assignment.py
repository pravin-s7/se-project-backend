import requests
import json
import pytest
from datetime import datetime, timezone
from fixtures import token, assignment, assignment_id, assignments

BASE_URL = "http://localhost:8000/assignment"  # Replace with your actual API base URL

def test_create_question(token, assignment):
    path = BASE_URL + "/create"
    res = requests.post(path, data=json.dumps(assignment), headers={"Authorization": token, "Content-Type": "application/json"})
    print(res.json(), res.status_code)
    assert res.status_code == 201
    assert res.json().get("message") == "success"
    assert "db_entry_id" in res.json()

def test_create_many_questions(token, assignments):
    path = BASE_URL + "/create_many_questions"
    res = requests.post(path, data=json.dumps(assignments), headers={"Authorization": token, "Content-Type": "application/json"})
    print(res.json(), res.status_code)
    assert res.status_code == 201
    assert res.json().get("message") == "success"
    assert "db_entry_ids" in res.json()

def test_get_question(token, assignment_id):
    path = BASE_URL + f"/get/{assignment_id}"
    res = requests.get(path, headers={"Authorization": token})
    print(res.json(), res.status_code)
    assert res.status_code == 200
    assert "question" in res.json()

def test_update_question(token, assignment_id, assignment):
    update_data = {
        "question": "Updated question",
        "q_type": "MCQ",
        "options": ["Option 1", "Option 2"],
        "answers": ["Option 1"],
        "assgn_type": "AQ",
        "course_id": "CS01",
        "week": 1,
        "evaluated": False,
        "deadline": datetime.now(timezone.utc).isoformat()
    }
    path = BASE_URL + f"/update/{assignment_id}"
    res = requests.put(path, data=json.dumps(update_data), headers={"Authorization": token, "Content-Type": "application/json"})
    print(res.json(), res.status_code)
    assert res.status_code == 202
    assert res.json().get("msg") == "Assigment Updated"

def test_delete_question(token, assignment_id):
    path = BASE_URL + f"/delete/{assignment_id}"
    res = requests.delete(path, headers={"Authorization": token})
    print(res.json(), res.status_code)
    assert res.status_code == 200
    assert res.json().get("msg") == "Deleted Successfully"

# Error handling tests

def test_create_question_invalid_data(token):
    invalid_assignment = {
        "question": "What is the capital of France?",
        "q_type": "MCQ",
        # Missing 'options' and 'answers'
        "assgn_type": "AQ",
        "course_id": "CS01",
        "week": 1,
        "evaluated": False,
        "deadline": datetime.now(timezone.utc).isoformat()
    }
    path = BASE_URL + "/create"
    res = requests.post(path, data=json.dumps(invalid_assignment), headers={"Authorization": token, "Content-Type": "application/json"})
    print(res.status_code, res.json())
    assert res.status_code == 422

def test_get_question_not_found(token):
    invalid_id = "invalid_id"
    path = BASE_URL + f"/get/{invalid_id}"
    res = requests.get(path, headers={"Authorization": token})
    print(res.status_code)
    assert res.status_code == 422

def test_update_question_not_found(token):
    invalid_id = "invalid_id"
    update_data = {
        "question": "Updated question",
        "q_type": "MCQ",
        "options": ["Option 1", "Option 2"],
        "answers": ["Option 1"],
        "assgn_type": "AQ",
        "course_id": "CS01",
        "week": 1,
        "evaluated": False,
        "deadline": datetime.now(timezone.utc).isoformat()
    }
    path = BASE_URL + f"/update/{invalid_id}"
    res = requests.put(path, data=json.dumps(update_data), headers={"Authorization": token, "Content-Type": "application/json"})
    print(res.status_code)
    assert res.status_code == 422

def test_delete_question_not_found(token):
    invalid_id = "invalid_id"
    path = BASE_URL + f"/delete/{invalid_id}"
    res = requests.delete(path, headers={"Authorization": token})
    print(res.status_code)
    assert res.status_code == 422
