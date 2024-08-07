from fixtures import url, course_id, ensure_course, token
import requests
import json


def test_flashcard_create_get_put_delete(url, course_id, token, ensure_course):
    # Create Success
    path = url + "flash_card/create"
    data = {
        "course_id": course_id,
        "week": 2,
        "title": "What is NP complete",
        "content": "It is a class of problem where no polynomial time algorithm exists",
    }
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 201
    assert payload.get("message") == "success"
    assert payload.get("db_entry_id") is not None

    # Get Success
    _id = payload.get("db_entry_id")

    path = url + "flash_card/get/" + _id
    res = requests.get(path, headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 200
    assert payload.get("user_id") is not None
    assert payload.get("course_id") is not None
    assert payload.get("week") is not None
    assert payload.get("title") is not None
    assert payload.get("course_id") is not None

    # Update Success
    path = url + "flash_card/update/" + _id
    data = {
        "week": 10,
        "title": "NP complete?",
        "content": "It is a class of problem where no polynomial time algorithm exists.",
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 202
    assert payload.get("message") is not None

    # Delete Success
    path = url + "flash_card/delete/" + _id
    res = requests.delete(path, headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 200

    # Delete success check
    path = url + "flash_card/get/" + _id
    res = requests.get(path, headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 404


def test_flashcard_get_incorrect_422(url, token):
    path = url + "flash_card/get/" + "some_random_id"
    res = requests.get(path, headers={"Authorization": token})

    print(res.status_code)

    assert res.status_code == 422


def test_flashcard_get_incorrect_404(url, token):
    path = url + "flash_card/get/" + "666f6f2d6261722d71757578"
    res = requests.get(path, headers={"Authorization": token})

    print(res.status_code)

    assert res.status_code == 404

def test_flashcard_post_incorrect_422(url, token, course_id):
    path = url + "flash_card/create"
    data = {
        "course_id": course_id,
        "title": "What is NP complete",
        "content": "It is a class of problem where no polynomial time algorithm exists",
    }
    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    print(res.status_code)
    assert res.status_code == 422

def test_flashcard_put_incorrect_404(url, token):
    path = url + "flash_card/update/" + "666f6f2d6261722d71757578"
    data = {
        "week": 10,
        "title": "NP complete?",
        "content": "It is a class of problem where no polynomial time algorithm exists.",
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(payload, res.status_code)
    assert res.status_code == 404

def test_flashcard_put_incorrect_422(url, token):
    path = url + "flash_card/update/" + "hello"
    data = {
        "week": 10,
        "title": "NP complete?",
        "content": "It is a class of problem where no polynomial time algorithm exists.",
    }
    res = requests.put(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(payload, res.status_code)
    assert res.status_code == 422

def test_flashcard_delete_incorrect_404(url, token):
    path = url + "flash_card/delete/" + "666f6f2d6261722d71757578"
    res = requests.delete(path, headers={"Authorization": token})
    print(res.json(), res.status_code)
    assert res.status_code == 404

def test_flashcard_delete_incorrect_422(url, token):
    path = url + "flash_card/delete/" + "something"
    res = requests.delete(path, headers={"Authorization": token})
    print(res.json(), res.status_code)
    assert res.status_code == 422