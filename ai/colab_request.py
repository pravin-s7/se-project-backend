import requests

url = "https://b876-34-16-218-145.ngrok-free.app/" 

def search_generate(course_id, week, query):
    r = requests.post(
        url + "search_generate",
        json={"query": query, "course_id": course_id, "week": week},
    )
    print("Colab request status", r.status_code)
    if r.status_code == 200:
        return r.json()["response"]
    else:
        return "Could not generate response"


def search_generate_flashcard(course_id, week, query):
    r = requests.post(
        url + "search_generate_flashcard",
        json={"query": query, "course_id": course_id, "week": week},
    )
    print("Colab request status", r.status_code)
    if r.status_code == 200:
        return r.json()["response"]
    else:
        return "Could not generate response"


def generate(query):
    r = requests.post(
        url + "generate",
        json={"query": query},
    )
    print("Colab request status", r.status_code)
    if r.status_code == 200:
        return r.json()["response"]
    else:
        return "Could not generate response"
    


# print(search_generate('CS01', 12 , 'What is NP Complete'))