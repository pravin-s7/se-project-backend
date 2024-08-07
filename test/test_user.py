import requests
import json
import pytest
from fixtures import token, course_id, week_id

BASE_URL = "http://localhost:8000"  

def test_get_current_user(token):
    path = BASE_URL + "/user/me"
    res = requests.get(path, headers={"Authorization": token})
    print(res.json())
    assert res.status_code == 200
    assert 'user_id' in res.json() 

def test_get_flash_card_course_filter(token, course_id):
    path = BASE_URL + f"/user/get/course/{course_id}"
    res = requests.get(path, headers={"Authorization": token})
    assert res.status_code == 200
    assert isinstance(res.json(), list)  # Assuming response is a list of flashcards

def test_get_flash_card_course_and_week_filter(token, course_id, week_id):
    path = BASE_URL + f"/user/get/course/{course_id}/week/{week_id}"
    res = requests.get(path, headers={"Authorization": token})
    assert res.status_code == 200
    assert isinstance(res.json(), list) 

def test_get_all_flashcards(token):
    path = BASE_URL + "/user/flashcards"
    res = requests.get(path, headers={"Authorization": token})
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_get_flash_card_course_filter_404(token):
    invalid_course_id = "invalid_course_id"
    path = BASE_URL + f"/user/get/course/{invalid_course_id}"
    res = requests.get(path, headers={"Authorization": token})
    assert res.status_code == 404

def test_get_flash_card_course_and_week_filter_422(token):
    invalid_course_id = "invalid_course_id"
    invalid_week_id = 999  # week_id does not exist
    path = BASE_URL + f"/user/get/course/{invalid_course_id}/week/{invalid_week_id}"
    res = requests.get(path, headers={"Authorization": token})
    assert res.status_code == 422

def test_get_all_flashcards_unauthorized():
    path = BASE_URL + "/user/flashcards"
    res = requests.get(path)  # No token provided
    assert res.status_code == 401
