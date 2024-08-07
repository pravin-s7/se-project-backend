import requests
import json
from fixtures import token, url, course_id, delete_course


def test_create_course(token, url, course_id, delete_course):
    # Create success
    path = url + "course/create"

    data = {"course_id": course_id, "course_name": "Data Structures"}
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})

    json_response = res.json()
    assert json_response
    assert json_response.get("message") == "success"
    assert json_response.get("db_entry_id") is not None


def test_create_course_1(token, url, course_id):
    # Duplicate create invalid output
    path = url + "course/create"

    data = {"course_id": course_id, "course_name": "Data Structures"}
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})

    json_response = res.json()

    assert json_response
    assert res.status_code == 409
    assert json_response.get("detail") is not None


def test_incomplete_create_course(token, url):
    #Incomplete input
    path = url + "course/create"

    data = {"course_name": "Data Structures"}
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})

    json_response = res.json()

    assert json_response
    assert res.status_code == 422
    assert json_response.get("detail") is not None


def test_incomplete_create_course_2(token, url):
    # Incomplete Create input
    path = url + "course/create"

    data = {
        "course_id": "CSD001",
    }
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})

    json_response = res.json()

    assert json_response
    assert res.status_code == 422
    assert json_response.get("detail") is not None


def test_course_get(token, url):
    # Incorrect GET with wrong id
    path = url + "course/get/some_random_id"

    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert json_response
    assert res.status_code == 404
    assert json_response.get("detail") is not None


def test_course_get_2(token, url):
    # Incorrect GET without ID
    path = url + "course/get/"

    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert json_response
    assert res.status_code == 404
    assert json_response.get("detail") is not None


def test_course_get_correct(token, url, course_id):
    # Correct GET
    path = url + "course/get/" + course_id

    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert json_response
    assert res.status_code == 200
    assert json_response.get("course_id") == course_id
    assert json_response.get("_id") is not None
    assert json_response.get("course_name") is not None


def test_course_get_material_correct(token, url, course_id):
    # Correct course material get
    path = url + "/course/course_material/" + course_id

    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert type(json_response) == list
    assert res.status_code == 200


def test_course_get_material_incorrect(token, url):
    # Incorrect GET with wrong id
    path = url + "/course/course_material/" + "Something random"

    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response, res.status_code)
    assert res.status_code == 404


def test_course_get_contents_correct(token, url, course_id):
    # Correct get
    path = url + "/course/get_contents/"
    params = {
        'course_id': course_id
    }
    res = requests.get(path,params=params, headers={"Authorization": token})

    json_response = res.json()
    
    print(json_response)
    assert type(json_response) == list
    assert res.status_code == 200


def test_course_get_contents_incorrect(token, url):
    # InCorrect GET with wrong id
    path = url + "/course/get_contents/" + "something"
    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert res.status_code == 404


def test_course_get_week_contents_correct(token, url, course_id):
    #Correct get with correct id and params
    path = url + "/course/get_week_content/"
    params = {
        'course_id': course_id,
        'week': 1
    }
    res = requests.get(path, params=params, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert type(json_response) == list
    assert res.status_code == 200


def test_course_get_week_contents_incorrect(token, url):
    # InCorrect GET with wrong id
    path = url + "/course/get_week_content/" + "something"
    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert res.status_code == 404


def test_course_get_assignment_correct(token, url, course_id):
    #Correct get with correct id and params
    path = url + "/course/get_assignment/"
    params = {"course_id": course_id, "week": 1, "assgn_type": "AQ"}
    res = requests.get(path, params=params, headers={"Authorization": token})

    json_response = res.json()
    print(json_response, res.status_code)
    assert type(json_response) == list
    assert res.status_code == 200


def test_course_get_assignment_incorrect(token, url):
    # InCorrect GET
    path = url + "/course/get_week_content/" + "something"
    res = requests.get(path, headers={"Authorization": token})

    json_response = res.json()
    print(json_response)
    assert res.status_code == 404

def test_course_update_incorrect_1(token, url, course_id):
    #Incorrect with missing input
    path = url + "course/update/" + course_id
    data = {
        "course_id": course_id,
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})

    json_response = res.json()

    assert json_response
    assert res.status_code == 422
    assert json_response.get("detail") is not None

def test_course_update_incorrect_2(token, url, course_id):
    #Incorrect with missing input
    path = url + "course/update/" + course_id
    data = {
        "course_name": course_id,
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})

    json_response = res.json()

    assert json_response
    assert res.status_code == 422
    assert json_response.get("detail") is not None

def test_course_update_correct(token, url, course_id):
    #Correct get with correct id and params
    path = url + "course/update/" + course_id
    data = {
        "course_name": 'DSA',
        "course_id": course_id
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})

    json_response = res.json()

    assert json_response
    assert res.status_code == 202
    assert json_response.get("message") == 'success'