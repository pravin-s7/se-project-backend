from fixtures import url, course_id, ensure_course, token
import requests
import json


def test_course_material_create_put_delete(url, course_id, token, ensure_course):
    # Create Success
    path = url + "course_material/create"
    data = {
        "course_id": course_id,
        "week": 2,
        "material_type": "video_URL",
        "content": "Main URL",
        "url": "https://www.youtube.com/@IITMadrasBSDegreeProgramme"
    }
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 201
    assert payload.get("message") == "success"
    assert payload.get("db_entry_id") is not None

    _id = payload.get("db_entry_id")
    # Update Success
    path = url + "course_material/update/" + _id
    data = {
        "week": 2,
        "material_type": "video_URL",
        "content": "IIT Madras Main Youtube URL",
        "url": "https://www.youtube.com/@IITMadrasBSDegreeProgramme"
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 202
    assert payload.get("message") is not None

    # Delete Success
    path = url + "course_material/delete/" + _id
    res = requests.delete(path, headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 200


def test_course_material_get_correct(url, token, course_id):
    path = url + "course_material/get/" + course_id
    res = requests.get(path, headers={"Authorization": token})

    print(res.status_code)
    json_response = res.json()
    assert res.status_code == 200
    assert type(json_response) == list


def test_course_material_get_incorrect(url, token, course_id):
    path = url + "course_material/get/" + course_id + '123a'
    res = requests.get(path, headers={"Authorization": token})

    print(res.status_code)
    json_response = res.json()
    assert res.status_code == 404

def test_course_material_get_incorrect_404(url, token):
    path = url + "course_material/get/" + "666f6f2d6261722d71757578"
    res = requests.get(path, headers={"Authorization": token})

    print(res.status_code)

    assert res.status_code == 404

def test_course_material_post_incorrect_404(url, token, course_id):
    path = url + "course_material/create"
    data = {
        "course_id": course_id + '123al',
        "week": 2,
        "material_type": "video_URL",
        "content": "Main URL",
        "url": "https://www.youtube.com/@IITMadrasBSDegreeProgramme"
    }
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    print(res.status_code, res.json())
    assert res.status_code == 404

def test_course_material_post_incorrect_422(url, token, course_id):
    path = url + "course_material/create"
    data = {
        "course_id": course_id,
        "week": 2,
        "url": "https://www.youtube.com/@IITMadrasBSDegreeProgramme"
    }
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    print(res.status_code)
    assert res.status_code == 422

def test_course_material_put_incorrect_404(url, token):
    path = url + "course_material/update/" + "666f6f2d6261722d71757578"
    data = {
        "week": 2,
        "material_type": "video_URL",
        "content": "IIT Madras Main Youtube URL",
        "url": "https://www.youtube.com/@IITMadrasBSDegreeProgramme"
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(payload, res.status_code)
    assert res.status_code == 404

def test_course_material_put_incorrect_422(url, token):
    path = url + "course_material/update/" + "hello"
    data = {
        "week": 2,
        "material_type": "video_URL",
        "content": "IIT Madras Main Youtube URL",
        "url": "https://www.youtube.com/@IITMadrasBSDegreeProgramme"
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})
    print(res.status_code)
    assert res.status_code == 422

def test_course_material_delete_incorrect_404(url, token):
    path = url + "course_material/delete/" + "666f6f2d6261722d71757578"
    res = requests.delete(path, headers={"Authorization": token})
    print(res.json(), res.status_code)
    assert res.status_code == 404

def test_course_material_delete_incorrect_422(url, token):
    path = url + "course_material/delete/" + "something"
    res = requests.delete(path, headers={"Authorization": token})
    print(res.json(), res.status_code)
    assert res.status_code == 422