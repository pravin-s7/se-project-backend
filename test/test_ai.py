from fixtures import url, course_id, ensure_course, token
import requests
import json


def test_generate_flash_card(url, course_id, token, ensure_course):
    # Create Flashcard after searching from the vector store
    path = url + "flash_card/generate"
    data = {
        "course_id": course_id,
        "week": 2,
        "title": "What is NP complete",
        "content": "",
    }

    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 200
    assert payload.get("content") is not None and len(payload.get("content")) > 0


def test_generic_generate(url, token):
    # Generate without search
    path = url + "/user/generate"

    data = {
        "query": """
        Improve the code
    def printer(x):
        for i in range(x):
            print(i)
        """
    }

    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 200
    assert payload.get("response") is not None and len(payload.get("response")) > 0

def test_search_generic_generate(url, token, course_id):
    #Generate with search from transcript
    path = url + "/user/generate"

    data = {
        "query": "What is NP complete",
        "course_id": course_id,
        "week": 12
    }

    res = requests.post(path, data=json.dumps(data), headers={"Authorization": token})
    payload = res.json()
    print(res.json(), res.status_code)
    assert res.status_code == 200
    assert payload.get("response") is not None and len(payload.get("response")) > 0
